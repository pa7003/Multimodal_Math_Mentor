import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add user site-packages to path (for Windows pip --user installs)
user_site_packages = os.path.expanduser("~\\AppData\\Roaming\\Python\\Python311\\site-packages")
if user_site_packages not in sys.path:
    sys.path.append(user_site_packages)

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from utils.ocr import OCRProcessor
    from utils.audio import AudioProcessor
    from agents.parser import ParserAgent
    from agents.router import IntentRouter
    from agents.verifier import VerifierAgent
    from agents.explainer import ExplainerAgent
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Multimodal Math Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Initialization ---

@st.cache_resource
def get_ocr_processor():
    return OCRProcessor()

@st.cache_resource
def get_audio_processor():
    return AudioProcessor()

@st.cache_resource
def get_agents():
    return {
        "parser": ParserAgent(),
        "router": IntentRouter(),
        "solver": SolverAgent(),
        "verifier": VerifierAgent(),
        "explainer": ExplainerAgent()
    }

# --- Pipeline Logic ---

def display_results(result):
    if result.get("success"):
        st.session_state.final_result = result
        st.subheader("💡 Solution")
        st.markdown(result["explanation"])
        
        st.divider()
        st.markdown("### Technical Steps")
        st.code(result["solution"])
        
        with st.expander("Verification & Sources"):
            st.write(f"Confidence: {result['verification']['confidence']}")
            if result.get("citations"):
                st.write(f"Sources: {result['citations']}")
            st.json(result['verification'])
            
    elif result.get("error") == "clarification":
        st.error("Ambiguous Input")
        st.write(result["data"]["clarification_question"])
        
    elif result.get("error") == "verification_failed":
        st.warning("⚠️ The verifier is not confident in the solution.")
        st.write("### Proposed Solution")
        st.markdown(result["solution"])
        
        st.write("### Critique")
        st.error(result["verification"]["critique"])
        
        col1, col2 = st.columns(2)
        with col1:
             if st.button("Accept Anyway"):
                 st.success("User overrode verification. (Mock Action)")
        with col2:
             if st.button("Retry"):
                 st.info("Retry logic to be implemented (Recursive Agent call)")

    # Feedback / Learning Loop
    st.divider()
    st.write("### Feedback")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ Mark as Correct (Learn)"):
            with st.spinner("Learning..."):
                agents = get_agents()
                topic = st.session_state.current_problem_data.get("topic", "General")
                agents["solver"].learn(
                    result["explanation"], # Storing explanation is often better for future retrieval than raw technical steps, or store both.
                    result["solution"], 
                    topic
                )
            st.success("Stored in Memory! This will help solve future problems.")
            
    with col_b:
        if st.button("❌ Incorrect"):
            st.text_input("Describe error for future improvements:")

def run_solver_pipeline(text_input):
    agents = get_agents()
    
    with st.status("Thinking...", expanded=True) as status:
        # 1. Parsing
        status.write("Parsing problem...")
        parsed = agents["parser"].parse(text_input)
        
        if parsed.get("needs_clarification"):
            status.update(label="Clarification Needed", state="error")
            return {"error": "clarification", "data": parsed}
            
        st.session_state.current_problem_data = parsed
        status.write(f"Problem Parsed: {parsed.get('topic')}")
        
        # 2. Routing
        status.write("Routing...")
        route = agents["router"].route(parsed)
        status.write(f"Strategy: {route.get('category')} ({route.get('complexity')})")
        
        # 3. Solving
        status.write("Solving with RAG...")
        solve_result = agents["solver"].solve(parsed)
        solution = solve_result["solution"]
        
        # 4. Verification
        status.write("Verifying...")
        verification = agents["verifier"].verify(parsed["problem_text"], solution)
        
        if not verification["is_correct"] or verification["confidence"] < 0.8:
            status.update(label="Verification Alert", state="error")
            return {
                "error": "verification_failed",
                "solution": solution,
                "verification": verification,
                "solve_result": solve_result
            }
            
        # 5. Explanation
        status.write("Generating Explanation...")
        final_explanation = agents["explainer"].explain(parsed["problem_text"], solution)
        
        status.update(label="Solved!", state="complete")
        return {
            "success": True,
            "solution": solution,
            "explanation": final_explanation,
            "verification": verification,
            "citations": solve_result["citations"]
        }

# --- UI Layout ---

st.title("🎓 Multimodal Math Mentor")
st.markdown("Upload a problem (Image/Audio) or type it out to get a step-by-step solution.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Handling (Better UX)
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY") and not os.getenv("GROQ_API_KEY"):
        st.warning("⚠️ No API Key found in .env")
        api_key_input = st.text_input(
            "Enter OpenAI / Gemini / Groq API Key:", 
            type="password",
            help="Get one from https://platform.openai.com/, https://aistudio.google.com/ or https://console.groq.com/"
        )
        if api_key_input:
            if api_key_input.startswith("sk-"):
                os.environ["OPENAI_API_KEY"] = api_key_input
                st.success("OpenAI Key Set!")
            elif api_key_input.startswith("AI"):
                os.environ["GOOGLE_API_KEY"] = api_key_input
                st.success("Gemini Key Set!")
            elif api_key_input.startswith("gsk_"):
                os.environ["GROQ_API_KEY"] = api_key_input
                st.success("Groq Key Set!")
            else:
                st.error("Invalid Key Format")
    
    input_mode = st.radio("Input Mode", ["Text", "Image", "Audio"])
    st.divider()
    st.info("System Ready")

# Session State
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

# Main Content
st.write(f"### Current Mode: {input_mode}")

if input_mode == "Text":
    problem = st.text_area("Enter your math problem here:", height=150, value=st.session_state.extracted_text)
    if st.button("Solve"):
        if problem.strip():
            result = run_solver_pipeline(problem)
            display_results(result)
        else:
            st.warning("Please enter a problem.")

elif input_mode == "Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Problem", use_container_width=True)
        if st.button("Extract Text"):
            with st.spinner("Extracting text..."):
                ocr = get_ocr_processor()
                result = ocr.process_image(uploaded_file.getvalue())
                if result.get("error"):
                    st.error(f"OCR Error: {result['error']}")
                else:
                    st.session_state.extracted_text = result["text"]
                    st.success(f"Extracted (Conf: {result['confidence']:.2f})")
                    st.rerun()

    if st.session_state.extracted_text:
        st.subheader("Verify Extracted Text")
        edited_text = st.text_area("Edit text if incorrect:", value=st.session_state.extracted_text, height=150)
        st.session_state.extracted_text = edited_text
        if st.button("Confirm & Solve"):
             result = run_solver_pipeline(st.session_state.extracted_text)
             display_results(result)

elif input_mode == "Audio":
    tab_upload, tab_record = st.tabs(["📂 Upload File", "🎙️ Record Audio"])
    
    with tab_upload:
        st.warning("Upload a WAV/MP3 file.")
        audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])
        
        if audio_file:
            st.audio(audio_file)
            if st.button("Transcribe Upload"):
                with st.spinner("Transcribing..."):
                    audio_proc = get_audio_processor()
                    result = audio_proc.process_audio(audio_file.getvalue())
                    if result.get("error"):
                        st.error(f"ASR Error: {result['error']}")
                    else:
                        st.session_state.extracted_text = result["text"]
                        st.rerun()

    with tab_record:
        st.write("Click to record audio:")
        audio_value = st.audio_input("Record")
        
        if audio_value:
            # Playback
            st.audio(audio_value)
            
            if st.button("Transcribe Recording"):
                with st.spinner("Transcribing..."):
                    audio_proc = get_audio_processor()
                    # Export to bytes
                    audio_bytes = audio_value.getvalue()
                    result = audio_proc.process_audio(audio_bytes)
                    if result.get("error"):
                        st.error(f"ASR Error: {result['error']}")
                    else:
                        st.session_state.extracted_text = result["text"]
                        st.rerun()

    if st.session_state.extracted_text:
        st.subheader("Verify Transcription")
        edited_text = st.text_area("Edit text if incorrect:", value=st.session_state.extracted_text, height=150)
        st.session_state.extracted_text = edited_text
        if st.button("Confirm & Solve"):
             result = run_solver_pipeline(st.session_state.extracted_text)
             display_results(result)




# Multimodal Math Mentor

## Overview
The Multimodal Math Mentor is an innovative application designed to assist learners in mastering mathematical concepts through various modalities. Leveraging advanced technologies, this application integrates a Streamlit UI, LangChain agents, Optical Character Recognition (OCR), audio processing, Retrieval-Augmented Generation (RAG), and multiple Large Language Model (LLM) providers.

## Features
- **Streamlit UI**: A user-friendly interface developed using Streamlit, allowing users to easily interact with the application's capabilities.
- **LangChain Agents**: The app utilizes LangChain to enable dynamic interactions and facilitate complex workflows involving multiple data sources.
- **OCR Processing**: Recognizes and processes written mathematical problems from images, converting them into digital format for analysis and solution.
- **Audio Processing**: Supports voice input to allow users to verbally communicate their queries and receive spoken feedback.
- **RAG**: Retrieval-Augmented Generation enhances the quality of responses by using external databases to inform its answers based on real-time data retrieval.
- **Multiple LLM Providers**: Leverages different LLM providers to ensure users receive accurate and contextually relevant responses regardless of query complexity.

## Setup Instructions
To set up the Multimodal Math Mentor, follow these steps:
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/pa7003/Multimodal_Math_Mentor.git
   cd Multimodal_Math_Mentor
   ```

2. **Install Dependencies**:  
   Ensure you have Python installed. Then, use pip to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:  
   Create a `.env` file in the root directory and add the necessary configuration variables as indicated in the provided `.env.example` file.

4. **Run the Application**:  
   Start the Streamlit application with the following command:
   ```bash
   streamlit run app.py
   ```

5. **Access the UI**:  
   Open your web browser and go to `http://localhost:8501` to use the application.

## Contributions
We welcome contributions from the community. Please fork the repository and submit a pull request with your changes. Make sure to follow the code of conduct and contribution guidelines.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
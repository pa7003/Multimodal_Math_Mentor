# Multimodal Math Mentor

## Project Overview
The Multimodal Math Mentor is an AI-powered math problem solver designed to assist users in solving mathematical problems through various input modalities including text, images (using OCR), and audio (utilizing speech-to-text technology). This project leverages state-of-the-art machine learning algorithms to provide accurate and efficient solutions across different interface formats.

## Features
- **Multi-Input Capability**: Accepts text queries, images with mathematical expressions, and audio instructions.
- **Real-Time Processing**: Processes input data in real-time, providing immediate feedback and solutions.
- **User-Friendly Interface**: Intuitive design that enhances user engagement and ease of use.
- **Cross-Platform Compatibility**: Works on multiple platforms and devices.

## System Architecture
The architecture is designed to handle various types of inputs efficiently. It includes:
- **Input Module**: Captures input data from text, image, and audio.
- **Processing Unit**: Utilizes OCR for images and STT for audio, alongside NLP techniques for text processing.
- **Output Module**: Displays solutions and explanations clearly.

![System Architecture Diagram](path/to/architecture-diagram.png)

## Prerequisites
- Python 3.8+
- Required Libraries:
  - `tensorflow`
  - `opencv-python`
  - `speech_recognition`
  - `Pillow`
  - (and others as needed)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pa7003/Multimodal_Math_Mentor.git
   cd Multimodal_Math_Mentor
   ```
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. Create a `.env` file in the root directory to set up your environment variables.
2. Add API keys and configurations as needed:
   ```plaintext
   API_KEY=your_api_key_here
   ```

## Usage Instructions
1. Run the application:
   ```bash
   python app.py
   ```
2. Input your math problem through text, image upload, or speech input.

## Project Structure
```plaintext
Multimodal_Math_Mentor/
│
├── app.py
├── models/
│   ├── model.py
├── utils/
│   ├── ocr.py
│   ├── stt.py
├── requirements.txt
├── README.md
```  

## Core Components
- **OCR Module**: Converts images of math problems into text.
- **STT Module**: Transcribes spoken math problems into text.
- **NLP Module**: Analyzes and interprets the text to find solutions.

## API Keys Setup
1. Signup for API services (e.g., OCR and STT services).
2. Get your API keys and add them to your `.env` file.

## Supported LLM Providers
This project currently supports:
- OpenAI GPT-3
- Google Bert

## Architecture Workflow
![Architecture Workflow Diagram](path/to/workflow-diagram.png)

1. User inputs data (text/image/audio) →
2. Processing Module (OCR/STT/NLP) →
3. Output Module (Solution Display)

## Contributing Guidelines
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/new-feature
   ```
5. Create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting
- **Problem**: Application does not start.  
  **Solution**: Check for missing dependencies in `requirements.txt`.
- **Problem**: OCR not recognizing text accurately.  
  **Solution**: Ensure proper lighting and image quality for input photos.

---
For more details, visit the [GitHub repository](https://github.com/pa7003/Multimodal_Math_Mentor) for updates, issues, and discussions.  

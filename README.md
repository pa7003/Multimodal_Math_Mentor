# Multimodal Math Mentor

## Overview
A comprehensive tool designed to assist learners in exploring various mathematical concepts through interactive multimodal techniques.

## Features
- Interactive problem-solving assistance
- Visualization of mathematical concepts
- Support for multiple learning styles

## System Architecture
The system is built using a microservices architecture that enables scalability and easy integration of new features.

## Prerequisites
- Node.js (version 14 or higher)
- npm (version 6 or higher)
- Python (version 3.6 or higher)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pa7003/Multimodal_Math_Mentor.git
   cd Multimodal_Math_Mentor
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

## Configuration
- Update the configuration file located at `config/config.json` with your settings.

## Usage Instructions
1. Start the server:
   ```bash
   npm start
   ```
2. Access the application at `http://localhost:3000`.

## Project Structure
- `src/`: Contains the source code
- `config/`: Configuration files
- `tests/`: Unit tests and integration tests

## Core Components
- Frontend: Built with React
- Backend: Node.js with Express framework
- Database: MongoDB

## API Keys Setup
- Obtain API keys for external services needed for the application (e.g., LLM providers) and update the `config/config.json` file.

## Supported LLM Providers
- OpenAI
- Hugging Face
- Custom providers (add your own in the configuration)

## Architecture Workflow
A brief diagram or flowchart of how the components interact with each other would go here.

## Contributing Guidelines
Please refer to `CONTRIBUTING.md` for detailed guidelines on contributing to this project.

## Troubleshooting
- Common issues and their fixes will be documented here.

## License Information
This project is licensed under the MIT License. See `LICENSE` for details.

#Trinity

Trinity is a terminal-based chatbot powered by Google's Gemini AI, designed to speak in the tone of a royal servant. It provides users with a unique, polite, and conversational AI experience.
Features

    🤖 Gemini-Powered Chat: Uses Google's generative AI for natural conversation.

    🗃️ Chat History Logging: Saves conversations to chat_log.json.

    🛠️ Customizable: Clean and modular Python code for easy editing.

Getting Started
Prerequisites

    Python 3.6 or higher

    A Google API key for Gemini (get one from Google AI Studio)

Installation

Clone the Repository:

    git clone https://github.com/psreyas09/Trinity.git
    cd Trinity

(Optional) Set Up a Virtual Environment:

    python -m venv trinity_env
    source trinity_env/bin/activate  # Windows: trinity_env\Scripts\activate

Install Required Libraries:

    pip install google-generativeai

Configure the API Key:

There are two ways to provide your Gemini API key:
🔐 Option 1: Use an Environment Variable (Recommended)

 On Linux/macOS:

    export GOOGLE_API_KEY="your-api-key-here"

 On Windows CMD:

    set GOOGLE_API_KEY=your-api-key-here

 On Windows PowerShell:

    $env:GOOGLE_API_KEY="your-api-key-here"

 In main.py, use:

    import os
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

🗂️ Option 2: Hardcode the Key (Not recommended for production)

In main.py, add:

    import google.generativeai as genai

    genai.configure(api_key="your-api-key-here")

⚠️ Do not commit your API key to public repositories!

Running Trinity

    python main.py

Once started, Trinity will begin chatting with you in a royal tone.
Project Structure

Trinity/
├── main.py             # Main script that runs the chatbot
├── chat_log.json       # Stores chat history
├── README.md           # This file
└── trinity_env/        # (Optional) Virtual environment

License

This project is licensed under the MIT License.
Author

Created by psreyas09

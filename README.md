Trinity

Trinity is a terminal-based chatbot powered by Google's Gemini AI, designed to speak in the tone of a royal servant. It provides users with a unique, polite, and conversational AI experience.
Features

    🤖 Gemini-Powered Chat: Uses Google's generative AI for natural conversation.

    🗃️ Chat History Logging: Saves conversations to chat_log.json.

    🛠️ Customizable: Clean and modular Python code for easy editing.

Getting Started
Prerequisites

Python 3.6 or higher

A Google API key for Gemini (from Google AI Studio)

Installation

Clone the Repository:

    git clone https://github.com/psreyas09/Trinity.git
    cd Trinity

Set Up a Virtual Environment (Recommended):

    python -m venv trinity_env
    source trinity_env/bin/activate  # Windows: trinity_env\Scripts\activate

Install Required Libraries:

Since there's no requirements.txt, install manually:

    pip install google-generativeai

Add Your API Key:

In main.py, replace the placeholder with your actual API key:

    genai.configure(api_key="YOUR_API_KEY")

Run the Chatbot

python main.py

Start chatting with Trinity directly from your terminal!
Project Structure

Trinity/
├── main.py             # Entry point for Trinity chatbot
├── chat_log.json       # Stores all chat history
├── README.md           # Project documentation
└── trinity_env/        # (Optional) Virtual environment directory

License

This project is licensed under the MIT License.
Author

Created by psreyas09

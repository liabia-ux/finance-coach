# 💰 Finance Coach Chatbot

An AI-powered finance chatbot that helps users understand their finances, build better habits, and make smarter financial decisions.

## 🚀 Features

- Conversational AI for financial questions
- Budgeting and saving guidance
- Personalized financial insights
- Simple web interface using Streamlit

## 🛠️ Tech Stack

- Python
- Streamlit
- OpenAI API

## 📦 Installation

1. Clone the repository:
git clone https://github.com/your-username/finance-coach.git

2. Navigate into the project folder:
cd finance-coach

3. Install dependencies:
pip install -r requirements.txt

4. Add your OpenAI API key:
Create a `.env` file and add:
OPENAI_API_KEY=your_api_key_here

## ▶️ Run the App

streamlit run streamlit_app.py

## 🧠 How It Works

- User enters a financial question
- The app sends the request to an AI model
- The model generates a response
- The response is displayed in a chat interface

## ⚠️ Disclaimer

This chatbot is for informational purposes only and does not provide professional financial advice.

## 👩🏽‍💻 Author

Khalia Anderson

This project contains the Ollama Modelfile for my finance chatbot.

## Rebuild the model

```bash
ollama create finance-coach -f Modelfile

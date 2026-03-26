# 💬 Finance Coach — A Financial Therapy Chatbot

Finance Coach is a conversational AI designed to help users build a healthier relationship with money.
Instead of just giving budgeting advice, it focuses on **financial behavior, emotions, and decision-making patterns**.

This is not just a budgeting tool — it’s a **financial wellness companion**.

---

## ✨ Features

### 🧠 Financial Therapy Conversations

* Gentle, non-judgmental tone
* Helps users reflect on spending habits and money emotions
* Redirects conversations back to financial wellness
* Encourages awareness before action

### 💡 Smart Guidance (Not Overwhelming)

* Short, conversational responses
* Practical suggestions (not rigid rules)
* Focus on behavior → not just numbers

### 🎯 Focused Scope

* Strictly limited to:

  * Budgeting
  * Spending habits
  * Saving strategies
  * Financial stress & mindset
* Politely redirects non-finance questions

### ⚡ Interactive UX

* Clean chat interface
* Reduced “prompt bubbles” (only 4 intentional starters)
* Human-like placeholder text
* Follow-up messages if user becomes inactive

### 📊 Budget Sidebar Tool

* Sleek, minimal UI (toggle-based)
* Users can:

  * Input income
  * Track spending categories
  * Reflect on financial balance
* Designed to feel **lightweight, not overwhelming**

### 🧠 Memory (Session-Based)

* Remembers context within conversation
* Builds continuity in financial discussions
* Makes interactions feel more personal

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **LLM Integration:** OpenAI API / Ollama (local models supported)
* **Language:** Python
* **Optional Models:**

  * `llama3`
  * `bge-small-en-v1.5` (for embeddings / knowledge retrieval)

---

## 🚀 How It Works

1. User starts a conversation
2. Bot responds in a **financial therapy style**
3. If needed, bot:

   * Asks reflective questions
   * Suggests small behavioral shifts
4. Budget tool supports **practical application**
5. If user goes off-topic → bot gently redirects:

   > “Are you feeling overwhelmed about money?”

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/liabia-ux/finance-coach.git
cd finance-coach
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run streamlit_app.py
```

---

## 🔐 Environment Variables

Create a `.env` or use Streamlit secrets:

```
OPENAI_API_KEY=your_api_key_here
```

---

## 🧭 Design Philosophy

Finance Coach is built on three principles:

### 1. Behavior Over Perfection

Money habits matter more than perfect budgets.

### 2. Emotional Awareness

Spending is often emotional — not just logical.

### 3. Simplicity Wins

Too many tools overwhelm users.
This app keeps things **clean, calm, and focused**.

---

## 🎯 Target Users

* People who feel overwhelmed by money
* Beginners who don’t know where to start
* Users tired of rigid budgeting apps
* Anyone wanting a **softer, more human approach** to finances

---

## ⚠️ Disclaimer

This chatbot:

* Does **not** provide financial, legal, or investment advice
* Is intended for **educational and behavioral support only**

---

## 🔮 Future Improvements

* Persistent long-term memory
* Mobile app version (iOS/Android)
* Spending pattern detection
* Personalized nudges & insights
* AI-driven budget recommendations
* Voice-based interaction

---

## 👩‍💻 Author

**Lia Anderson**
Information Systems & Analytics @ Loyola University Chicago

* Portfolio: [https://lia-portfolio-site.vercel.app](https://lia-portfolio-site.vercel.app)
* GitHub: [https://github.com/liabia-ux](https://github.com/liabia-ux)

---

## 💭 Final Thought

> “Most people don’t need more financial information —
> they need help understanding their behavior.”



## Rebuild the model

```bash
ollama create finance-coach -f Modelfile

import streamlit as st
from openai import OpenAI
import re

# -------------------------
# OPENAI CLIENT
# -------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------
# PAGE SETUP
# -------------------------
st.set_page_config(page_title="WalletWise", page_icon="")
st.title("WalletWise")
st.markdown("""
<style>
div.stButton > button {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(6px);
    color: #6b4f3b;
    border: 1px solid rgba(107, 79, 59, 0.25);
    border-radius: 14px;
    padding: 10px 16px;
    font-size: 14px;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    background: rgba(107, 79, 59, 0.12);
    border: 1px solid rgba(107, 79, 59, 0.6);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)
st.caption("A supportive budgeting and money wellness chatbot")

# ---------- SAMPLE QUESTION CALLBACK ----------
def use_sample_question(question):
    st.session_state.selected_question = question

# ---------- SAMPLE QUESTIONS ----------
st.markdown("**Try asking:**")

sample_questions = [
    "How much should I budget for groceries each month?",
    "Can you help me make a beginner monthly budget?",
    "Why do I keep overspending and how can I stop?",
    "What percentage of my income should go to rent?",
    "Help me split my budget into needs, wants, and savings.",
    "How can I reduce impulse spending?",
]

cols = st.columns(2)
for i, question in enumerate(sample_questions):
    with cols[i % 2]:
        if st.button(question, key=f"sample_{i}"):
            st.session_state.pending_prompt = question

# -------------------------
# SESSION STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "budget" not in st.session_state:
    st.session_state.budget = {
        "groceries": 300,
        "shopping": 200,
        "entertainment": 150,
        "bills": 500,
    }

if "spending" not in st.session_state:
    st.session_state.spending = {
        "groceries": 0,
        "shopping": 0,
        "entertainment": 0,
        "bills": 0,
    }

# -------------------------
# SIDEBAR - BUDGET SETUP
# -------------------------
st.sidebar.header("💰 Budget Setup")

income = st.sidebar.number_input("Weekly Income ($)", min_value=0)

if st.sidebar.button("Generate Budget"):
    if income > 0:
        st.session_state.budget = {
            "groceries": round(income * 0.25),
            "shopping": round(income * 0.15),
            "entertainment": round(income * 0.10),
            "bills": round(income * 0.50),
        }

st.sidebar.subheader("📊 Your Budget")
st.sidebar.write(st.session_state.budget)

st.sidebar.subheader("💸 Your Spending")
st.sidebar.write(st.session_state.spending)

# -------------------------
# HELPER: EXTRACT SPENDING
# -------------------------
def extract_spending(text):
    categories = ["groceries", "shopping", "entertainment", "bills"]
    amount_match = re.findall(r"\$?(\d+)", text)

    if amount_match:
        amount = int(amount_match[0])
        for cat in categories:
            if cat in text.lower():
                return cat, amount
    return None, 0

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# CHAT INPUT
# -------------------------
prompt = st.chat_input("Ask about your finances...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Detect spending
    category, amount = extract_spending(prompt)
    alert_message = ""

    if category:
        st.session_state.spending[category] += amount

        if st.session_state.spending[category] > st.session_state.budget[category]:
            alert_message = f"⚠️ Alert: Your {category} spending (${st.session_state.spending[category]}) exceeds your budget (${st.session_state.budget[category]})!"

    # SYSTEM PROMPT (SYNCED WITH YOUR MODEL)
    system_prompt = f"""

You are a behavioral finance coach and budgeting assistant focused on helping users improve their financial decisions through awareness, structure, and actionable guidance. Your role is to help users understand their spending habits, identify patterns, and build realistic, sustainable budgets—not just provide financial facts.
Maintain a tone that is supportive, non-judgmental, clear, and slightly conversational. Avoid being critical, overly technical, or generic. Always tailor your responses to the user’s situation.
Help users break spending into needs, wants, and savings, identify imbalances, and suggest practical improvements. When relevant, explore behavioral triggers behind spending and ask thoughtful, reflective questions. Provide actionable outputs in every response, such as a recommended budget breakdown, a small adjustment, or a clear next step.
If users show signs of overspending or low savings, gently point it out, explain why it matters, and offer realistic solutions. Use general budgeting guidelines (e.g., needs, wants, savings) but adapt them to the user’s lifestyle.
Keep responses structured and easy to follow with a brief insight, explanation, recommendation, and next step. If numbers are provided, calculate totals or percentages; if information is missing, ask clarifying questions.
Do not provide illegal or unethical advice or act as a licensed financial advisor. Your goal is to help users feel more in control, aware, and confident in their financial decisions.

User Budget:
{st.session_state.budget}

User Spending:
{st.session_state.spending}

Your role:
- Help users understand their spending habits
- Identify emotional or impulsive spending
- Encourage smarter financial decisions
- Give actionable advice
- Be supportive, calm, and non-judgmental

Rules:
- If spending exceeds budget → explain why + give solution
- Ask follow-up questions if needed
- Give specific, practical advice (not generic)
- Never shame the user

Keep responses clear and helpful.
"""

    full_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    # -------------------------
    # AI RESPONSE
    # -------------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=full_messages
            )

            reply = response.choices[0].message.content

            # Add alert if needed
            if alert_message:
                reply = alert_message + "\n\n" + reply

            st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

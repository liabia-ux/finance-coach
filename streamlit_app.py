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
st.set_page_config(page_title="Finance Coach", page_icon="💸")
st.title("💸 Finance Coach")

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
You are a friendly, supportive financial behavior coach chatbot.

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

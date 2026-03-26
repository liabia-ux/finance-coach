import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Finance Coach",
    page_icon="💸",
    layout="centered"
)

# ---------------- TOP TITLE ----------------
st.markdown("""
<style>

/* WealthWell Title */
.wealth-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #5c4033, #c8a27a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: 0.5px;
}

/* Subtitle */
.wealth-subtitle {
    text-align: center;
    font-size: 1rem;
    color: #7a5c4d;
    margin-bottom: 1.5rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="wealth-title">WealthWell</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="wealth-subtitle">Build better money habits. Feel in control of your finances.</div>',
    unsafe_allow_html=True
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(180deg, #fffaf6 0%, #f7efe8 100%);
}

/* Section label */
.sample-label {
    font-weight: 600;
    color: #6b4f3b;
    margin-top: 1rem;
    margin-bottom: 0.6rem;
}

/* Style all Streamlit buttons like bubbles */
div.stButton > button {
    width: 100%;
    border-radius: 999px;
    padding: 0.7rem 1rem;
    border: 1px solid rgba(107, 79, 59, 0.28);
    background: rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(8px);
    color: #5f4637;
    font-size: 0.95rem;
    font-weight: 500;
    box-shadow: 0 4px 14px rgba(92, 64, 51, 0.06);
    transition: all 0.22s ease;
}

div.stButton > button:hover {
    border: 1px solid rgba(107, 79, 59, 0.55);
    background: rgba(107, 79, 59, 0.08);
    color: #4d372b;
    transform: translateY(-2px);
}

div.stButton > button:active {
    transform: scale(0.98);
}

/* Chat input */
[data-testid="stChatInput"] {
    margin-top: 1rem;
}

/* Container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Chat text */
[data-testid="stChatMessage"],
[data-testid="stChatMessageContent"],
[data-testid="stMarkdownContainer"] p {
    color: #2b2b2b !important;
}

/* Budget tool styling */
div[data-testid="stExpander"] {
    border: 1px solid rgba(107, 79, 59, 0.18);
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.35);
    backdrop-filter: blur(8px);
    overflow: hidden;
    margin-bottom: 1rem;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.35);
    border: 1px solid rgba(107, 79, 59, 0.15);
    padding: 12px;
    border-radius: 16px;
}

/* Reflection card */
.reflection-card {
    background: rgba(255, 255, 255, 0.45);
    border: 1px solid rgba(107, 79, 59, 0.14);
    border-radius: 18px;
    padding: 14px 14px 10px 14px;
    margin-top: 1rem;
    color: #5f4637;
}

.reflection-title {
    font-weight: 700;
    margin-bottom: 0.35rem;
    color: #5c4033;
}

.reflection-text {
    font-size: 0.93rem;
    line-height: 1.45;
    color: #6a5347;
}

.small-note {
    font-size: 0.86rem;
    color: #7a6254;
    margin-top: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="wealth-subtitle">Your judgment-free space for smarter money habits.</div>',
    unsafe_allow_html=True
)

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SYSTEM PROMPT ----------------
THERAPY_SYSTEM_PROMPT = (
    "You are WealthWell, a warm and supportive financial wellness chatbot with a financial therapy-inspired tone. "
    "You help users with budgeting, saving, spending habits, emotional spending, financial stress, and money organization. "
    "You are calm, natural, conversational, and non-judgmental. "
    "Do not sound robotic, overly therapeutic, overly intense, or emotionally heavy unless the user is clearly expressing a money-related struggle. "
    "If the user sends a simple greeting like 'hi', 'hello', or 'hey', respond briefly and naturally like a normal human assistant. "
    "Do not start analyzing their emotions, patterns, or financial behavior unless they actually bring up a financial concern or ask for help. "
    "If the user asks for budgeting or money help, respond with empathy, practical guidance, and gentle reflection when appropriate. "
    "Only validate emotions when emotions are actually present in the user's message. "
    "Do not force emotional interpretation onto neutral messages. "
    "If budget fields are empty or zero, do not make assumptions about the user's life or financial state. "
    "You may acknowledge that no budget has been entered yet, but keep it light and practical. "
    "When the user is discussing real financial stress, overspending, avoidance, guilt, or anxiety, respond supportively: "
    "first acknowledge, then gently identify patterns, then offer small realistic next steps. "
    "Do not give legal, tax, or investment advice. "
    "Keep answers concise, natural, and human."
)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": THERAPY_SYSTEM_PROMPT}
    ]

if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None

if "user_budget" not in st.session_state:
    st.session_state.user_budget = {
        "income": 0,
        "rent": 0,
        "groceries": 0,
        "transportation": 0,
        "savings": 0,
        "dining_out": 0,
        "entertainment": 0,
        "other": 0,
    }

if "money_mood" not in st.session_state:
    st.session_state.money_mood = "Neutral"

if "reflection_note" not in st.session_state:
    st.session_state.reflection_note = ""

# ---------------- CALLBACK ----------------
def set_prompt(question: str) -> None:
    st.session_state.selected_prompt = question

# ---------------- HELPER FUNCTIONS ----------------
def is_simple_greeting(text: str) -> bool:
    cleaned = text.strip().lower()
    simple_greetings = {
        "hi", "hello", "hey", "hey there", "hi there",
        "good morning", "good afternoon", "good evening", "yo"
    }
    return cleaned in simple_greetings

def build_budget_context(budget_data: dict) -> str:
    total_spending = (
        budget_data["rent"]
        + budget_data["groceries"]
        + budget_data["transportation"]
        + budget_data["savings"]
        + budget_data["dining_out"]
        + budget_data["entertainment"]
        + budget_data["other"]
    )
    remaining_amount = budget_data["income"] - total_spending

    all_zero = (
        budget_data["income"] == 0
        and budget_data["rent"] == 0
        and budget_data["groceries"] == 0
        and budget_data["transportation"] == 0
        and budget_data["savings"] == 0
        and budget_data["dining_out"] == 0
        and budget_data["entertainment"] == 0
        and budget_data["other"] == 0
    )

    if all_zero:
        return (
            "\n\nUser budget context:\n"
            "- No budget data has been entered yet.\n"
            "Do not infer emotional meaning from this. "
            "Only mention it if relevant."
        )

    return (
        "\n\nUser budget context:\n"
        f"- Monthly income: ${budget_data['income']}\n"
        f"- Rent: ${budget_data['rent']}\n"
        f"- Groceries: ${budget_data['groceries']}\n"
        f"- Transportation: ${budget_data['transportation']}\n"
        f"- Savings: ${budget_data['savings']}\n"
        f"- Dining out: ${budget_data['dining_out']}\n"
        f"- Entertainment: ${budget_data['entertainment']}\n"
        f"- Other: ${budget_data['other']}\n"
        f"- Total planned monthly outflow: ${total_spending}\n"
        f"- Remaining amount: ${remaining_amount}\n"
        "Use this only when relevant."
    )

def budget_summary_values(budget_data: dict):
    total = (
        budget_data["rent"]
        + budget_data["groceries"]
        + budget_data["transportation"]
        + budget_data["savings"]
        + budget_data["dining_out"]
        + budget_data["entertainment"]
        + budget_data["other"]
    )
    remaining = budget_data["income"] - total
    return total, remaining

def get_reflection_text(remaining: int | float) -> str:
    if st.session_state.user_budget["income"] == 0:
        return (
            "No budget has been added yet. That is completely okay — this can just be a starting point whenever you're ready."
        )
    if remaining < 0:
        return (
            "Your current plan is going over your income. That does not mean you failed — it just means your budget may need a few adjustments."
        )
    if remaining == 0:
        return (
            "Your budget is currently balanced to your income. That can be a really useful starting point for getting clarity."
        )
    return (
        "You currently have money left after your planned spending, which can give you room for savings, flexibility, or a buffer."
    )

# ---------------- SIDEBAR BUDGET TOOL ----------------
with st.sidebar:
    st.markdown("### 💰 Budget Planner")

    with st.expander("Set your monthly budget", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            income = st.number_input(
                "Income",
                min_value=0,
                step=50,
                value=st.session_state.user_budget["income"]
            )
            rent = st.number_input(
                "Rent",
                min_value=0,
                step=50,
                value=st.session_state.user_budget["rent"]
            )
            groceries = st.number_input(
                "Groceries",
                min_value=0,
                step=25,
                value=st.session_state.user_budget["groceries"]
            )
            transportation = st.number_input(
                "Transport",
                min_value=0,
                step=25,
                value=st.session_state.user_budget["transportation"]
            )

        with col2:
            savings = st.number_input(
                "Savings",
                min_value=0,
                step=25,
                value=st.session_state.user_budget["savings"]
            )
            dining_out = st.number_input(
                "Dining",
                min_value=0,
                step=25,
                value=st.session_state.user_budget["dining_out"]
            )
            entertainment = st.number_input(
                "Fun",
                min_value=0,
                step=25,
                value=st.session_state.user_budget["entertainment"]
            )
            other = st.number_input(
                "Other",
                min_value=0,
                step=25,
                value=st.session_state.user_budget["other"]
            )

        if st.button("Save Budget"):
            st.session_state.user_budget = {
                "income": income,
                "rent": rent,
                "groceries": groceries,
                "transportation": transportation,
                "savings": savings,
                "dining_out": dining_out,
                "entertainment": entertainment,
                "other": other,
            }
            st.success("Saved")

    budget = st.session_state.user_budget
    total, remaining = budget_summary_values(budget)

    st.markdown("#### 📊 Snapshot")
    st.metric("Income", f"${budget['income']:,}")
    st.metric("Remaining", f"${remaining:,}")

    st.markdown("#### 🌿 Money Check-In")
    mood_options = ["Calm", "Anxious", "Overwhelmed", "Guilty", "Hopeful", "Avoiding it", "Neutral"]
    mood = st.selectbox(
        "How are you feeling about money today?",
        mood_options,
        index=mood_options.index(st.session_state.money_mood) if st.session_state.money_mood in mood_options else 6
    )
    st.session_state.money_mood = mood

    st.markdown(
        f"""
        <div class="reflection-card">
            <div class="reflection-title">Monthly reflection</div>
            <div class="reflection-text">{get_reflection_text(remaining)}</div>
            <div class="small-note">Current money mood: <strong>{st.session_state.money_mood}</strong></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    reflection_input = st.text_area(
        "Optional reflection",
        value=st.session_state.reflection_note,
        placeholder="Example: I spend more on takeout when I’m stressed.",
        height=100
    )
    st.session_state.reflection_note = reflection_input

# ---------------- CLICKABLE BUBBLES ----------------
st.markdown('<div class="sample-label">Try one of these</div>', unsafe_allow_html=True)

sample_questions = [
    "Help me create a simple monthly budget.",
    "Why do I keep impulse spending and how can I stop?",
    "I feel anxious every time I look at my bank account.",
    "Can you help me build a plan for when I want to stress spend?",
]

for i in range(0, len(sample_questions), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(sample_questions):
            with cols[j]:
                st.button(
                    sample_questions[i + j],
                    key=f"sample_q_{i+j}",
                    on_click=set_prompt,
                    args=(sample_questions[i + j],)
                )

# ---------------- DISPLAY CHAT HISTORY ----------------
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- INPUT LOGIC ----------------
typed_prompt = st.chat_input("Ask me about budgeting, saving, or spending habits...")

prompt = None
if st.session_state.selected_prompt:
    prompt = st.session_state.selected_prompt
    st.session_state.selected_prompt = None
elif typed_prompt:
    prompt = typed_prompt

# ---------------- RESPONSE LOGIC ----------------
if prompt:
    budget_context = build_budget_context(st.session_state.user_budget)

    emotion_context = (
        "\n\nUser emotional context:\n"
        f"- Current money mood: {st.session_state.money_mood}\n"
        f"- Reflection note: {st.session_state.reflection_note if st.session_state.reflection_note.strip() else 'No reflection provided.'}\n"
        "Use this emotional context only when the user's message is actually about money stress, guilt, avoidance, overspending, or emotional difficulty."
    )

    if is_simple_greeting(prompt):
        enriched_prompt = (
            f"{prompt}\n\n"
            "The user is only greeting you. "
            "Respond naturally, warmly, and briefly. "
            "Do not provide budgeting advice, emotional analysis, or financial therapy language unless the user asks for help."
        )
    else:
        enriched_prompt = (
            f"{prompt}\n\n"
            "Respond naturally and use good judgment. "
            "Only use a financial therapy style if the user is actually expressing a money problem, emotional stress, guilt, anxiety, avoidance, or overspending pattern. "
            "If the user is simply asking an informational budgeting question, be warm but straightforward. "
            "Do not overanalyze neutral messages. "
            "If useful, include one small next step. "
            f"{budget_context}"
            f"{emotion_context}"
        )

    st.session_state.messages.append({"role": "user", "content": enriched_prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.7,
                stream=True
            )

            def response_generator():
                full_text = ""
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_text += delta
                        yield delta

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_text}
                )

            st.write_stream(response_generator())

        except Exception as e:
            error_message = f"Something went wrong: {e}"
            st.error(error_message)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message}
            )

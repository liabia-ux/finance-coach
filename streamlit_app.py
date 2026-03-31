import time
import random
import re
import streamlit as st
from openai import OpenAI
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="WealthWell",
    page_icon="💸",
    layout="centered"
)

# ---------------- AUTO REFRESH FOR IDLE FOLLOW-UP ----------------
st_autorefresh(interval=15000, key="idle_refresh")

# ---------------- STYLES ----------------
st.markdown("""
<style>
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

.wealth-subtitle {
    text-align: center;
    font-size: 1rem;
    color: #7a5c4d;
    margin-bottom: 1.2rem;
}

.sample-label {
    font-weight: 600;
    color: #6b4f3b;
    margin-top: 1rem;
    margin-bottom: 0.6rem;
}

.stApp {
    background: linear-gradient(180deg, #fffaf6 0%, #f7efe8 100%);
}

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

[data-testid="stChatInput"] {
    margin-top: 1rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stChatMessage"],
[data-testid="stChatMessageContent"],
[data-testid="stMarkdownContainer"] p {
    color: #2b2b2b !important;
}

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

.followup-card {
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(107, 79, 59, 0.16);
    border-radius: 18px;
    padding: 14px;
    margin-top: 1rem;
    color: #5f4637;
}

section[data-testid="stSidebar"] {
    background: #232634 !important;
}

section[data-testid="stSidebar"] * {
    color: #f4eee7;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] span {
    color: #f4eee7 !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #0f1320 !important;
    color: #f4eee7 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}

section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] input {
    background-color: #0f1320 !important;
    color: #f4eee7 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}

section[data-testid="stSidebar"] textarea::placeholder,
section[data-testid="stSidebar"] input::placeholder {
    color: #c7beb5 !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextArea label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stExpander label {
    color: #f4eee7 !important;
    font-weight: 500;
}

section[data-testid="stSidebar"] .reflection-card {
    background: rgba(255, 255, 255, 0.82);
    color: #5f4637 !important;
}

section[data-testid="stSidebar"] .reflection-title {
    color: #5c4033 !important;
}

section[data-testid="stSidebar"] .reflection-text {
    color: #6a5347 !important;
}

section[data-testid="stSidebar"] .small-note {
    color: #7a6254 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="wealth-title">WealthWell</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="wealth-subtitle">Your judgment-free space for smarter money habits.</div>',
    unsafe_allow_html=True
)

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SYSTEM PROMPT ----------------
THERAPY_SYSTEM_PROMPT = """
You are WealthWell, a warm financial therapy and money support chatbot.

Your focus is:
- budgeting
- savings
- emotional spending
- stress spending
- impulse spending
- overspending
- money anxiety
- financial avoidance
- debt stress
- bill planning
- paycheck planning
- financial organization
- practical financial wellness support

Your tone should feel:
- warm
- calm
- emotionally safe
- natural
- conversational
- non-judgmental
- supportive without sounding clinical

Important behavior:
- Stay centered on money, spending, budgeting, debt, saving, and financial stress.
- Do not answer unrelated topics in depth.
- But do allow natural human conversation flow.
- If the user is clearly continuing a money-related conversation, respond naturally even if their message is short.
- Do not sound like a compliance bot.
- Do not overuse phrases like "I'm only here for..."
- If something is off-topic, gently redirect with warmth.
- If the user sounds emotional, acknowledge briefly in human language.
- Ask at most one follow-up question.
- Keep replies concise to medium length.
- Do not overanalyze simple messages.
- Do not give legal, tax, or investment advice.
"""

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

if "last_assistant_time" not in st.session_state:
    st.session_state.last_assistant_time = None

if "last_user_time" not in st.session_state:
    st.session_state.last_user_time = None

if "idle_followup_sent_for_turn" not in st.session_state:
    st.session_state.idle_followup_sent_for_turn = -1

if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = {
        "last_topic": "",
        "support_style": "balanced",
        "user_state": "neutral",
        "recent_concern": "",
        "spending_trigger": "",
        "goal": "",
        "last_response_mode": ""
    }

# ---------------- CALLBACK ----------------
def set_prompt(question: str) -> None:
    st.session_state.selected_prompt = question

# ---------------- CLASSIFIERS ----------------
FINANCE_KEYWORDS = [
    "money", "finance", "financial", "budget", "budgeting", "save", "saving",
    "savings", "spend", "spending", "overspending", "impulse spending",
    "stress spending", "debt", "loan", "credit", "credit card", "bill",
    "bills", "income", "expenses", "expense", "rent", "groceries",
    "transportation", "emergency fund", "paycheck", "paycheck to paycheck",
    "bank account", "banking", "afford", "payment", "payments", "cash flow",
    "money anxiety", "financial stress", "money habits", "financial goals",
    "shopping", "takeout", "impulse buy", "financial plan", "financial wellness"
]

OFF_TOPIC_PATTERNS = [
    r"\bweather\b",
    r"\bmovie\b",
    r"\bmovies\b",
    r"\bcelebrity\b",
    r"\bsports\b",
    r"\bpolitics\b",
    r"\belection\b",
    r"\brecipe\b",
    r"\bcoding\b",
    r"\bprogramming\b",
    r"\bpython code\b",
    r"\btravel\b",
    r"\bvacation\b",
    r"\bgame\b",
    r"\bgames\b",
    r"\bhistory\b",
    r"\bscience\b"
]

EMOTION_WORDS = [
    "anxious", "anxiety", "overwhelmed", "stressed", "stress", "guilty",
    "ashamed", "worried", "avoiding", "avoid", "behind", "struggling",
    "panic", "scared", "afraid", "embarrassed"
]

SHORT_CONFIRMATIONS = {
    "yes", "yeah", "yep", "yup", "sure", "okay", "ok", "yes please",
    "please", "sounds good", "let's do it", "lets do it", "i do", "i am"
}

def is_simple_greeting(text: str) -> bool:
    cleaned = text.strip().lower()
    greetings = {
        "hi", "hello", "hey", "hey there", "hi there",
        "good morning", "good afternoon", "good evening"
    }
    return cleaned in greetings

def recent_conversation_is_money_related() -> bool:
    recent_messages = st.session_state.messages[-6:]
    combined = " ".join(msg["content"].lower() for msg in recent_messages if msg["role"] != "system")
    return any(word in combined for word in FINANCE_KEYWORDS) or any(word in combined for word in EMOTION_WORDS)

def last_assistant_message() -> str:
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "assistant":
            return msg["content"].lower()
    return ""

def is_short_continuation(text: str) -> bool:
    lower = text.strip().lower()
    if lower in SHORT_CONFIRMATIONS:
        return True
    if len(lower.split()) <= 4 and recent_conversation_is_money_related():
        return True
    return False

def classify_scope(text: str) -> str:
    lower = text.strip().lower()

    if is_simple_greeting(lower):
        return "greeting"

    if any(re.search(pattern, lower) for pattern in OFF_TOPIC_PATTERNS):
        return "off_topic"

    if any(word in lower for word in FINANCE_KEYWORDS):
        return "finance"

    if any(word in lower for word in EMOTION_WORDS):
        if recent_conversation_is_money_related():
            return "finance"
        return "unclear_emotional"

    if is_short_continuation(lower):
        return "finance"

    if recent_conversation_is_money_related() and len(lower.split()) <= 12:
        return "finance"

    return "unclear"

def soft_redirect_response(user_text: str) -> str:
    lower = user_text.lower().strip()

    if any(word in lower for word in EMOTION_WORDS):
        return (
            "I may not be the best for that exact topic, but if this connects to money stress, spending, "
            "or feeling overwhelmed financially, I’m here with you. What’s been going on?"
        )

    return (
        "I might not be the best for that exact topic, but if it connects back to money, budgeting, "
        "spending, debt, or financial stress, I’d love to help. What part feels most tied to money?"
    )

def expand_short_followup(prompt: str) -> str:
    lower = prompt.strip().lower()
    last_assistant = last_assistant_message()

    if lower in SHORT_CONFIRMATIONS:
        if "budget" in last_assistant:
            return (
                "The user agreed to continue with the budget conversation. "
                "Respond naturally and warmly. "
                "Do not redirect. "
                "Move forward with one simple budgeting step."
            )
        return (
            "The user gave a short confirmation in an ongoing money-related conversation. "
            "Respond naturally, continue the thread, and do not restart the conversation."
        )

    return prompt

# ---------------- BUDGET HELPERS ----------------
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

def build_budget_context(budget_data: dict) -> str:
    total_spending, remaining_amount = budget_summary_values(budget_data)

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
            "- Do not assume emotional meaning from that.\n"
            "- Mention this only if helpful."
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
        "- Use this lightly and only when relevant."
    )

def get_reflection_text(remaining: int | float) -> str:
    if st.session_state.user_budget["income"] == 0:
        return "No budget has been added yet. That is totally okay — you can start whenever you're ready."
    if remaining < 0:
        return "Your current plan is over your income, which just means the budget probably needs a few adjustments."
    if remaining == 0:
        return "Your budget is currently balanced to your income. That is a solid starting point."
    return "You currently have money left after your planned spending, which can give you a little flexibility or buffer."

def get_idle_followup() -> str:
    options = [
        "No rush — we can keep this really simple and just start with income and essentials.",
        "Take your time. We can do this one small step at a time.",
        "No pressure. Want to start with just your monthly income and main bills?",
        "We can make this easy together — income first, then essentials, then everything else."
    ]
    return random.choice(options)

# ---------------- MEMORY ----------------
def classify_response_mode(text: str) -> str:
    lower = text.lower().strip()

    if is_simple_greeting(lower):
        return "greeting"

    if any(word in lower for word in EMOTION_WORDS):
        return "reflective"

    if any(word in lower for word in ["budget", "plan", "organize", "breakdown", "how much should"]):
        return "planning"

    if any(phrase in lower for phrase in ["how do i", "what should i", "can you help", "why do i"]):
        return "direct"

    if len(lower.split()) <= 6:
        return "gentle_followup"

    return "balanced"

def detect_topic(text: str) -> str:
    lower = text.lower()
    if any(k in lower for k in ["budget", "monthly budget", "categories", "income", "expenses", "expense"]):
        return "budgeting"
    if any(k in lower for k in ["impulse", "stress spend", "overspend", "shopping", "takeout"]):
        return "spending habits"
    if any(k in lower for k in ["anxious", "avoid", "bank account", "guilty", "overwhelmed", "stress"]):
        return "money stress"
    if any(k in lower for k in ["save", "saving", "emergency fund"]):
        return "saving"
    if any(k in lower for k in ["debt", "credit card", "loan", "bills"]):
        return "debt"
    return "general financial support"

def extract_trigger(text: str) -> str:
    lower = text.lower()
    trigger_patterns = [
        r"when i[' ]?m ([a-z\s]+)",
        r"i spend more when i[' ]?m ([a-z\s]+)",
        r"i overspend when i[' ]?m ([a-z\s]+)",
        r"when i feel ([a-z\s]+)"
    ]
    for pattern in trigger_patterns:
        match = re.search(pattern, lower)
        if match:
            return match.group(1).strip(" .,!?")
    return ""

def update_memory_from_user_input(prompt: str):
    memory = st.session_state.conversation_memory
    mode = classify_response_mode(prompt)
    topic = detect_topic(prompt)
    trigger = extract_trigger(prompt)

    memory["last_topic"] = topic
    memory["last_response_mode"] = mode

    if mode == "reflective":
        memory["user_state"] = "emotional"
        memory["support_style"] = "reflective"
    elif mode in ["planning", "direct"]:
        memory["user_state"] = "planning"
        memory["support_style"] = "practical"
    else:
        memory["user_state"] = "neutral"
        memory["support_style"] = "balanced"

    if trigger:
        memory["spending_trigger"] = trigger

    lower = prompt.lower()
    if any(k in lower for k in ["save more", "saving", "emergency fund"]):
        memory["goal"] = "build savings"
    elif "budget" in lower:
        memory["goal"] = "create a workable budget"
    elif any(k in lower for k in ["impulse", "overspend", "stress spend"]):
        memory["goal"] = "reduce reactive spending"
    elif any(k in lower for k in ["debt", "credit card", "loan", "bills"]):
        memory["goal"] = "reduce financial pressure"

    if len(prompt.strip()) > 8:
        memory["recent_concern"] = prompt.strip()

def build_memory_context() -> str:
    memory = st.session_state.conversation_memory
    return (
        "\n\nConversation memory:\n"
        f"- Last topic: {memory['last_topic'] or 'None yet'}\n"
        f"- Support style to favor: {memory['support_style']}\n"
        f"- User state: {memory['user_state']}\n"
        f"- Recent concern: {memory['recent_concern'] or 'None yet'}\n"
        f"- Known spending trigger: {memory['spending_trigger'] or 'None noted'}\n"
        f"- Current goal: {memory['goal'] or 'Not yet clear'}\n"
        "- Use this lightly for continuity.\n"
        "- Do not sound repetitive."
    )

def build_response_structure_instruction(prompt: str) -> str:
    mode = classify_response_mode(prompt)

    if mode == "greeting":
        return (
            "\n\nResponse structure:\n"
            "- Respond briefly and warmly.\n"
            "- Do not jump into advice.\n"
            "- Invite them in naturally."
        )

    if mode == "reflective":
        return (
            "\n\nResponse structure:\n"
            "- Start with a short human acknowledgment.\n"
            "- Briefly reflect the money feeling.\n"
            "- Offer one small next step or ask one gentle question.\n"
            "- Keep it grounded."
        )

    if mode == "planning":
        return (
            "\n\nResponse structure:\n"
            "- Be warm and practical.\n"
            "- Give one simple step first.\n"
            "- End with one small question."
        )

    if mode == "direct":
        return (
            "\n\nResponse structure:\n"
            "- Answer the money question directly.\n"
            "- Keep the tone soft and human.\n"
            "- Add one useful practical suggestion."
        )

    if mode == "gentle_followup":
        return (
            "\n\nResponse structure:\n"
            "- Continue the conversation naturally.\n"
            "- Do not restart the topic.\n"
            "- Keep it short and warm."
        )

    return (
        "\n\nResponse structure:\n"
        "- Be conversational.\n"
        "- Use a brief acknowledgment, brief guidance, then one next step.\n"
        "- Avoid sounding robotic."
    )

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 💰 Budget Planner")

    with st.expander("Set your monthly budget", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            income = st.number_input("Income", min_value=0, step=50, value=st.session_state.user_budget["income"])
            rent = st.number_input("Rent", min_value=0, step=50, value=st.session_state.user_budget["rent"])
            groceries = st.number_input("Groceries", min_value=0, step=25, value=st.session_state.user_budget["groceries"])
            transportation = st.number_input("Transport", min_value=0, step=25, value=st.session_state.user_budget["transportation"])

        with col2:
            savings = st.number_input("Savings", min_value=0, step=25, value=st.session_state.user_budget["savings"])
            dining_out = st.number_input("Dining", min_value=0, step=25, value=st.session_state.user_budget["dining_out"])
            entertainment = st.number_input("Fun", min_value=0, step=25, value=st.session_state.user_budget["entertainment"])
            other = st.number_input("Other", min_value=0, step=25, value=st.session_state.user_budget["other"])

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

    reflection_input = st.text_area(
        "Optional reflection",
        value=st.session_state.reflection_note,
        placeholder="Example: I spend more on takeout when I’m stressed.",
        height=100
    )
    st.session_state.reflection_note = reflection_input

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

# ---------------- EXAMPLE BUBBLES ----------------
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

# ---------------- SHOW CHAT HISTORY ----------------
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- IDLE FOLLOW-UP ----------------
assistant_count = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
user_count = sum(1 for m in st.session_state.messages if m["role"] == "user")

if (
    st.session_state.last_assistant_time is not None
    and assistant_count > 0
    and assistant_count > st.session_state.idle_followup_sent_for_turn
):
    seconds_since_assistant = time.time() - st.session_state.last_assistant_time
    user_has_not_replied_yet = user_count < assistant_count

    if seconds_since_assistant >= 45 and user_has_not_replied_yet:
        followup_text = get_idle_followup()
        with st.chat_message("assistant"):
            st.markdown(followup_text)
        st.session_state.messages.append({"role": "assistant", "content": followup_text})
        st.session_state.last_assistant_time = time.time()
        st.session_state.idle_followup_sent_for_turn = assistant_count

# ---------------- INPUT ----------------
typed_prompt = st.chat_input("What’s on your mind about money right now?")

prompt = None
if st.session_state.selected_prompt:
    prompt = st.session_state.selected_prompt
    st.session_state.selected_prompt = None
elif typed_prompt:
    prompt = typed_prompt

# ---------------- RESPONSE ENGINE ----------------
if prompt:
    st.session_state.last_user_time = time.time()

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    scope = classify_scope(prompt)
    prompt_for_model = expand_short_followup(prompt)

    if scope == "off_topic":
        blocked_response = soft_redirect_response(prompt)

        with st.chat_message("assistant"):
            st.markdown(blocked_response)

        st.session_state.messages.append({"role": "assistant", "content": blocked_response})
        st.session_state.last_assistant_time = time.time()
        st.stop()

    if scope == "unclear":
        gentle_response = (
            "I’m here for money-related support, budgeting, spending, and financial stress. "
            "What’s been feeling hardest for you financially lately?"
        )

        with st.chat_message("assistant"):
            st.markdown(gentle_response)

        st.session_state.messages.append({"role": "assistant", "content": gentle_response})
        st.session_state.last_assistant_time = time.time()
        st.stop()

    update_memory_from_user_input(prompt)

    budget_context = build_budget_context(st.session_state.user_budget)
    emotion_context = (
        "\n\nUser emotional context:\n"
        f"- Current money mood: {st.session_state.money_mood}\n"
        f"- Reflection note: {st.session_state.reflection_note if st.session_state.reflection_note.strip() else 'No reflection provided.'}\n"
        "- Use this only when genuinely relevant."
    )
    memory_context = build_memory_context()
    structure_instruction = build_response_structure_instruction(prompt)

    if scope == "greeting":
        enriched_prompt = (
            f"{prompt_for_model}\n\n"
            "The user is greeting you. "
            "Respond warmly and naturally. "
            "Do not jump into analysis or advice. "
            "A light invitation to share what is going on with money is enough."
            f"{memory_context}"
            f"{structure_instruction}"
        )
    elif scope == "unclear_emotional":
        enriched_prompt = (
            f"{prompt_for_model}\n\n"
            "The user sounds emotional, but the money connection is not fully explicit yet. "
            "Respond warmly and gently. "
            "Do not shut them down. "
            "Briefly acknowledge the feeling and softly ask whether this has been coming up around money, spending, or financial stress."
            f"{memory_context}"
            f"{structure_instruction}"
        )
    else:
        enriched_prompt = (
            f"{prompt_for_model}\n\n"
            "Stay focused on financial topics, but allow natural conversation flow. "
            "If the user is continuing a money-related conversation, respond naturally without redirecting. "
            "If the user expresses money anxiety, guilt, shame, avoidance, or stress, acknowledge it briefly in plain human language. "
            "If they want practical help, give one clear step first instead of too much at once. "
            "Keep the response concise to medium length. "
            "Ask at most one follow-up question. "
            "Do not sound robotic or overly scripted."
            f"{budget_context}"
            f"{emotion_context}"
            f"{memory_context}"
            f"{structure_instruction}"
        )

    temp_messages = st.session_state.messages.copy()
    temp_messages[-1] = {"role": "user", "content": enriched_prompt}

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=temp_messages,
                temperature=0.7,
                stream=True
            )

            full_text_parts = []

            def response_generator():
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_text_parts.append(delta)
                        yield delta

            st.write_stream(response_generator())

            full_text = "".join(full_text_parts).strip()

            st.session_state.messages.append(
                {"role": "assistant", "content": full_text}
            )
            st.session_state.last_assistant_time = time.time()

        except Exception as e:
            error_message = f"Something went wrong: {e}"
            st.error(error_message)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message}
            )
            st.session_state.last_assistant_time = time.time()

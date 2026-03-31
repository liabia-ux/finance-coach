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

# ---------------- TOP TITLE + STYLES ----------------
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

/* -------- SIDEBAR FIXES -------- */
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
You are WealthWell, a financial therapy bot.

Your role is strictly limited to helping with:
- budgeting
- saving
- overspending
- impulse spending
- stress spending
- emotional spending
- money anxiety
- financial avoidance
- debt stress
- paycheck planning
- expense planning
- financial goal setting
- money habits
- financial organization
- financial wellness support

You must ONLY respond to topics directly related to personal finance, money behavior, or financial therapy.

Do NOT answer questions about:
- coding
- schoolwork unrelated to finance
- relationships unless directly tied to money
- health or mental health outside financial stress
- entertainment
- current events
- politics
- sports
- history
- technology unrelated to finance
- travel
- recipes
- general trivia
- any topic outside money or financial therapy

If the user asks something outside your scope:
- do not answer the off-topic question
- briefly and warmly redirect toward money-related support
- if the user sounds emotionally overwhelmed, gently ask whether it is about money

Tone:
- warm
- calm
- grounded
- human
- conversational
- non-judgmental

Behavior rules:
- do not sound robotic
- do not overanalyze neutral messages
- do not force emotional meaning onto simple messages
- if the user sounds emotional, acknowledge briefly, reflect simply, and ask at most one gentle follow-up question
- if the user asks for direct financial help, answer clearly and practically
- keep responses concise to medium length
- avoid long monologues unless the user asks for more
- do not give legal, tax, or investment advice
- in each reply, anchor to the user's most recent message
- if the user is reacting to a prior suggestion, address that reaction before offering anything new
- do not repeat the same advice with slightly different wording
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

# ---------------- FINANCE LOCK ----------------
FINANCE_KEYWORDS = [
    "money", "finance", "financial", "budget", "budgeting", "save", "saving",
    "savings", "spend", "spending", "overspending", "impulse spending",
    "stress spending", "debt", "loan", "credit", "credit card", "bill",
    "bills", "income", "expenses", "expense", "rent", "groceries",
    "transportation", "emergency fund", "paycheck", "paycheck to paycheck",
    "bank account", "banking", "afford", "affordable", "payment", "payments",
    "cash flow", "financial stress", "money anxiety", "money habits",
    "financial goals", "save more", "spend less", "shopping", "takeout",
    "overspend", "impulse buy", "financial plan", "financial wellness"
]

FINANCE_THERAPY_PHRASES = [
    "i feel anxious when i check my account",
    "i keep impulse buying",
    "i overspend",
    "i stress spend",
    "i avoid checking my bank account",
    "i feel guilty after spending",
    "help me make a plan",
    "help me make a budget",
    "i spend too much",
    "i feel bad about money",
    "i'm behind on bills",
    "i am behind on bills",
    "i keep spending when i'm stressed",
    "why do i spend when i'm stressed",
    "why do i keep spending"
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
    r"\brelationship\b",
    r"\bdating\b",
    r"\bmedical\b",
    r"\bdiagnosis\b",
    r"\bessay\b",
    r"\bhomework\b",
    r"\bpython code\b",
    r"\bcoding\b",
    r"\bprogramming\b",
    r"\bhistory\b",
    r"\bscience\b",
    r"\btravel\b",
    r"\bvacation\b",
    r"\bgame\b",
    r"\bgames\b"
]

SOFT_EMOTION_WORDS = [
    "overwhelmed", "stressed", "anxious", "worried", "guilty",
    "ashamed", "lost", "confused", "behind", "struggling", "panic"
]

SHORT_CONFIRMATIONS = {
    "yes", "yeah", "yep", "yup", "sure", "it is", "kind of", "a little",
    "i am", "i do", "okay", "ok", "yes please", "sounds good", "please"
}

def is_simple_greeting(text: str) -> bool:
    cleaned = text.strip().lower()
    greetings = {
        "hi", "hello", "hey", "hey there", "hi there",
        "good morning", "good afternoon", "good evening", "yo"
    }
    return cleaned in greetings

def last_assistant_asked_money_redirect() -> bool:
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "assistant":
            content = msg["content"].lower()
            trigger_phrases = [
                "is there a money-related part of this for you",
                "are you feeling overwhelmed about money",
                "if this ties into money",
                "i’m here specifically for financial therapy and money-related support",
                "i'm here specifically for financial therapy and money-related support"
            ]
            return any(phrase in content for phrase in trigger_phrases)
    return False

def recent_conversation_is_money_related() -> bool:
    recent_messages = st.session_state.messages[-6:]
    combined = " ".join(msg["content"].lower() for msg in recent_messages if msg["role"] != "system")
    return any(word in combined for word in FINANCE_KEYWORDS) or any(word in combined for word in SOFT_EMOTION_WORDS)

def is_followup_confirmation(text: str) -> bool:
    cleaned = text.strip().lower()
    return cleaned in SHORT_CONFIRMATIONS

def is_short_continuation(text: str) -> bool:
    lower = text.strip().lower()
    if lower in SHORT_CONFIRMATIONS:
        return True
    if len(lower.split()) <= 5 and recent_conversation_is_money_related():
        return True
    return False

def is_finance_related(text: str) -> bool:
    lower = text.lower().strip()

    if is_simple_greeting(lower):
        return True

    if last_assistant_asked_money_redirect() and is_followup_confirmation(lower):
        return True

    if is_short_continuation(lower) and recent_conversation_is_money_related():
        return True

    keyword_hit = any(word in lower for word in FINANCE_KEYWORDS)
    phrase_hit = any(phrase in lower for phrase in FINANCE_THERAPY_PHRASES)
    off_topic_hit = any(re.search(pattern, lower) for pattern in OFF_TOPIC_PATTERNS)

    if keyword_hit or phrase_hit:
        return True

    if off_topic_hit:
        return False

    if any(word in lower for word in SOFT_EMOTION_WORDS) and recent_conversation_is_money_related():
        return True

    return False

def off_topic_response(user_text: str) -> str:
    lower = user_text.lower().strip()

    if any(word in lower for word in SOFT_EMOTION_WORDS):
        return (
            "I might not be the best for that exact topic, but if this connects to money stress, "
            "spending, or financial pressure, I’m here with you. What’s been going on?"
        )

    return (
        "I might not be the best for that exact topic, but if this ties into money, budgeting, "
        "spending, debt, or financial stress, I’d be glad to help. What part feels most connected to money?"
    )

def expand_short_followup(prompt: str) -> str:
    lower = prompt.strip().lower()

    if last_assistant_asked_money_redirect() and is_followup_confirmation(lower):
        return (
            "The user confirmed that this does relate to money. "
            "Respond warmly and naturally. "
            "Do not repeat the redirect. "
            "Ask one gentle, specific follow-up question to help them open up about what is going on financially."
        )

    if lower in {"no", "not really", "nope"} and last_assistant_asked_money_redirect():
        return (
            "The user said this is not about money. "
            "Briefly and kindly explain that you can only help with financial therapy and money-related support."
        )

    if is_short_continuation(lower) and recent_conversation_is_money_related():
        return (
            "The user gave a short continuation in an ongoing money-related conversation. "
            "Respond naturally and continue the thread without restarting it."
        )

    return prompt

def user_is_still_distressed(text: str) -> bool:
    lower = text.lower().strip()
    distress_patterns = [
        "still stressed",
        "still anxious",
        "still overwhelmed",
        "still worried",
        "but i'm still",
        "but im still",
        "i'm still stressed",
        "im still stressed",
        "i'm still anxious",
        "im still anxious",
        "still really stressed",
        "still feel stressed",
        "still feel anxious"
    ]
    return any(p in lower for p in distress_patterns)

# ---------------- HELPERS ----------------
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
            "Do not infer emotional meaning from this. Mention it only if relevant."
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
        "No rush — would it help if we kept it really simple and just started with income and essentials?",
        "Take your time. We can break this into one small step if that feels easier.",
        "You do not need to figure it all out at once. Want to start with just a basic monthly budget?",
        "If it helps, we can make this super simple together — income, bills, savings, then spending."
    ]
    return random.choice(options)

def build_recent_flow_context() -> str:
    recent = st.session_state.messages[-4:]
    visible = [m for m in recent if m["role"] != "system"]

    if not visible:
        return "\n\nRecent flow context:\n- No prior conversation yet."

    formatted = []
    for msg in visible:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted.append(f"- {role}: {msg['content']}")

    return (
        "\n\nRecent flow context:\n"
        + "\n".join(formatted)
        + "\nUse this to continue the emotional and conversational thread naturally."
        + "\nPay close attention to how the user is responding to the assistant’s last suggestion."
        + "\nIf the user is hesitant, overwhelmed, or says the suggestion does not solve the feeling, do not just offer another generic step."
    )

# ---------------- RESPONSE STRUCTURE + MEMORY ----------------
def classify_response_mode(text: str) -> str:
    lower = text.lower().strip()

    if is_simple_greeting(lower):
        return "greeting"

    emotional_words = [
        "anxious", "anxiety", "guilty", "ashamed", "overwhelmed", "stress",
        "stressed", "avoid", "avoiding", "scared", "afraid", "regret",
        "panic", "bad with money", "embarrassed", "impulse", "overspend"
    ]
    planning_words = [
        "budget", "plan", "help me create", "help me build", "monthly budget",
        "set up", "organize", "breakdown", "categories", "how much should"
    ]
    direct_question_words = [
        "how do i", "what should i", "can you help", "what is", "why do i"
    ]

    if any(word in lower for word in emotional_words):
        return "reflective"
    if any(word in lower for word in planning_words):
        return "planning"
    if any(word in lower for word in direct_question_words):
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
        "Use this lightly to keep continuity. "
        "Only reference earlier details when it feels natural and helpful."
    )

def build_response_structure_instruction(prompt: str) -> str:
    mode = classify_response_mode(prompt)

    if mode == "greeting":
        return (
            "\n\nResponse structure:\n"
            "- Respond briefly and warmly.\n"
            "- Do not give advice yet.\n"
            "- Do not analyze emotions or patterns."
        )

    if mode == "reflective":
        return (
            "\n\nResponse structure:\n"
            "- Start with a short human acknowledgment.\n"
            "- Respond directly to the user's most recent emotional shift or reaction.\n"
            "- If they are reacting to a prior suggestion, address that reaction before offering anything new.\n"
            "- Do not repeat the same type of advice in slightly different wording.\n"
            "- Only offer a next step if it feels earned."
        )

    if mode == "planning":
        return (
            "\n\nResponse structure:\n"
            "- Start warm but concise.\n"
            "- Give a simple practical step or framework.\n"
            "- End with one small question to tailor the next response.\n"
            "- Keep it clear and not too long."
        )

    if mode == "direct":
        return (
            "\n\nResponse structure:\n"
            "- Answer the finance question directly.\n"
            "- Keep the tone warm and human.\n"
            "- Add one small practical suggestion if useful.\n"
            "- Avoid over-reflecting."
        )

    if mode == "gentle_followup":
        return (
            "\n\nResponse structure:\n"
            "- Be supportive and simple.\n"
            "- Continue the thread naturally.\n"
            "- Do not restart the topic.\n"
            "- Ask one clarifying question only if needed."
        )

    return (
        "\n\nResponse structure:\n"
        "- Be conversational and steady.\n"
        "- Use brief acknowledgment, brief guidance, then one small next step.\n"
        "- Do not turn the reply into a lecture."
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

# ---------------- RESPONSE LOGIC ----------------
if prompt:
    st.session_state.last_user_time = time.time()

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt_for_model = expand_short_followup(prompt)

    if not is_finance_related(prompt):
        blocked_response = off_topic_response(prompt)

        with st.chat_message("assistant"):
            st.markdown(blocked_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": blocked_response}
        )
        st.session_state.last_assistant_time = time.time()
        st.stop()

    update_memory_from_user_input(prompt)

    budget_context = build_budget_context(st.session_state.user_budget)
    recent_flow_context = build_recent_flow_context()

    emotion_context = (
        "\n\nUser emotional context:\n"
        f"- Current money mood: {st.session_state.money_mood}\n"
        f"- Reflection note: {st.session_state.reflection_note if st.session_state.reflection_note.strip() else 'No reflection provided.'}\n"
        "Use this only when the user's message is actually about money stress, guilt, avoidance, overspending, or emotional difficulty."
    )

    memory_context = build_memory_context()
    structure_instruction = build_response_structure_instruction(prompt)

    extra_flow_instruction = ""
    if user_is_still_distressed(prompt):
        extra_flow_instruction = (
            "\n\nSpecial flow instruction:\n"
            "- The user is saying the previous step does not fully reduce the stress.\n"
            "- Do not simply give another generic budgeting task.\n"
            "- First acknowledge that doing the task and still feeling stressed can both be true.\n"
            "- Stay with that tension for a moment.\n"
            "- Then offer one gentler next step only if it fits."
        )

    if is_simple_greeting(prompt):
        enriched_prompt = (
            f"{prompt_for_model}\n\n"
            "The user is only greeting you. Respond warmly, naturally, and briefly. "
            "Do not provide financial advice or emotional analysis unless they ask for money help."
            f"{memory_context}"
            f"{structure_instruction}"
        )
    else:
        enriched_prompt = (
            f"{prompt_for_model}\n\n"
            "Only respond if the user's message is related to finance, money behavior, budgeting, spending, saving, debt, bills, or financial stress. "
            "If the message is vague and emotional, gently connect it back to money instead of answering unrelated topics. "
            "Respond naturally and conversationally. "
            "Keep the response fairly short to medium length. "
            "Only use a financial therapy style if the user is actually expressing a money problem, emotional stress, guilt, anxiety, avoidance, or overspending pattern. "
            "If the user is asking a straightforward budgeting or financial planning question, be warm but direct. "
            "Do not overanalyze neutral messages. "
            "If useful, include one small next step. "
            "Ask at most one follow-up question."
            f"{budget_context}"
            f"{emotion_context}"
            f"{memory_context}"
            f"{recent_flow_context}"
            f"{extra_flow_instruction}"
            f"{structure_instruction}"
        )

    # IMPORTANT: keep the real user message intact and add instructions separately
    temp_messages = st.session_state.messages.copy()
    temp_messages.append({"role": "system", "content": enriched_prompt})

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=temp_messages,
                temperature=0.55,
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

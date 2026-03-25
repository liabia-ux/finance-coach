import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Finance Coach",
    page_icon="💸",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(180deg, #fffaf6 0%, #f7efe8 100%);
}

/* Title area */
.main-title {
    font-size: 2.3rem;
    font-weight: 700;
    color: #5c4033;
    margin-bottom: 0.2rem;
}

.sub-title {
    color: #7a5c4d;
    font-size: 1rem;
    margin-bottom: 1.2rem;
}

/* Section label */
.sample-label {
    font-weight: 600;
    color: #6b4f3b;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
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

/* Optional container softness */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Fix chat text color */
[data-testid="stChatMessage"] {
    color: #2b2b2b !important;
}

/* Force markdown text inside chat */
[data-testid="stMarkdownContainer"] p {
    color: #2b2b2b !important;
}

/* User + assistant text specifically */
[data-testid="stChatMessageContent"] {
    color: #2b2b2b !important;
}

/* Optional: make assistant slightly darker */
[data-testid="stChatMessage"][aria-label="assistant"] {
    color: #1f1f1f !important;
}

/* Optional: make user text slightly different tone */
[data-testid="stChatMessage"][aria-label="user"] {
    color: #3a3a3a !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">💸 Finance Coach</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Your judgment-free space to improve budgeting, spending, and saving habits.</div>',
    unsafe_allow_html=True
)

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are Finance Coach, a supportive financial wellness chatbot. "
                "Help users with budgeting, spending habits, savings strategies, and money organization. "
                "Be warm, practical, encouraging, and non-judgmental. "
                "Do not give legal, tax, or investment advice. "
                "When useful, offer realistic budget breakdowns across categories like rent, groceries, "
                "transportation, debt payments, savings, dining out, and entertainment. "
                "Keep responses clear and easy to follow."
            )
        }
    ]

if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = None


# ---------------- CALLBACK ----------------
def set_prompt(question: str) -> None:
    st.session_state.selected_prompt = question


# ---------------- SAMPLE QUESTIONS ----------------
st.markdown('<div class="sample-label">Sample questions</div>', unsafe_allow_html=True)

sample_questions = [
    "How do I start budgeting if I’ve never made one before?",
    "Help me create a simple monthly budget.",
    "Why do I keep impulse spending and how can I stop?",
    "What percentage of my income should go to rent?",
    "How should I divide my money between needs, wants, and savings?",
    "Can you help me figure out a grocery budget?",
]

# Display in rows of 2
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
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.7,
            )

            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_reply}
            )

        except Exception as e:
            error_message = f"Something went wrong: {e}"
            st.error(error_message)
            st.session_state.messages.append(
                {"role": "assistant", "content": error_message}
            )

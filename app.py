
import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Word Puzzle Game",
    page_icon="🧩",
    layout="centered"
)

# Custom CSS and HTML
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #FFD166;
}

.subtitle {
    text-align: center;
    color: #E0E0E0;
    font-size: 18px;
}

.puzzle-box {
    background-color: #304766;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin: 20px 0;
    border: 2px solid #FFD166;
}

.scrambled {
    font-size: 38px;
    font-weight: bold;
    letter-spacing: 12px;
    color: #FFD166;
}

.score-box {
    background-color: #304766;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    font-size: 20px;
}

.stButton button {
    background-color: #FFD166;
    color: #141E30;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    width: 100%;
}

.stButton button:hover {
    background-color: #F4A261;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# Word database
words = {
    "Easy": {
        "APPLE": "A fruit that can be red or green.",
        "HOUSE": "A place where people live.",
        "TIGER": "A large animal with orange and black stripes.",
        "PLANT": "A living thing that grows in soil.",
        "BREAD": "A food commonly made from flour."
    },

    "Medium": {
        "PLANET": "A celestial body that orbits a star.",
        "JUNGLE": "A dense tropical forest.",
        "PYTHON": "A popular programming language.",
        "PUZZLE": "A game that tests your thinking skills.",
        "GUITAR": "A musical instrument with strings."
    },

    "Hard": {
        "ASTRONOMY": "The scientific study of space.",
        "ADVENTURE": "An exciting or unusual experience.",
        "KNOWLEDGE": "Information and understanding gained through learning.",
        "CHOCOLATE": "A sweet treat made from cocoa.",
        "EDUCATION": "The process of learning and gaining knowledge."
    }
}


# Game functions
def scramble_word(word):
    letters = list(word)
    scrambled = word

    while scrambled == word:
        random.shuffle(letters)
        scrambled = "".join(letters)

    return scrambled


def new_word():
    difficulty = st.session_state.difficulty
    word = random.choice(list(words[difficulty].keys()))

    st.session_state.word = word
    st.session_state.scrambled = scramble_word(word)
    st.session_state.hint = words[difficulty][word]
    st.session_state.attempted = False
    st.session_state.message = ""


# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"

if "word" not in st.session_state:
    st.session_state.word = ""

if "attempted" not in st.session_state:
    st.session_state.attempted = False

if "message" not in st.session_state:
    st.session_state.message = ""

if "rounds" not in st.session_state:
    st.session_state.rounds = 0


# Header
st.markdown(
    '<div class="title">🧩 WORD PUZZLE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Unscramble the letters and discover the hidden word!</div>',
    unsafe_allow_html=True
)

st.write("")


# Difficulty selection
difficulty = st.selectbox(
    "Choose Difficulty:",
    ["Easy", "Medium", "Hard"]
)

if difficulty != st.session_state.difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.score = 0
    st.session_state.rounds = 0
    new_word()


# Start first word
if not st.session_state.word:
    new_word()


# Score display
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f'<div class="score-box">🏆 Score: {st.session_state.score}</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="score-box">📝 Rounds: {st.session_state.rounds}</div>',
        unsafe_allow_html=True
    )


# Puzzle display
st.markdown(f"""
<div class="puzzle-box">
    <h3>Unscramble This Word!</h3>
    <div class="scrambled">
        {st.session_state.scrambled}
    </div>
    <p>Can you figure out the correct word?</p>
</div>
""", unsafe_allow_html=True)


# Hint
with st.expander("💡 Show Hint"):
    st.info(st.session_state.hint)


# Answer input
answer = st.text_input(
    "Enter your answer:",
    placeholder="Type your word here...",
    disabled=st.session_state.attempted
)


# Check answer
if st.button("Check Answer", disabled=st.session_state.attempted):

    if answer.strip().upper() == st.session_state.word:
        st.session_state.score += 10
        st.session_state.rounds += 1
        st.session_state.message = "🎉 Correct! Excellent work!"
        st.session_state.attempted = True

    else:
        st.session_state.message = "❌ Not quite! Try again."
    
    st.rerun()


# Feedback
if st.session_state.message:
    if "Correct" in st.session_state.message:
        st.success(st.session_state.message)
    else:
        st.error(st.session_state.message)


# Next word
if st.session_state.attempted:
    if st.button("➡️ Next Word"):
        new_word()
        st.rerun()


# Restart
st.divider()

if st.button("🔄 Restart Game"):
    st.session_state.score = 0
    st.session_state.rounds = 0
    new_word()
    st.rerun()


# Footer HTML
st.markdown("""
<hr>
<div style="text-align:center; color:#BBBBBB;">
    <p>🧩 Word Puzzle Game</p>
    <p>Challenge your brain and have fun learning!</p>
</div>
""", unsafe_allow_html=True)

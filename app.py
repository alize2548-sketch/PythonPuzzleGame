

import streamlit as st
import random

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Word Puzzle Game",
    page_icon="🧩",
    layout="centered"
)

# -----------------------------
# CUSTOM HTML AND CSS
# -----------------------------
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


# -----------------------------
# WORD DATABASE: 20 EACH
# -----------------------------
words = {
    "Easy": {
        "APPLE": "A fruit that can be red or green.",
        "HOUSE": "A place where people live.",
        "TIGER": "A large animal with orange and black stripes.",
        "PLANT": "A living thing that grows in soil.",
        "BREAD": "A food commonly made from flour.",
        "CHAIR": "Something you sit on.",
        "WATER": "A liquid essential for life.",
        "TABLE": "Furniture used for eating or working.",
        "SMILE": "An expression that shows happiness.",
        "CLOUD": "A white or grey shape in the sky.",
        "MUSIC": "Sounds arranged to create a melody.",
        "BEACH": "A sandy area beside the sea.",
        "HAPPY": "A feeling of joy.",
        "GRAPE": "A small fruit that grows in bunches.",
        "HORSE": "An animal that people can ride.",
        "TRAIN": "A vehicle that travels on railway tracks.",
        "PHONE": "A device used for communication.",
        "RIVER": "A natural flowing body of water.",
        "LIGHT": "Something that helps us see.",
        "FLOWER": "A colourful part of a plant."
    },

    "Medium": {
        "PLANET": "A celestial body that orbits a star.",
        "JUNGLE": "A dense tropical forest.",
        "PYTHON": "A popular programming language.",
        "PUZZLE": "A game that tests your thinking skills.",
        "GUITAR": "A musical instrument with strings.",
        "BRIDGE": "A structure built over water or roads.",
        "ROCKET": "A vehicle used for space travel.",
        "CASTLE": "A large historic fortified building.",
        "ORANGE": "A citrus fruit.",
        "SILVER": "A shiny precious metal.",
        "FOREST": "A large area covered with trees.",
        "CAMERA": "A device used to take photographs.",
        "DOCTOR": "A person who treats sick people.",
        "LIBRARY": "A place where books can be borrowed.",
        "JOURNEY": "An act of travelling from one place to another.",
        "DIAMOND": "A very hard precious gemstone.",
        "WHISPER": "To speak very quietly.",
        "COMPASS": "A tool used to find directions.",
        "VOLCANO": "An opening in Earth's crust that can release lava.",
        "MACHINE": "A device that performs a particular task."
    },

    "Hard": {
        "ASTRONOMY": "The scientific study of space.",
        "ADVENTURE": "An exciting or unusual experience.",
        "KNOWLEDGE": "Information gained through learning.",
        "CHOCOLATE": "A sweet treat made from cocoa.",
        "EDUCATION": "The process of learning.",
        "DISCOVERY": "Finding something new.",
        "TECHNOLOGY": "The use of scientific knowledge for practical purposes.",
        "PHILOSOPHY": "The study of fundamental questions about existence.",
        "ENVIRONMENT": "The natural world around us.",
        "INTELLIGENCE": "The ability to learn and understand.",
        "CELEBRATION": "An event that marks a special occasion.",
        "ARCHITECTURE": "The art and design of buildings.",
        "EXPERIMENT": "A scientific test to discover something.",
        "CURIOSITY": "A strong desire to learn or know something.",
        "COMMUNICATION": "The exchange of information.",
        "RESPONSIBILITY": "Being accountable for something.",
        "INDEPENDENCE": "The state of being free from outside control.",
        "TRANSLATION": "Changing text from one language to another.",
        "MATHEMATICS": "The study of numbers and calculations.",
        "CONSTELLATION": "A group of stars forming a pattern."
    }
}


# -----------------------------
# GAME FUNCTIONS
# -----------------------------

def scramble_word(word):
    letters = list(word)
    scrambled = word

    while scrambled == word:
        random.shuffle(letters)
        scrambled = "".join(letters)

    return scrambled


def setup_deck():
    """Create a shuffled list of unused words."""
    st.session_state.word_deck = list(
        words[st.session_state.difficulty].keys()
    )
    random.shuffle(st.session_state.word_deck)


def new_word():
    """Select the next unused word."""
    if not st.session_state.word_deck:
        st.session_state.word = None
        return

    word = st.session_state.word_deck.pop(0)

    st.session_state.word = word
    st.session_state.scrambled = scramble_word(word)
    st.session_state.hint = words[
        st.session_state.difficulty
    ][word]

    st.session_state.attempted = False
    st.session_state.message = ""
    st.session_state.round_id += 1


# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "rounds" not in st.session_state:
    st.session_state.rounds = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"

if "word_deck" not in st.session_state:
    st.session_state.word_deck = []

if "word" not in st.session_state:
    st.session_state.word = None

if "attempted" not in st.session_state:
    st.session_state.attempted = False

if "message" not in st.session_state:
    st.session_state.message = ""

if "round_id" not in st.session_state:
    st.session_state.round_id = 0


# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="title">🧩 WORD PUZZLE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Unscramble the letters and discover the hidden word!'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# -----------------------------
# DIFFICULTY SELECTION
# -----------------------------

difficulty = st.selectbox(
    "Choose Difficulty:",
    ["Easy", "Medium", "Hard"]
)

# Reset game when difficulty changes
if difficulty != st.session_state.difficulty:

    st.session_state.difficulty = difficulty
    st.session_state.score = 0
    st.session_state.rounds = 0

    setup_deck()
    new_word()

# Initialize the first word
if not st.session_state.word_deck and st.session_state.word is None:
    setup_deck()

if st.session_state.word is None:
    new_word()


# -----------------------------
# SCORE AND PROGRESS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="score-box">🏆 Score: '
        f'{st.session_state.score}</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="score-box">📝 Completed: '
        f'{st.session_state.rounds}</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="score-box">📚 Remaining: '
        f'{len(st.session_state.word_deck)}</div>',
        unsafe_allow_html=True
    )

st.progress(
    st.session_state.rounds % 20 / 20
)


# -----------------------------
# PUZZLE DISPLAY
# -----------------------------

if st.session_state.word is not None:

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
        disabled=st.session_state.attempted,
        key=f"answer_{st.session_state.round_id}"
    )

    # Check answer
    if st.button(
        "Check Answer",
        disabled=st.session_state.attempted
    ):

        if answer.strip().upper() == st.session_state.word:

            st.session_state.score += 10
            st.session_state.rounds += 1
            st.session_state.message = (
                "🎉 Correct! Excellent work!"
            )
            st.session_state.attempted = True

        else:
            st.session_state.message = (
                "❌ Not quite! Try again."
            )

        st.rerun()


# -----------------------------
# FEEDBACK
# -----------------------------

if st.session_state.message:

    if "Correct" in st.session_state.message:
        st.success(st.session_state.message)
    else:
        st.error(st.session_state.message)


# -----------------------------
# NEXT WORD / NEW SET
# -----------------------------

if st.session_state.attempted:

    if st.session_state.word_deck:

        if st.button("➡️ Next Word"):
            new_word()
            st.rerun()

    else:

        st.success(
            "🏆 Congratulations! You have completed "
            "all 20 words in this difficulty!"
        )

        if st.button("🔄 Start Another Set"):

            setup_deck()
            new_word()
            st.rerun()


# -----------------------------
# RESTART GAME
# -----------------------------

st.divider()

if st.button("🔄 Restart Game"):

    st.session_state.score = 0
    st.session_state.rounds = 0

    setup_deck()
    new_word()

    st.rerun()


# -----------------------------
# FOOTER HTML
# -----------------------------

st.markdown("""
<hr>

<div style="text-align:center; color:#BBBBBB;">
    <h4>🧩 Word Puzzle Game</h4>
    <p>Challenge your brain and have fun learning!</p>
    <p>60 words available across 3 difficulty levels.</p>
</div>
""", unsafe_allow_html=True)


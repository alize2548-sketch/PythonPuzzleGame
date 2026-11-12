
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
    padding: 15px 5px;
    border-radius: 12px;
    text-align: center;
    font-size: 17px;
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
# WORD DATABASE (20 EACH)
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
# SESSION STATE INITIALIZATION
# -----------------------------
defaults = {
    "score": 0,
    "rounds": 0,
    "difficulty": "Easy",
    "word_deck": [],
    "word": None,
    "scrambled": "",
    "hint": "",
    "attempted": False,
    "message": "",
    "round_id": 0,
    "review_queue": [],
    "current_is_review": False,
    "base_words_seen": 0,
    "game_complete": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------
# GAME FUNCTIONS
# -----------------------------
def scramble_word(word):
    letters = list(word)
    shuffled = letters[:]

    while shuffled == letters:
        random.shuffle(shuffled)

    return "".join(shuffled)


def setup_deck():
    """Create a shuffled list of words."""

    st.session_state.word_deck = list(
        words[st.session_state.difficulty].keys()
    )

    random.shuffle(st.session_state.word_deck)


def age_review_queue():
    """Count one completed normal word toward review."""

    for item in st.session_state.review_queue:
        item["wait"] -= 1


def add_to_review(word):
    """Schedule an incorrect or skipped word for review."""

    st.session_state.review_queue.append({
        "word": word,
        "wait": 5
    })


def new_word():
    """Choose a review word or a new normal word."""

    ready_words = [
        item for item in st.session_state.review_queue
        if item["wait"] <= 0
    ]

    if ready_words:

        item = ready_words[0]

        st.session_state.word = item["word"]

        st.session_state.review_queue.remove(item)

        st.session_state.current_is_review = True

    elif st.session_state.word_deck:

        word = st.session_state.word_deck.pop(0)

        st.session_state.word = word

        st.session_state.current_is_review = False

        st.session_state.base_words_seen += 1

    elif st.session_state.review_queue:

        # Finish remaining review words when normal words run out.
        item = st.session_state.review_queue.pop(0)

        st.session_state.word = item["word"]

        st.session_state.current_is_review = True

    else:

        st.session_state.word = None

        st.session_state.game_complete = True

        return

    word = st.session_state.word

    st.session_state.scrambled = scramble_word(word)

    st.session_state.hint = words[
        st.session_state.difficulty
    ][word]

    st.session_state.attempted = False

    st.session_state.message = ""

    st.session_state.round_id += 1


def reset_game(difficulty):
    """Reset the game."""

    st.session_state.difficulty = difficulty

    st.session_state.score = 0

    st.session_state.rounds = 0

    st.session_state.review_queue = []

    st.session_state.word = None

    st.session_state.attempted = False

    st.session_state.message = ""

    st.session_state.base_words_seen = 0

    st.session_state.game_complete = False

    setup_deck()

    new_word()


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
    ["Easy", "Medium", "Hard"],
    key="difficulty_selector"
)

if difficulty != st.session_state.difficulty:
    reset_game(difficulty)


# -----------------------------
# START FIRST WORD
# -----------------------------
if (
    st.session_state.word is None
    and not st.session_state.game_complete
):

    if (
        not st.session_state.word_deck
        and not st.session_state.review_queue
    ):
        setup_deck()

    new_word()


# -----------------------------
# SCORE AND PROGRESS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<div class="score-box">🏆 Score<br>'
        f'<b>{st.session_state.score}</b></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<div class="score-box">📝 Correct<br>'
        f'<b>{st.session_state.rounds}</b></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<div class="score-box">📚 Remaining<br>'
        f'<b>{len(st.session_state.word_deck)}</b></div>',
        unsafe_allow_html=True
    )


# -----------------------------
# PROGRESS BAR
# -----------------------------
completed = st.session_state.base_words_seen

st.write("**Progress**")

st.progress(
    min(completed / 20, 1.0)
)

st.caption(
    f"{completed} out of 20 original words shown"
)


# -----------------------------
# REVIEW QUEUE COUNTER
# -----------------------------
if st.session_state.review_queue:

    st.info(
        f"🔁 Words waiting for another attempt: "
        f"{len(st.session_state.review_queue)}"
    )


# -----------------------------
# PUZZLE DISPLAY
# -----------------------------
if st.session_state.word is not None:

    if st.session_state.current_is_review:

        st.info("🔁 REVIEW WORD - Try again!")

    # HTML tags start at the left edge so Streamlit
    # displays them as HTML instead of a code block.
    st.markdown(
        f"""
<div class="puzzle-box">
<h3>Unscramble This Word!</h3>
<div class="scrambled">{st.session_state.scrambled}</div>
<p>Can you figure out the correct word?</p>
</div>
""",
        unsafe_allow_html=True
    )

    # HINT
    with st.expander("💡 Show Hint"):

        st.info(st.session_state.hint)


    # ANSWER INPUT
    answer = st.text_input(
        "Enter your answer:",
        placeholder="Type your word here...",
        disabled=st.session_state.attempted,
        key=f"answer_{st.session_state.round_id}"
    )


    # -----------------------------
    # CHECK ANSWER AND SKIP BUTTON
    # -----------------------------
    col1, col2 = st.columns(2)

    # CHECK ANSWER
    with col1:

        if st.button(
            "Check Answer",
            disabled=st.session_state.attempted
        ):

            current_word = st.session_state.word

            if answer.strip().upper() == current_word:

                if not st.session_state.current_is_review:
                    age_review_queue()

                st.session_state.score += 10

                st.session_state.rounds += 1

                st.session_state.message = (
                    "🎉 Correct! Excellent work! +10 points"
                )

                st.session_state.attempted = True

            else:

                if not st.session_state.current_is_review:
                    age_review_queue()

                add_to_review(current_word)

                st.session_state.message = (
                    f"❌ Incorrect! The correct answer is "
                    f"{current_word}. "
                    "You can try it again after 5 other words!"
                )

                st.session_state.attempted = True

            st.rerun()


    # SKIP WORD
    with col2:

        if st.button(
            "⏭️ Skip Word",
            disabled=st.session_state.attempted
        ):

            current_word = st.session_state.word

            if not st.session_state.current_is_review:
                age_review_queue()

            add_to_review(current_word)

            st.session_state.message = (
                f"⏭️ Skipped! The correct answer is "
                f"{current_word}. "
                "This word will return after 5 other words!"
            )

            st.session_state.attempted = True

            st.rerun()


# -----------------------------
# FEEDBACK
# -----------------------------
if st.session_state.message:

    if "Correct!" in st.session_state.message:

        st.success(st.session_state.message)

    elif "Incorrect" in st.session_state.message:

        st.error(st.session_state.message)

    else:

        st.warning(st.session_state.message)


# -----------------------------
# NEXT WORD BUTTON
# -----------------------------
if st.session_state.attempted:

    if st.button("➡️ Next Word"):

        new_word()

        st.rerun()


# -----------------------------
# GAME COMPLETION
# -----------------------------
if st.session_state.game_complete:

    st.success(
        "🏆 Congratulations! You completed "
        "all 20 words and all review words!"
    )

    st.balloons()

    st.write(
        f"Your final score: {st.session_state.score}"
    )

    if st.button("🔄 Start Another Set"):

        st.session_state.score = 0

        st.session_state.rounds = 0

        st.session_state.review_queue = []

        st.session_state.word = None

        st.session_state.attempted = False

        st.session_state.message = ""

        st.session_state.base_words_seen = 0

        st.session_state.game_complete = False

        setup_deck()

        new_word()

        st.rerun()


# -----------------------------
# RESTART GAME
# -----------------------------
st.divider()

if st.button("🔄 Restart Game"):

    reset_game(st.session_state.difficulty)

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

<p>Keep practising and improve your vocabulary!</p>

</div>
""", unsafe_allow_html=True)


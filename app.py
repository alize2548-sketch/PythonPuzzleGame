    # -----------------------------
    # CHECK ANSWER AND SKIP BUTTON
    # -----------------------------
    col1, col2 = st.columns(2)

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
                    f"❌ Incorrect! The correct answer is {current_word}. "
                    "You can try it again after 5 other words!"
                )
                st.session_state.attempted = True

            st.rerun()

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
                f"⏭️ Skipped! The correct answer is {current_word}. "
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
    st.write(f"Your final score: {st.session_state.score}")

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


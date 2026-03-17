import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")
st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox(  
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty

if st.session_state.current_difficulty != difficulty:
    st.session_state.current_difficulty = difficulty
    # FIX: Reset game state for new difficulty
    st.session_state.secret = random.randint(low, high) # fxed: secret number was not resetting when difficulty changed
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = [] 

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. " #fixed bounds change when difficulty changes using copilot agent mode to refactor logic into logic_utils.py
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high) #fixed: secret number was not in bound of difficulty when new game clicked using copilot agent mode
    st.session_state.score = 0 #fixed: score was not resetting when new game clicked using copilot agent mode
    st.success("New game started.")
    st.session_state.status = "playing"
    st.session_state.history = []
    st.rerun()

if st.session_state.status != "playing": #FIXME: logic breaks here, hast to reset when new game  clicked
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret
        outcome_str = check_guess(guess_int, secret)

        if show_hint:
            if outcome_str == "Win":
                message = "🎉 Correct!"
            elif outcome_str == "Too High":
                message = "📉 Go LOWER!"
            else:
                message = "📈 Go HIGHER!"
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome_str,
            attempt_number=st.session_state.attempts,
        )

        if outcome_str == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            attempts_remaining_after = attempt_limit - st.session_state.attempts
            if attempts_remaining_after <= 0:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else: 
        st.error("Game over. Start a new game to try again.") 
    st.stop()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

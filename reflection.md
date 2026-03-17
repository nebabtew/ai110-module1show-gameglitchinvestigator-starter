# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
it ran well  okay
- List at least two concrete bugs you noticed at the start 

 Bug 1 — Secret number doesn't reset on difficulty change
Expected: Selecting a new difficulty should generate a fresh secret number within the new range. Actual: The secret number carries over from the previous difficulty, so it may fall outside the valid range entirely.

Bug 2 — Out-of-bounds guesses are accepted without feedback
Expected: If a player enters a number outside the allowed range, the game should reject it and display a warning. Actual: The game silently accepts the input and processes it as a normal guess.

Bug 3 — Hints reversed + string conversion
Expected: If the secret number is higher than the guess, the hint should say "Too Low" (and vice versa). Actual: The hints are flipped, telling the player to go in the wrong direction. They also contradict themselves across guesses.

Bug 4 — "Start New Game" button does not restart the game
Expected: Clicking the button should reset the score, attempts, and secret number to start fresh. Actual: The button does nothing, leaving the game in its current state.

Bug 5 — Displayed attempt count doesn't match the actual limit
Expected: The number of attempts shown to the player should match how many guesses they actually get. Actual: The two values are out of sync, so the player runs out of guesses unexpectedly.

Bug 6 — Answer is revealed one guess too early
Expected: The secret number should only be revealed after all attempts are exhausted. Actual: With one attempt remaining, the game spoils the answer prematurely.

Bug7 - string attempts will take attempts left into negative integer if kpt going

Bug8 : Info message hardcodes the range
It always says 1 and 100 regardless of difficulty. Easy uses 1–20, Hard uses 1–50, but the player is never told the correct range — it should use low and high.


(for example: "the secret number kept changing" or "the hints were backwards").

BUGS to fix this session bug 3 and 4 only!!!

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
   Copilot Agent Mode and Copilot Chat. and external claude ai for prompting and rephrasing

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
    When fixing the New Game button, the AI also flagged that the attempts display was inconsistent — the attempts used and attempts allowed weren't being shown together clearly. It suggested formatting it as {st.session_state.attempts}/{attempt_limit} so the player could see both numbers at once. I verified this by running the app and confirming the display updated correctly after each guess.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  At one point I was trying to fix the out-of-bounds input validation — the agent kept making edits to different lines but nothing changed in the running app. I kept undoing and reprompting with no result. Eventually I realized the agent was editing the wrong part of the code and the fix wasn't actually being applied anywhere meaningful. I decided to move on and focus on the hint mechanism instead, which was a more impactful fix.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
    The first and easiest method was trial and error — specifically testing the exact behavior I had just fixed. If I fixed the hints, I would guess a number I knew was too high and check that it said "Go LOWER."

- Describe at least one test you ran (manual or using pytest) 
    I used both manual testing and pytest. For manual testing I tried guesses on both sides of the secret number to verify hints, confirmed the New Game button fully reset status and score, and switched difficulties to confirm the range updated correctly. For pytest I used an external AI to help me write a detailed prompt describing which functions to test and which bugs to target, then pasted that prompt to the Copilot agent to generate the test cases. This gave me more targeted tests than just asking generically

- Did AI help you design or understand any tests? How?
    AI helped me generate pytest cases based on the bugs I fixed — for example, testing that check_guess(60, 50) returns "Too High" to verify the reversed hint fix. However, the AI falsely told me the tests passed before I even ran them. When I ran python -m pytest -v myself I got a ModuleNotFoundError — the tests had never actually executed. This taught me to always verify AI claims in the terminal instead of taking its word for it.


---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

- What change did you make that finally gave the game a stable secret number?

    Adding the difficulty change detection block that checks if st.session_state.current_difficulty != difficulty — this made sure the secret only regenerated when the difficulty actually changed, not on every rerun. The range also now correctly updates when switching difficulty.
    
- range should change when changing difficult

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

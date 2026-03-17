from logic_utils import check_guess, get_range_for_difficulty


def _outcome(result):
    # Some versions of check_guess may return a tuple (outcome, ...).
    # This helper normalizes to just the first element if so.
    if isinstance(result, tuple):
        return result[0]
    return result


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert _outcome(result) == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert _outcome(result) == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert _outcome(result) == "Too Low"


def test_get_range_for_difficulty_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_get_range_for_difficulty_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)

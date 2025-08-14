"""Utilities for working with i-radio fragments and flag values."""

from typing import Any
from ..models.fragment import Fragment


# Flag value constants
FLAG_CORRECT = 20  # Correct answer
FLAG_WRONG = 21  # Wrong answer
FLAG_EXPLANATION = 29  # Explanation shown after any answer is selected
FLAG_COMMENT = -1  # Non-interactive comment/explanation (always visible)


def is_correct_answer(radio_item: dict[str, Any]) -> bool:
    """Check if a radio item is marked as the correct answer.

    Args:
        radio_item: Dictionary containing radio button data with 'flag' key

    Returns:
        True if the flag indicates a correct answer (20)
    """
    return radio_item.get("flag") == FLAG_CORRECT


def is_wrong_answer(radio_item: dict[str, Any]) -> bool:
    """Check if a radio item is marked as a wrong answer.

    Args:
        radio_item: Dictionary containing radio button data with 'flag' key

    Returns:
        True if the flag indicates a wrong answer (21)
    """
    return radio_item.get("flag") == FLAG_WRONG


def is_interactive(radio_item: dict[str, Any]) -> bool:
    """Check if a radio item is interactive (not a comment or explanation).

    Args:
        radio_item: Dictionary containing radio button data with 'flag' key

    Returns:
        True if the item is interactive (flag != -1 and flag != 29)
    """
    flag = radio_item.get("flag", FLAG_COMMENT)
    return flag != FLAG_COMMENT and flag != FLAG_EXPLANATION


def is_explanation(radio_item: dict[str, Any]) -> bool:
    """Check if a radio item is an explanation (shown after any answer).

    Args:
        radio_item: Dictionary containing radio button data with 'flag' key

    Returns:
        True if the flag indicates an explanation (29)
    """
    return radio_item.get("flag") == FLAG_EXPLANATION


def get_correct_answers(fragment: Fragment) -> list[dict[str, Any]]:
    """Get all correct answer options from a radio fragment.

    Args:
        fragment: Fragment object of type 'radio_'

    Returns:
        List of radio items marked as correct answers
    """
    if fragment.f_type.value != "radio_":
        return []

    radios = fragment.data.get("radios", [])
    return [r for r in radios if is_correct_answer(r)]


def get_feedback_class(flag: int) -> str:
    """Get CSS class for feedback based on flag value.

    Args:
        flag: The flag value from the radio item

    Returns:
        CSS class string for styling feedback
    """
    if flag == FLAG_CORRECT:
        return "text-success"
    elif flag == FLAG_WRONG:
        return "text-error"
    elif flag == FLAG_EXPLANATION:
        return "text-info"
    elif flag == FLAG_COMMENT:
        return "text-base-content opacity-70"
    else:
        return "text-base-content"


def validate_radio_fragment(fragment: Fragment) -> tuple[bool, str]:
    """Validate that a radio fragment has proper structure.

    Args:
        fragment: Fragment object to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if fragment.f_type.value != "radio_":
        return False, "Fragment is not a radio type"

    radios = fragment.data.get("radios", [])

    if not radios:
        return False, "Radio fragment has no options"

    interactive_radios = [r for r in radios if is_interactive(r)]

    if not interactive_radios:
        return False, "Radio fragment has no interactive options"

    correct_answers = [r for r in interactive_radios if is_correct_answer(r)]

    if not correct_answers:
        return False, "Radio fragment has no correct answer marked"

    # Check for required keys in each radio
    required_keys = {"pos", "name", "flag", "html", "classes"}
    for radio in radios:
        if not all(key in radio for key in required_keys):
            return False, f"Radio item missing required keys: {required_keys - set(radio.keys())}"

    return True, ""


def create_radio_item(html: str, flag: int, pos: int = 0, classes: str = "") -> dict[str, Any]:
    """Create a properly formatted radio item dictionary.

    Args:
        html: The HTML content for the radio option
        flag: The flag value (20 for correct, 21 for wrong, -1 for comment)
        pos: Position in the list
        classes: Additional CSS classes

    Returns:
        Dictionary with radio item data
    """
    from ..services.fragment_builder import slugify

    return {"pos": pos, "name": slugify(html), "flag": flag, "html": html, "classes": classes}

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from dbdie_classes.base import Emoji


def emoji_len_func(emoji: Optional["Emoji"]) -> Optional["Emoji"]:
    """NOTE: We allow more than 1 character because of how len works for emojis."""
    if emoji is not None:
        emoji_len = len(emoji)
        assert emoji_len > 0, "Emoji can't be an empty string."
        assert emoji_len <= 4, "Emoji should be 1-character long."
    return emoji

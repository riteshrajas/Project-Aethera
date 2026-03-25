# Code for data analysis
import re
from collections import Counter
from typing import Dict, Union, Iterable

def analyze_text_frequency(
    text_input: Union[str, Iterable[str]],
    max_unique_words: int = 100000,
    max_word_length: int = 100
) -> Dict[str, int]:
    """
    Analyzes the frequency of words in a given text or iterable of text chunks.

    This function is optimized for memory usage. It uses `re.finditer` to avoid
    creating a list of all matches. It also accepts an iterable (like a file object)
    to process data chunk-by-chunk or line-by-line, allowing analysis of datasets
    larger than available memory.

    To prevent memory exhaustion (DoS), it limits the number of unique words
    and the maximum length of individual words.

    Args:
        text_input (Union[str, Iterable[str]]): The input text string or an iterable yielding strings.
        max_unique_words (int): The maximum number of unique words to store. Defaults to 100,000.
        max_word_length (int): The maximum length of a single word. Defaults to 100.

    Returns:
        Dict[str, int]: A dictionary mapping words to their frequency counts.
    """
    counter = Counter()

    # Compile regex for better performance if called many times
    word_pattern = re.compile(r'\b\w+\b')

    def update_counter(chunk: str):
        """Processes a chunk of text and updates the counter with limits."""
        for match in word_pattern.finditer(chunk):
            word = match.group().lower()
            if len(word) > max_word_length:
                word = word[:max_word_length]

            # Only add new words if we haven't reached the limit
            if word in counter or len(counter) < max_unique_words:
                counter[word] += 1

    if isinstance(text_input, str):
        if not text_input:
            return {}
        update_counter(text_input)
    else:
        # Assume iterable of strings (e.g., file object)
        for chunk in text_input:
            if chunk:
                update_counter(chunk)

    return dict(counter)

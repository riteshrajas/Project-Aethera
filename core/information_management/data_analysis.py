# Code for data analysis
import re
from collections import Counter
from typing import Dict, Union, Iterable

def analyze_text_frequency(text_input: Union[str, Iterable[str]]) -> Dict[str, int]:
    """
    Analyzes the frequency of words in a given text or iterable of text chunks.

    This function is optimized for memory usage. It uses `re.finditer` to avoid
    creating a list of all matches. It also accepts an iterable (like a file object)
    to process data chunk-by-chunk or line-by-line, allowing analysis of datasets
    larger than available memory.

    Args:
        text_input (Union[str, Iterable[str]]): The input text string or an iterable yielding strings.

    Returns:
        Dict[str, int]: A dictionary mapping words to their frequency counts.
    """
    counter = Counter()

    # Compile regex for better performance if called many times
    word_pattern = re.compile(r'\b\w+\b')

    def process_chunk(chunk: str):
        # Generator expression avoids creating a list of matches for the chunk
        return (match.group().lower() for match in word_pattern.finditer(chunk))

    if isinstance(text_input, str):
        if not text_input:
            return {}
        counter.update(process_chunk(text_input))
    else:
        # Assume iterable of strings (e.g., file object)
        for chunk in text_input:
            if chunk:
                counter.update(process_chunk(chunk))

    return dict(counter)

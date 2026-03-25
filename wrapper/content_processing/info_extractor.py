class InfoExtractor:
    """
    A class to extract information from text.
    """
    def extract_info(self, text, keywords):
        """
        Extracts sentences containing any of the keywords.

        Args:
            text (str): The source text to extract from.
            keywords (list): A list of keywords to search for.

        Returns:
            list: A list of sentences containing at least one of the keywords.
        """
        if not text or not keywords:
            return []

        # Pre-lowercase keywords for performance
        lowered_keywords = [kw.lower() for kw in keywords]

        # Split text into sentences (simple split by period)
        sentences = text.split('.')
        results = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Lowercase sentence once per iteration for performance
            lowered_sentence = sentence.lower()
            if any(keyword in lowered_sentence for keyword in lowered_keywords):
                results.append(sentence)
        return results

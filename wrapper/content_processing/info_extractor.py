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

        # Split text into sentences (simple split by period)
        sentences = text.split('.')
        results = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                results.append(sentence)
        return results

import unittest
from core.information_management.data_analysis import analyze_text_frequency

class TestDataAnalysisSecurity(unittest.TestCase):
    def test_max_unique_words_limit(self):
        # Generate 100 unique words
        def word_generator():
            for i in range(100):
                yield f"word{i} "

        # Limit to 10 unique words
        max_unique = 10
        result = analyze_text_frequency(word_generator(), max_unique_words=max_unique)

        self.assertEqual(len(result), max_unique)
        # Check that we have some of the first words
        self.assertIn('word0', result)
        self.assertIn('word9', result)
        # Check that we don't have words beyond the limit
        self.assertNotIn('word10', result)

    def test_max_unique_words_allows_existing(self):
        # Test that it still counts existing words even after limit is reached
        text = "word1 word2 word3 word1 word2 word1"
        # Limit to 2 unique words
        max_unique = 2
        result = analyze_text_frequency(text, max_unique_words=max_unique)

        self.assertEqual(len(result), max_unique)
        self.assertEqual(result['word1'], 3)
        self.assertEqual(result['word2'], 2)
        self.assertNotIn('word3', result)

    def test_max_word_length_limit(self):
        long_word = "a" * 200
        max_len = 50
        result = analyze_text_frequency(long_word, max_word_length=max_len)

        truncated_word = "a" * max_len
        self.assertIn(truncated_word, result)
        self.assertEqual(result[truncated_word], 1)
        self.assertEqual(len(list(result.keys())[0]), max_len)

    def test_default_limits(self):
        # Just ensure it works with defaults and handles a reasonable amount
        def word_generator():
            for i in range(1000):
                yield f"w{i} "

        result = analyze_text_frequency(word_generator())
        self.assertEqual(len(result), 1000)

if __name__ == '__main__':
    unittest.main()

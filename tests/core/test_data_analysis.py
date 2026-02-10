import unittest
import time
import sys
import re
from io import StringIO
from core.information_management.data_analysis import analyze_text_frequency

class TestDataAnalysis(unittest.TestCase):
    def test_analyze_text_frequency_basic(self):
        text = "Hello world! Hello everyone."
        expected = {'hello': 2, 'world': 1, 'everyone': 1}
        result = analyze_text_frequency(text)
        self.assertEqual(result, expected)

    def test_analyze_text_frequency_empty(self):
        text = ""
        expected = {}
        result = analyze_text_frequency(text)
        self.assertEqual(result, expected)

    def test_analyze_text_frequency_iterable(self):
        # Test with a list of chunks
        chunks = ["Apple ", "apple ", "APPLE"]
        expected = {'apple': 3}
        result = analyze_text_frequency(chunks)
        self.assertEqual(result, expected)

    def test_analyze_text_frequency_file_object(self):
        # Test with a file-like object
        text = "Line 1\nLine 2\nLine 1"
        f = StringIO(text)
        expected = {'line': 3, '1': 2, '2': 1}
        result = analyze_text_frequency(f)
        self.assertEqual(result, expected)

    def test_performance_benchmark(self):
        """
        Benchmarks the optimized function against a naive implementation.
        This is not a strict pass/fail test based on speed, but prints metrics.
        """
        # Generate a large text (~5MB)
        large_text = "word " * 1000000 + "unique " * 1000

        # Naive implementation using re.findall (loads all into list)
        start_naive = time.time()
        naive_counts = {}
        # Simulate naive approach: findall creates a list of all 1,001,000 words
        words = re.findall(r'\b\w+\b', large_text)
        for word in words:
            w = word.lower()
            naive_counts[w] = naive_counts.get(w, 0) + 1
        end_naive = time.time()
        duration_naive = end_naive - start_naive

        # Optimized implementation (using string)
        start_opt = time.time()
        opt_counts = analyze_text_frequency(large_text)
        end_opt = time.time()
        duration_opt = end_opt - start_opt

        print(f"\n[BENCHMARK] analyze_text_frequency vs Naive re.findall")
        print(f"Text size: {len(large_text)/1024/1024:.2f} MB")
        print(f"Naive time: {duration_naive:.4f}s")
        print(f"Optimized time: {duration_opt:.4f}s")
        if duration_opt > 0:
            print(f"Speedup: {duration_naive / duration_opt:.2f}x")
        else:
            print(f"Speedup: Infinite (too fast to measure)")

        # Ensure correctness
        self.assertEqual(opt_counts['word'], 1000000)
        self.assertEqual(opt_counts['unique'], 1000)

if __name__ == '__main__':
    unittest.main()

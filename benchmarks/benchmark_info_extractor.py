import time
import random
import string
from wrapper.content_processing.info_extractor import InfoExtractor

def generate_random_sentence(length=100):
    return ''.join(random.choices(string.ascii_letters + ' ', k=length))

def generate_data(num_sentences=5000, sentence_length=150, num_keywords=500):
    sentences = [generate_random_sentence(sentence_length) for _ in range(num_sentences)]
    text = '. '.join(sentences)
    keywords = [generate_random_sentence(random.randint(5, 15)).strip() for _ in range(num_keywords)]
    return text, keywords

def benchmark():
    text, keywords = generate_data()
    extractor = InfoExtractor()

    # Warm up
    extractor.extract_info(text, keywords)

    start_time = time.time()
    num_runs = 50
    for _ in range(num_runs):
        extractor.extract_info(text, keywords)
    end_time = time.time()

    print(f"Total time for {num_runs} runs: {end_time - start_time:.4f} seconds")
    print(f"Average time per run: {(end_time - start_time) / num_runs:.4f} seconds")

if __name__ == "__main__":
    benchmark()

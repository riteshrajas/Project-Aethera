# Main application entry point for Project Aethera
import sys
import os
from core.information_management.data_analysis import analyze_text_frequency

def main():
    print("Project Aethera Initializing...")

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            print(f"Analyzing {filepath}...")
            try:
                # pass file object directly to be memory efficient
                with open(filepath, 'r', encoding='utf-8') as f:
                    stats = analyze_text_frequency(f)

                print(f"Analysis complete. Found {len(stats)} unique words.")
                # print top 5 words
                top_5 = sorted(stats.items(), key=lambda item: item[1], reverse=True)[:5]
                print("Top 5 words:", top_5)
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            print(f"File not found: {filepath}")

    print("Project Aethera Active.")

if __name__ == "__main__":
    main()

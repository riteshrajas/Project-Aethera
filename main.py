# Main application entry point for Project Aethera
import sys
import subprocess

def run_web_client():
    print("Starting web client (python -m services.web_client)...")
    subprocess.run([sys.executable, "-m", "services.web_client"]) 

def run_tests():
    print("Running tests (pytest)...")
    subprocess.run([sys.executable, "-m", "pytest"]) 

def main():
    print("Project Aethera — Productive Starter")

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ("web", "webclient", "web_client"):
            run_web_client()
            return
        if cmd in ("test", "tests"):
            run_tests()
            return
        print(f"Unknown command: {cmd}")
        print("Available commands: web, tests")
        return

    # Interactive prompt for quick productivity actions
    while True:
        print("\nChoose an action:")
        print("1) Start web client")
        print("2) Run tests")
        print("3) Exit")
        choice = input("Select 1-3: ").strip()
        if choice == "1":
            run_web_client()
        elif choice == "2":
            run_tests()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

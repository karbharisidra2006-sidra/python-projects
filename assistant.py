import random
import datetime
import os

MEMORY_FILE = "memory.txt"

def load_memory():
    data = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    data[key] = value
    return data

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        for key, value in data.items():
            f.write(f"{key}:{value}\n")

memory = load_memory()

responses = {
    "hello": ["Hello!", "Hi!", "Hey there!"],
    "how are you": ["I am functioning well.", "All systems running."],
    "bye": ["Goodbye!", "See you!", "Take care!"]
}

def chatbot():
    print("Smart Assistant started. Type 'help' to see commands.")

    while True:
        user_input = input("You: ").lower()

        if user_input == "bye":
            print(random.choice(responses["bye"]))
            break

        elif "help" in user_input:
            print("""Commands:
- my name is ___
- hello
- time
- date
- calculate 2+2
- note: your note
- show notes
- bye
""")

        elif "my name is" in user_input:
            name = user_input.split("my name is")[-1].strip()
            memory["name"] = name
            save_memory(memory)
            print(f"Nice to meet you, {name.title()}!")

        elif "hello" in user_input:
            if "name" in memory:
                print(f"Hello {memory['name'].title()}!")
            else:
                print(random.choice(responses["hello"]))

        elif "time" in user_input:
            print(datetime.datetime.now().strftime("%H:%M:%S"))

        elif "date" in user_input:
            print(datetime.datetime.now().strftime("%d-%m-%Y"))

        elif "calculate" in user_input:
            try:
                expression = user_input.replace("calculate", "").strip()
                result = eval(expression)
                print(f"Result = {result}")
            except:
                print("Invalid calculation")

        elif "note:" in user_input:
            note = user_input.replace("note:", "").strip()
            with open("notes.txt", "a") as f:
                f.write(note + "\n")
            print("Note saved.")

        elif "show notes" in user_input:
            if os.path.exists("notes.txt"):
                with open("notes.txt", "r") as f:
                    print("Notes:\n" + f.read())
            else:
                print("No notes found.")

        else:
            print("Unknown command. Type 'help'.")

chatbot()
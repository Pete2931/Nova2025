key = input("What is your OpenRouter API key?: ")

with open("OPENROUTER_API_KEY.txt", 'w') as key_file:
    key_file.write(key)

print("Created 'OPENROUTER_API_KEY.txt'")

print("Checking .gitignore")

try:
    gitignore_file = open(".gitignore", 'r')
    gitignore_contents = gitignore_file.read()
    gitignore_file.close()

    if "OPENROUTER_API_KEY.txt" in gitignore_contents:
        print("'OPENROUTER_API_KEY.txt' is already in your .gitignore file. You're all set!")
        exit(0)
except FileNotFoundError:
    print(".gitignore file does not exist. Creating...")

with open(".gitignore", 'a') as gitignore_file:
    gitignore_file.write("\nOPENROUTER_API_KEY.txt\n")

print("'OPENROUTER_API_KEY.txt' added to .gitignore. You're all set!")

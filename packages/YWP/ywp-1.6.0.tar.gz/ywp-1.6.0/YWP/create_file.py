def create_file(name):

    print("Please enter the text or code (press Ctrl + D on Unix or Ctrl + Z then Enter on Windows to finish):")

    user_input_lines = []
    try:
        while True:
            line = input()
            user_input_lines.append(line)
    except EOFError:
        pass

    # Merge the entered lines into a single text
    user_input = '\n'.join(user_input_lines)

    # Write the entered text to the file
    filename = f"{name}.py"

    # Write the entered text to the file using Unicode encoding
    with open(filename, "w", encoding="utf-8") as file:
        file.write(user_input)

    return "created"
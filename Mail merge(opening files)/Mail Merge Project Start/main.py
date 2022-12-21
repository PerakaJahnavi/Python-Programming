PLACEHOLDER = "[name]"

with open("./Input/Names/invited_names.txt") as names_file:
    names = names_file.readlines()
    print(names)

with open("./Input/Letters/starting_letter.txt") as letters_file:
    letter_content = letters_file.read()
    for name in names:
        stripped_name = name.strip()
        letters = letter_content.replace(PLACEHOLDER, stripped_name)
        print(letters)
        with open(f"./Output/ReadyToSend/letter_for_{stripped_name}.txt", mode="w") as completed_letter:
            completed_letter.write(letters)

MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-',
                    'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
                    'X': '-..-', 'Y': '-.--', 'Z': '--..',
                    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...','8': '---..', '9': '----.', '0': '-----',
                    ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-','(': '-.--.', ')': '-.--.-',}


def encrypt(normal_string):
    morse_string = ""
    for letter in normal_string:
        if letter != ' ':
            morse_string += MORSE_CODE_DICT[letter] + ' '
        else:
            morse_string += ' '
    print(morse_string)
    return morse_string


def decrypt(coded_string):
    code_string = ""
    normal_string = ""
    for code in coded_string:
        if code != ' ':
            i = 0
            code_string += code
        else:
            i += 1
            if i == 2:
                normal_string += ' '
            else:
                for key, value in MORSE_CODE_DICT.items():
                    if value == code_string:
                        normal_string += key
                code_string = ""

    print(normal_string)


string = input("Enter your string: ").upper()
morse_message = encrypt(string)
decrypt(morse_message)





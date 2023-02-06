import pyttsx3
from PyPDF2 import PdfReader

reader = PdfReader("PATH_OF_FILE")
number_of_pages = len(reader.pages)
print(number_of_pages)
for page in range(number_of_pages):
    page = reader.pages[page-1]
    text = page.extract_text()

    # reading the text
    speak = pyttsx3.init()
    speak.say(text)
    speak.runAndWait()
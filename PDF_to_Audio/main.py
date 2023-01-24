import pyttsx3
from PyPDF2 import PdfReader

reader = PdfReader("C:/Users/jahna/OneDrive/Desktop/Jahnavi/Blog_Capstone_Project_Docs.pdf")
number_of_pages = len(reader.pages)
print(number_of_pages)
for page in range(number_of_pages):
    page = reader.pages[page-1]
    text = page.extract_text()

    # reading the text
    speak = pyttsx3.init()
    speak.say(text)
    speak.runAndWait()
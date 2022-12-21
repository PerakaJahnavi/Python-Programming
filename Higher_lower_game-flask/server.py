from flask import Flask
import random

app = Flask(__name__)
random_number = random.randint(0, 9)
print(random_number)


@app.route('/')
def entrance():
    return '<h1>Guess the number between 0 and 9</h1>' \
           '<iframe src="https://giphy.com/embed/3o7aCSPqXE5C6T8tBC" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/animation-retro-pixel-3o7aCSPqXE5C6T8tBC"></a></p>'


@app.route("/<int:number>")
def check(number):
    if number > random_number:
        print(random_number)
        return '<h2>Too High</h2>' \
               '<iframe src="https://giphy.com/embed/3o6ZtaO9BZHcOjmErm" width="480" height="453" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/dog-puppy-fly-3o6ZtaO9BZHcOjmErm"></a></p>'
    elif number < random_number:
        return '<h2>Too Low</h2>' \
               '<iframe src="https://giphy.com/embed/jD4DwBtqPXRXa" width="384" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/work-digging-jD4DwBtqPXRXa"></a></p>'
    else:
        return '<h2>Your Correct</h2>' \
               '<iframe src="https://giphy.com/embed/4T7e4DmcrP9du" width="458" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/puppy-biscuit-emerging-4T7e4DmcrP9du"></a></p>'


if __name__ == "__main__":
    app.run(debug=True)
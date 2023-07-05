from flask import Flask
from .views import home, ask_question

app = Flask(__name__)

# Register view functions
@app.route('/')
def index():
    return home()

@app.route('/chat', methods=['POST'])
def chat():
    return ask_question()

if __name__ == '__main__':
    app.run()

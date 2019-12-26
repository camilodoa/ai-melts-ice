from flask import Flask
from ai.ai import Predictor

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main_':
    app = Flask(__name__)
    app.run(host='0.0.0.0',port=8080)

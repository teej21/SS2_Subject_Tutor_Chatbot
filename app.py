from flask import Flask, request

import rag.rag
from rag.rag import get_answer

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


"""
post method to get the answer to a question
"""


@app.route('/api/answer', methods=['POST'])
def get_answer():
    question = request.json['question']
    print(question)
    return rag.rag.get_answer(question)





if __name__ == '__main__':
    app.run()

from flask import Flask
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

from src.routes.chat_route import chat_bp
from src.routes.user_route import user_bp  # Adjust the import path based on your project structure

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(chat_bp, url_prefix='/chat')

if __name__ == '__main__':
    app.run()

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# @app.route('/api/answer', methods=['POST'])
# def get_answer():
#     """
#     post method to get the answer to a question
#     """
#     question = request.json['question']
#     print(question)
#     return {
#         'answer': rag_utils.get_answer(question)
#     }

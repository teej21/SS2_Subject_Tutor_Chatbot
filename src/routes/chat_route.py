from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.utils import rag_utils

chat_bp = Blueprint('chat_bp', __name__)


@chat_bp.route('/get-answer', methods=['POST'])
@jwt_required()
def get_answer():
    """
    get the answer to a question
    """
    question = request.json['question']
    answer = rag_utils.get_answer(question)
    return {
        'answer': answer
    }

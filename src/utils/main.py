from rag_utils import *

import time


# # Start timer
# start_time = time.time()
#
# # Code to be timed
# print(get_answer("What programming language is used in this course?"))
# # End timer
# end_time = time.time()
#
# # Calculate elapsed time
# elapsed_time = end_time - start_time
# print("Elapsed time: ", elapsed_time)

def estimateResponseTime(question):
    print(f'#### **Question**: \n{question}')
    start_time = time.time()
    answer = get_answer(question)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'#### **Response Time**: {elapsed_time:.2f} seconds')
    print(f'#### **Answer**: \n'
          f'```\n'
          f'{answer}'
          f'\n```')
    print('-' * 10)


questions = [
    "Give me short advice to get good assessment in this course?",
    "Give me Module Code of this course?",
    "What is the course duration?"
]
for question in questions:
    estimateResponseTime(question)

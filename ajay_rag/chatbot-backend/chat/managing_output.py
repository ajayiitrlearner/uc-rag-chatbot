import json

# Function to determine the final output based on the given answers
def final_output(answer_for_trivia: dict, answer_for_user_question: dict):
    if answer_for_trivia:  # Return trivia answer if it exists
        return answer_for_trivia
    else:  # Otherwise, return the user question answer
        return answer_for_user_question

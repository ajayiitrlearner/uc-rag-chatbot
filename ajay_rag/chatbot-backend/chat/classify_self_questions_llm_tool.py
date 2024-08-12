from openai import OpenAI
from typing import List
from chat.prompts import classify_self_questions_system_prompt
from jinja2 import Template

# Function to classify questions using GPT-4o
def classify_self_questions_llm(query: str):
    
    client = OpenAI()  # Initialize OpenAI client
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": classify_self_questions_system_prompt },  # System prompt for context
            {"role": "user", "content": query}  # User's query to be classified
        ],
        model="gpt-3.5-turbo"  # Using GPT-4o model
    )

    return completion.choices[0].message.content  # Return the classification result

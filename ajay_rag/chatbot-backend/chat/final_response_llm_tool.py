from openai import OpenAI
from typing import List
from chat.prompts import final_response_system_prompt, final_response_user_message
from jinja2 import Template

# Function to generate a final response using GPT-4o
def final_response_from_llm(query: str, documents: List[dict], prev_history_documents: List[dict]):
    
    # Combine content from documents and previous history
    source_knowledge = "\n".join(document["content"] for document in documents if 'content' in document)
    prev_history = "\n".join(document["content"] for document in prev_history_documents if 'content' in document)
    
    # Render user template with combined content
    user_template = Template(final_response_user_message)
    rendered_user_template = user_template.render(source_knowledge=source_knowledge, prev_history=prev_history)
    
    client = OpenAI()  # Initialize OpenAI client
    completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": final_response_system_prompt },  # System prompt
            {"role": "system", "content": rendered_user_template},  # Rendered user template
            {"role": "user", "content": query},  # User's query
        ],
        model="gpt-3.5-turbo"  # Using GPT-4o model
    )

    return completion.choices[0].message.content  # Return the final response


    

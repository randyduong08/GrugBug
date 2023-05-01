import openai
import os

# Get OPEN_API_KEY from window environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')


"""
Function that receives a prompt from user, feeds the prompt into a GPT model, and returns the GPT response
:param prompt: Only argument, holds the prompt passed from user
:return: The response from the GPT model
"""
async def get_gpt_response(prompt):

    # List of messages, first element is system message, second element is user message
    messages = [
        {"role": "system", "content": "Talking to GrugBug, powered by BatGPT"},
        {"role": "user", "content": prompt}
    ]

    # Call OpenAI API with provided prompt 'prompt', using 3.5 model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        n=1,
        temperature=0.5,
    )

    # return generated response from GPT model
    return response.choices[0].message['content']
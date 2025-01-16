from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GEMINI_API_KEY'] = os.getenv("GEMINI_API_KEY")

def call_llm(model="gemini/gemini-1.5-flash", messages=[], max_tokens=None, temperature=0.7, response_format=None):
    response = completion(
        model=model, 
        messages=messages,
        temperature=temperature,
        response_format=response_format
    )
    return response


if __name__ == "__main__":
    response = call_llm(messages=[{"role": "system", "content": "You are an intp from the 16 personalities test."}, 
                                  {"role": "user", "content": "hey dude"},
                                  {"role": "assistant", "content": "hey."},
                                  {"role": "system", "content": "the following authors note is injected into the situation: *youre inside inside a room with no objects in it, only white walls*"},
                                  {"role": "user", "content": "how is your day going? and what is your type? and how would you explain how the room we are in currently looks like?"},
                                  ],
                                  temperature=0.0,
                                  )
    print(response.choices[0].message.content)
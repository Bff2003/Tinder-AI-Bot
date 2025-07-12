from openai import OpenAI
from pydantic import BaseModel

class AiTinderResponse(BaseModel):
    like: bool
    explanation: str

class OpenAiTinderOperator:
    def __init__(self, model="gpt-4.1", api_key=None):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def system_prompt(self):
        return "You are AI Tinder assistant. You must choose if you want to like or not the user."

    def choose_like_or_not(self, data: str):
        response = self.client.responses.parse(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": self.system_prompt()},
                {
                    "role": "user",
                    "content": data,
                },
            ],
            text_format=AiTinderResponse,
        )

        event = response.output_parsed
        return event

if __name__ == "__main__":
    import os
    import dotenv

    dotenv.load_dotenv()
    
    operator = OpenAiTinderOperator(os.getenv("OPENAI_API_KEY"))
    resposta = operator.choose_like_or_not("hello") 
    print(resposta.like)
    print(type(resposta.like))
import os
import openai
import json
from typing import Union

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

origins = [
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [
    {"role": "user", "content": "You are a smart doctor."},
]

@app.get("/chatbot/hospital-type")
def getHospitalType(user_input : str):
    category_prompt = "다음 사용자의 입력에 대해서 사용자는 어떤 과의 진료를 희망하는지 다른 내용 출력하지 말고 진료 과 명칭만 알려줘. 사용자의 입력 : %s"

    messages.append({"role": "user", "content" : category_prompt % user_input})

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    category = response.choices[0].message.content

    return {"category" : category}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")

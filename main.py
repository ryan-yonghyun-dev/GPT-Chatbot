import os
import openai
import json

openai.api_key = os.environ.get("OPENAI_API_KEY")

#messages = [
#        {"role": "system", "content": "You are a helpful assistant."},
#        {"role": "user", "content": "Who won the world series in 2020?"},
#        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#        {"role": "user", "content": "Where was it played?"}
#]

messages = [
    {"role": "user", "content": "You are a smart doctor."},
]

gender_input_process_is_running = True
gender = ""

while True:

    gender_prompt = "다음 사용자의 입력에 대해서 남자라면 M, 여자라면 F로 표현해줘. 사용자 입력 : '%s'"
    input_prompt = input("(의사) 당신의 성별은 무엇입니까? > ")

    messages.append({"role": "user", "content" : gender_prompt % input_prompt})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    gender = response.choices[0].message.content
    if gender == "M" :
        print("(의사) 남성분이시군요. 알겠습니다")
        break
    elif gender == "F" :
        print("(의사) 여성분이시군요. 알겠습니다")
        break
    else:
        print("(의사) 성별을 정확히 인식할 수 없습니다... 정확하게 당신의 성별을 알려주세요")

symptom_prompt = "다음 사용자의 입력에 대해서 이 사람의 증상을 간단하게 축약해서 ['증상1', '증상2', ..., '증상 N'] 이런 양식으로 알려줘. 사용자 입력 : '%s'"
input_prompt = input("(의사) 현재 어떤 증상을 가지고 있습니까? > ")

messages.append({"role": "user", "content" : symptom_prompt % input_prompt})

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)

symptom = response.choices[0].message.content
symptom_start_index, symptom_end_index = symptom.find("["), symptom.find("]")
symptom_list = eval(symptom[symptom_start_index:symptom_end_index+1]) 

print("(의사) ", end = "")
for i in range(0, len(symptom_list)):
    print(symptom_list[i], end = "")
    if i == 0:
        print("과 ", end="")
    elif i < len(symptom_list) - 1:
        print(", ", end = "")
    else:
        print("", end = "")

print("이 있으시군요... 알겠습니다")


background_prompt = "다음 사용자의 입력에 대해서 이 사람의 질환을 간단하게 축약해서 ['질환1', '질환2', ..., '질환 N'] 이런 양식으로 알려줘. 사용자 입력 : '%s'"
input_prompt = input("(의사) 평소에 앓고 계시는 병이 있습니까? > ")

messages.append({"role": "user", "content" : symptom_prompt % input_prompt})

response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages
)

background = response.choices[0].message.content
background_start_index, background_end_index = background.find("["), background.find("]")
background_list = eval(background[background_start_index:background_end_index+1]) 

print("(의사) ", end = "")
for i in range(0, len(background_list)):
    print(background_list[i], end = "")
    if i == 0:
        print("과 ", end="")
    elif i < len(background_list) - 1:
        print(", ", end = "")
    else:
        print("", end = "")

print("이 있으시군요... 알겠습니다")

questionnaire_tabular = {
    "sex" : gender,
    "symptom" : symptom_list,
    "background" : background_list
}

print("=========문진결과=========")
print(questionnaire_tabular)


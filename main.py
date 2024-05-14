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
familyships = []



category_input = input("(간호사) 안녕하세요. 어떤 과의 진료를 희망하세요? > ")
category_prompt = "다음 사용자의 입력에 대해서 사용자는 어떤 과의 진료를 희망하는지 다른 내용 출력하지 말고 진료 과 명칭만 알려줘. 사용자의 입력 : %s"

messages.append({"role": "user", "content" : category_prompt % category_input})

response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages
)
category = response.choices[0].message.content
print("(간호사) %s의 진료를 희망하시는군요. 알겠습니다." % category, end="\n\n")

age_prompt = "다음 사용자의 입력에 대해서 다른 내용 절대 출력하지 말고 나이를 숫자로만 알려줘. 사용자 입력 : '%s'"
input_prompt = input("(%s 의사) 환자분은 몇살이십니까? > " % category)

messages.append({"role": "user", "content" : age_prompt % input_prompt})

response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages
)
age = int(response.choices[0].message.content)
print("(%s 의사) %d세이시군요. 알겠습니다." % (category,age), end="\n\n")

while True:
    gender_prompt = "다음 사용자의 입력에 대해서 남자라면 M, 여자라면 F로 표현해줘. 사용자 입력 : '%s'"
    input_prompt = input("(%s 의사) 환자분의 성별은 무엇입니까? > " % category)

    messages.append({"role": "user", "content" : gender_prompt % input_prompt})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    gender = response.choices[0].message.content
    if gender == "M" :
        print("(%s 의사) 남성분이시군요. 알겠습니다" % category, end="\n\n")
        break

    elif gender == "F" :
        print("(%s 의사) 여성분이시군요. 알겠습니다" % category, end="\n\n")
        break

    else:
        print("(%s 의사) 성별을 정확히 인식할 수 없습니다... 정확하게 환자분의 성별을 알려주세요" % category, end="\n\n")

symptom_prompt = "다음 사용자의 입력에 대해서 이 사람의 증상을 간단하게 축약해서 ['증상1', '증상2', ..., , '증상 N'] 이런 양식으로 알려줘. 증상을 의학적 표현으로 변환해서 알려줘.  사용자 입력 : '%s'"
input_prompt = input("(%s 의사) 현재 어떤 증상을 가지고 있습니까? > " % category)

messages.append({"role": "user", "content" : symptom_prompt % input_prompt})

response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages
)

symptom = response.choices[0].message.content
symptom_start_index, symptom_end_index = symptom.find("["), symptom.find("]")
symptom_list = eval(symptom[symptom_start_index:symptom_end_index+1]) 

print("(%s 의사) " % category, end = "")
for i in range(0, len(symptom_list)):
    print(symptom_list[i], end = "")
    if i == 0 and len(symptom_list) > 1:
        print("과 ", end="")
    elif i < len(symptom_list) - 1:
        print(", ", end = "")
    else:
        print("", end = "")

print("이 있으시군요... 알겠습니다", end="\n\n")

for i in range(0, len(symptom_list)):
    familyship_prompt = "%s 은 유전적으로 발생할 수 있는 질병이야? 다른 내용 절대 출력하지 말고, True 또는 False로만 대답해줘" % symptom_list[i]
    messages.append({"role": "user", "content" : familyship_prompt})

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )

    is_familyship = response.choices[0].message.content

    if(bool(is_familyship)) :
        familyship_input = input("(%s 의사) 말씀해주신 증상들 중에 %s 은/는 가족력이 있을 수 있는데 가족 분들 중에 동일한 증상을 가지고 계신 분이 있으실까요? > " % (category, symptom_list[i]))
        extract_familyship_prompt = "사용자의 입력은 사용자가 가지고 있는 증상에 대한 가족력을 묻는 질문에 대한 응답 내용이야. 가족들 중에 누구에게 이 질병이 있는지 다른 내용 출력하지 말고 '가족 중에 누가 해당 질병을 가지고 있는지 호칭'만 알려줘. 사용자의 입력 : %s" % familyship_input
        messages.append({"role": "user", "content" : extract_familyship_prompt})
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )

        extract_familyship = response.choices[0].message.content

        familyships.append({'symptom' : symptom_list[i], 'familyship' : extract_familyship})
        
        print("(%s 의사) %s 쪽이 %s 질환을 가지고 계시네요... 알겠습니다." % (category, extract_familyship, symptom_list[i]), end="\n\n")


background_prompt = "다음 사용자의 입력에 대해서 이 사람의 질환을 간단하게 축약해서 ['질환1', '질환2', ..., '질환 N'] 이런 양식으로 알려줘. 질환을 알려줄 때 의학적으로 정확한 질환 명칭만 알려줘. 사용자 입력 : '%s'"
input_prompt = input("(%s 의사) 평소에 앓고 계시는 병이 있습니까? > " % category)

messages.append({"role": "user", "content" : symptom_prompt % input_prompt})

response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages
)

background = response.choices[0].message.content
background_start_index, background_end_index = background.find("["), background.find("]")
background_list = eval(background[background_start_index:background_end_index+1]) 

print("(%s 의사) " % category, end = "")
for i in range(0, len(background_list)):
    print(background_list[i], end = "")
    if i == 0 and len(symptom_list) > 1:
        print("과 ", end="")
    elif i < len(background_list) - 1:
        print(", ", end = "")
    else:
        print("", end = "")

print("이 있으시군요... 알겠습니다", end="\n\n")



for i in range(0, len(background_list)):
    familyship_prompt = "%s 라는 질병은 유전적으로 발생할 수 있는 질병이야? 다른 내용 절대 출력하지 말고, True 또는 False로만 대답해줘" % background_list[i]
    messages.append({"role": "user", "content" : familyship_prompt})

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )

    is_familyship = response.choices[0].message.content

    if(bool(is_familyship)):
        familyship_input = input("(%s 의사) 말씀해주신 기저 질환들 중에 %s 은 가족력이 있을 수 있는데 가족 분들 중에 동일한 질환을 앓고 계신 분이 있으실까요? > " % (category, background_list[i]))
        extract_familyship_prompt = "사용자의 입력은 기저 질환에서 가족력을 묻는 질문에 대한 응답 내용이야. 가족들 중에 누구에게 이 질병이 있는지 다른 내용 출력하지 말고 '가족 중에 누가 해당 질병을 가지고 있는지 호칭'만 알려줘. 사용자의 입력 : %s" % familyship_input
        messages.append({"role": "user", "content" : extract_familyship_prompt})
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )

        extract_familyship = response.choices[0].message.content

        familyships.append({'background' : background_list[i], 'familyship' : extract_familyship})
        
        print("(%s 의사) %s 쪽이 %s 질환을 가지고 계시네요... 알겠습니다." % (category, extract_familyship, background_list[i]))

questionnaire_tabular = {
    "category" : category,
    "age" : age,
    "sex" : gender,
    "symptom" : symptom_list,
    "background" : background_list,
    "familyship" : familyships
}

print("=========문진결과=========")
print(questionnaire_tabular)


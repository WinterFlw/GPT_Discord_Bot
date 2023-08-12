import random

def soragodong():
    with open("/workspace/GPT_Discord_Bot/code/magic_soragodong_answer.txt", "r", encoding="utf-8") as f:
        random_responses = f.readlines()
        respones = random.choice(random_responses)
    return(respones)

print(soragodong())
import random

def soragodong():
    with open("magic_soragodong_answer.txt", "r") as f:
        random_responses = f.readlines()
        respones = random.choice(random_responses)
    return(respones)

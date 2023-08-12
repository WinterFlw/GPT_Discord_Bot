import openai
from code.api_key import get_key

OPENAI_API_KEY = get_key("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

history = dict()


def add_history(user: str, text: str, bot_answer: str):
    if not user in history:
        history[user] = []
    pair = dict(
        prompt=text,
        answer=bot_answer
    )
    history[user] = history[user][-9:] + [pair]


def get_history(user: str) -> list:
    if not user in history:
        return []
    return history[user]


def prompt_to_chat(user: str, prompt: str) -> str:
    previous = get_history(user)
    conversation = ""
    for chat in previous:
        conversation += f"Human: {chat['prompt']}\n" \
                        f"Bot: {chat['answer']}\n"
    return conversation + "\n" + f"Human: {prompt}"

def chat_with_gpt(
    user: str,
    prompt: str,
    max_tokens: int = None,
    use_history: bool = None
) -> str:
    if max_tokens is None:
        max_tokens = 200
    if use_history is None or use_history == True:
        prompt = prompt_to_chat(user, prompt)
    print('prompt:', prompt)
    bot_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.25,
        top_p=0.5,
    )
    print('bot response:', bot_response)
    bot_answer = bot_response.choices[0].message['content'].strip()
    add_history(user, prompt, bot_answer)
    return bot_answer


def question_gpt(
    prompt: str,
    max_tokens: int = None,
) -> str:
    if max_tokens is None:
        max_tokens = 200
    print('prompt:', prompt)
    bot_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.25,
        top_p=0.5,
    )
    print('bot response:', bot_response)
    bot_answer = bot_response.choices[0].message['content'].strip()
    return bot_answer
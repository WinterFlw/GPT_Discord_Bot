import discord
import openai
import re
import random
from discord import option

from code.api_key import get_key
import code.ladder_game
import code.gpt
import code.magic_soragodong

OPENAI_API_KEY = get_key("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

DISCORD_BOT_KEY = get_key("DISCORD_BOT_KEY")
SERVER_IDS = get_key("SERVER_IDS")
bot = discord.Bot()

history = dict()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(SERVER_IDS)


@bot.event
async def on_connect():
    if bot.auto_sync_commands:
        await bot.sync_commands()
    print(f"{bot.user.name} connected.")


@bot.event
async def on_message(message):
    user = message.author
    if user == bot.user:
        return

    text = message.content
    if text.startswith('!chat '):
        prompt = text[6:]
        try:
            # 여러 채널에서 다른 문맥을 갖고 싶다면
            # user 가 아니라 채널을 포함한 f"{user}{message.channel}" 로 변경
            bot_answer = code.gpt.chat_with_gpt(user, prompt)
            await message.channel.send(f"> Your prompt is: {prompt}\nAnswer: {bot_answer}")
        except:
            await message.channel.send(f"> Your prompt is: {prompt}\nSorry, Failed to answer")


@bot.slash_command(guild_ids=SERVER_IDS)
@option(
    name="prompt",
    type=str,
    description="프롬프트를 적어주세요."
)
@option(
    name="max_length",
    type=int,
    description="AI가 출력할 수 있는 최대 답변 길이. (기본값: 200)",
    required=False,
)
@option(
    name="refresh",
    type=str,
    description="대화를 새로 시작합니다. (yes or no)",
    required=False,
)
async def chat(context, prompt: str, max_length: int, refresh: str):
    await context.defer()
    try:
        user = context.author
        # 여러 채널에서 다른 문맥을 갖고 싶다면
        # user 가 아니라 채널을 포함한 f"{user}{context.channel}" 로 변경
        use_history = (refresh or 'no').startswith('n')
        bot_answer = code.gpt.chat_with_gpt(user, prompt, max_tokens=max_length, use_history=use_history)
        await context.respond(f"> Prompt: {prompt}\n{bot_answer}")
    except Exception as err:
        await context.respond(f"> Prompt: {prompt}\n" \
                              f"Sorry, failed to answer\n" \
                              f"> {str(err)}")


@bot.slash_command(guild_ids=SERVER_IDS)    #랜덤 숫자
@option(
    name="front",
    type=int,
    description="랜덤 숫자 범위, N부터"
)
@option(
    name="rear",
    type=int,
    description="랜덤 숫자 범위, N까지",
)
@option(
    name="pick",
    type=int,
    description="몇 개를 뽑을지 선택합니다. 선택 안할 시 1개",
    required=False,
)
async def 랜덤(ctx, front: int, rear: int, pick: int):
    if pick is None:
        pick = 1
    if (front < rear) and (pick < (rear - front)):
        try:
            random.seed()
            randlist = []
            randnum = random.randint(front, rear)
            for i in range(pick):
                while randnum in randlist : # 중복될 경우
                    randnum = random.randint(front, rear) # 다시 난수 생성
                randlist.append(randnum) # 중복 되지 않은 경우만 추가
            randlist.sort()
            await ctx.respond(f"> {front}~{rear}사이에 랜덤으로 숫자 {pick}개를 추첨하겠습니다.\n{randlist}")
        except Exception as err:
            await ctx.send("랜덤함수, 알 수 없는 오류")
    else:
        await ctx.send("랜덤함수, 입력값 오류")

@bot.slash_command(guild_ids=SERVER_IDS)    #로또
async def 로또(ctx):
    try:
        random.seed()
        randlist = []
        randnum = random.randint(1, 45)
        for i in range(6):
            while randnum in randlist: # 중복될 경우
                randnum = random.randint(1, 45) # 다시 난수 생성
            randlist.append(randnum) # 중복 되지 않은 경우만 추가
        randlist.sort()
        await ctx.respond(f"> 로또는 재미로 사자.\n{randlist}")
    except Exception as err:
        await ctx.send("로또함수, 알 수 없는 오류")


@bot.slash_command(guild_ids=SERVER_IDS)    #사다리 게임
@option(
    name="row",
    type=int,
    description="사다리 몇 명이 참가할 지 선택합니다.",
    required=True,
)
@option(
    name="pick",
    type=int,
    description="당첨 몇 개를 뽑을지 선택합니다. 선택 안할 시 1개",
    required=False,
)
async def 사다리(ctx, row: int, pick: int):
    if pick is None:
        pick = 1
    if row > 1 and pick < row:
        try:
            ladder_text = code.ladder_game.make_ladder_text(row,pick)
            ladder_embed = discord.Embed(title = ":ladder: 사다리 결과", description = ladder_text, color = 0xff7f00)
            await ctx.respond(embed = ladder_embed)
        except ValueError as e:
            await ctx.respond(e)
@bot.slash_command(guild_ids=SERVER_IDS)    #마법의 소라고동
@option(
    name="question",
    type=str,
    description="마법의 소라고동님께 올릴 질문을 입력 합니다.",
    required=True,
)
async def 소라고동님(ctx, question: str):
    result = code.magic_soragodong.soragodong()
    await ctx.respond(f"> 마법의 소라고동님 {question}\n마법의 소라고동 : {result}")
            
bot.run(DISCORD_BOT_KEY)


"""
pip install git+https://github.com/Pycord-Development/pycord

nohup python index.py &

ps -ef | grep index.py

kill PID
"""
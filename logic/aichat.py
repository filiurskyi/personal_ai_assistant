import logging
from datetime import datetime
from pprint import pprint

from openai import OpenAI

from bot import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def simple_query(user_query):
    logging.info(f"AI query received: {user_query}")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant, skilled in life planning, calendar management and personal improvements. Today is {dt}".format(
                    dt=datetime.now()
                ),
            },
            {
                "role": "system",
                "content": "Format your answer as json with field user_context ()",
            },
            {
                "role": "user",
                "content": user_query,
            },
        ],
    )
    reply_text = completion.choices[0].message.content
    return reply_text


def voice_to_text(audio) -> str:
    contexts = "'create_new_event'|'gpt-query'"
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant, skilled in life planning, calendar management and personal improvements. Today is {dt}".format(
                    dt=datetime.now()
                ),
            },
            {
                "role": "system",
                "content": f"Format reply as json: {{'user_context': {contexts},'ev_date': 'dd.mm.yyyy','ev_title':'title', 'ev_time': 'hh:mm','ev_tags': '#tag1 #tag2 #tag3','ev_text': 'shot description of event'}}",
            },
            {
                "role": "user",
                "content": transcript.text,
            },
        ],
    )
    pprint("Tokens used: {}".format(completion.usage.total_tokens))
    reply_text = completion.choices[0].message.content
    return reply_text

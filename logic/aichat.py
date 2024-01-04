import logging
from datetime import datetime
from pprint import pprint

from openai import OpenAI

from bot import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

USER_CONTEXTS = "'create_new_event'|'create_new_note'"


def simple_query(user_query):
    logging.info(f"AI query received: {user_query}")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant, skilled in life planning, calendar management and personal "
                           "improvements. Today is {dt}".format(dt=datetime.now()),
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


def voice_to_text(audio, contexts=USER_CONTEXTS) -> str:
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant, skilled in life planning, calendar management and personal "
                           "improvements. Today is {dt}".format(dt=datetime.now()),
            },
            {
                "role": "system",
                "content": f"If user_context = create_new_event: Format reply as json: {{'user_context': {contexts}, 'ev_title':'title',"
                           f"'ev_datetime': 'dd.mm.yyyy hh:mm','ev_tags': '#tag1 #tag2 #tag3','ev_text': 'detailed "
                           f"description of event'}}",
            },
            {
                "role": "system",
                "content": f"If user_context = create_new_note: Format reply as json: {{'user_context': {contexts}, 'nt_title':'note title',"
                           f"'nt_text': 'formatted body text of note', 'nt_tags': '#tag1 #tag2 #tag3'}}",
            },
            {
                "role": "user",
                "content": transcript.text,
            },
        ],
    )
    pprint("Tokens used: {}".format(completion.usage.total_tokens))
    reply_text = completion.choices[0].message.content
    logging.info(reply_text)
    return reply_text


def text_to_text(user_message: str, contexts=USER_CONTEXTS) -> str:
    context_event = f"Format reply as json: {{'user_context': {contexts}, 'ev_title':'title', 'ev_datetime': 'dd.mm.yyyy hh:mm','ev_tags': '#tag1 #tag2 #tag3','ev_text': 'detailed description of event'}}"
    context_note = f"Format reply as json: {{'user_context': {contexts}, 'nt_title':'note title', 'nt_text': 'formatted body text of note', 'nt_tags': '#tag1 #tag2 #tag3'}}"
    if contexts == "create_new_event":
        context = context_event
    elif contexts == "create_new_note":
        context = context_note
    else:
        context = "unknown context"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant, skilled in life planning, calendar management and personal "
                           "improvements. Today is {dt}".format(dt=datetime.now()),
            },
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    )
    pprint("Tokens used: {}".format(completion.usage.total_tokens))
    reply_text = completion.choices[0].message.content
    logging.info(reply_text)
    return reply_text

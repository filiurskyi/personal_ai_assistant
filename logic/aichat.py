import logging

from openai import OpenAI

from bot import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def simple_query(user_query):
    logging.debug(f"AI query received: {user_query}")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a personal assistant, skilled in life planning, calendar management\
                and personal improvements.",
            },
            {
                "role": "user",
                "content": user_query,
            },
        ],
    )
    reply_text = completion.choices[0].message.content
    return reply_text


def voice_to_text(audio):
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio)
    return transcript.text

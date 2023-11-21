from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")

client = OpenAI()

# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("text-generation", model="MayaPH/GodziLLa2-70B")


def simple_query():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
            },
            {
                "role": "user",
                "content": "Compose a poem that explains the concept of recursion in programming.",
            },
        ],
    )
    return completion.choices[0].message


def voice_to_text(audio):
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio)
    return transcript

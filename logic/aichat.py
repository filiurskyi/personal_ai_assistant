from openai import OpenAI
client = OpenAI()

def simplequery():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ])
    return completion.choices[0].message


def voice_to_text(audio):
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio
        )
    return transcript
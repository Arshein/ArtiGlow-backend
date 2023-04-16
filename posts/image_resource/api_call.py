import openai
from artiglow import settings

openai.organization = settings.OPENAI_ORGANIZATION
openai.api_key = settings.OPENAI_API_KEY

def gen_image(prompt: str):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
    )
    return response["data"][0]["url"]

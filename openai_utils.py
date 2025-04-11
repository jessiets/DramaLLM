import openai
from api_keys import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def enhance_synopsis(title, overview):
    prompt = f"""
    Rewrite this K-drama or C-drama synopsis in a short, engaging way without spoilers. Also note the type of viewers who may enjoy it.

    Title: {title}
    Synopsis: {overview}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response['choices'][0]['message']['content']


def interpret_user_message(message):
    prompt = f"""
    A user said: "{message}"

    From this, extract the most relevant drama genre (like Romance, Comedy, Mystery, Drama, etc.), and identify if they prefer Korean or Chinese shows.

    Respond in this JSON format:
    {{
      "genre": "...",
      "region": "KR" or "CN"
    }}
    """
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return eval(res['choices'][0]['message']['content'])


def summarize_dramas(dramas):
    drama_list = ""
    for i, d in enumerate(dramas[:5], 1):
        drama_list += f"{i}. {d['name']} (Rating: {d['vote_average']}) - {d['overview']}\n\n"

    prompt = f"""
    Here are 5 Netflix dramas. Write a short summary and recommendation for each, like a friendly drama expert helping a viewer.

    {drama_list}
    """

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return res['choices'][0]['message']['content']

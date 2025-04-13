from openai import OpenAI
from api_keys import OPENAI_API_KEY

# openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)


def get_matched_synopsis(message, db):
    print(f"getting top matches...\n\n")
    # @return dict with keys: {data, distances, documents, embeddings, ids, included, metadatas, uris}
    top_matches = db.chromadb_user_query(message)
    top_documents = top_matches['documents'][0]

    print(f"top matches: {top_documents}\n\n")

    enhanced_responses = []
    for i in range(0, len(top_documents)):
        prompt = f"""
        Given the synopsis: {top_documents[i]}

        Rewrite this K-drama or C-drama synopsis in a short, engaging way without spoilers. 
        Note the type of viewers who may enjoy it.
        Write a short summary and recommendation for each, like a friendly drama expert helping a viewer.
        Do not include the title of the drama.
        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        response = completion.choices[0].message.content

        show_dict = {}
        show_dict["show_id"] = top_matches['metadatas'][0][i]['show_id']
        show_dict['synopsis'] = response

        enhanced_responses.append(show_dict)
    
    print(f'enhanced responses: \n{enhanced_responses}\n')
    return enhanced_responses


def interpret_user_message(message):
    prompt = f""" 
    Given the user input: {message}

    This user input describes what the user is looking for in a drama.
    Rewrite the input that will help with drama searching. 
    Feel free to include the genres, storylines, or anything of relevance.
    """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    print(f"\n\ninterpretted response: {completion}\n\n")
    return completion.choices[0].message.content


def analyze_results(message, db):
    analysis = []

    # interpret user message
    user_message = interpret_user_message(message)

    # get matched synopsis for the show
    enhanced_responses = get_matched_synopsis(message, db)

    for i in range(0, len(enhanced_responses)):
    
        prompt = f"""
        Given the user input: {user_message}
        Given the following match: {enhanced_responses[i]['synopsis']}

        Instruction:
        Analyze the match and determine whether it aligns with the user input or not.
        Respond only with yes or no. Do not elaborate.
        """

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        response = completion.choices[0].message.content
        show_dict = {}
        show_dict['show_id'] = enhanced_responses[i]['show_id']
        show_dict['synopsis'] = enhanced_responses[i]['synopsis']
        show_dict['is_match'] = response
        show_dict['user_input'] = user_message
        analysis.append(show_dict)

    return analysis
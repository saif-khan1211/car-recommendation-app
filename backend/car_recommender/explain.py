# backend/car_recommender/explain.py

import openai

def explain_prediction(data, tier, score):
    prompt = f"""
    A user submitted car data with the following:
    - Mileage: {data['mileage']}
    - Rating: {data['rating']}
    - Price: {data['price']}
    - Certification: {data['certified']}
    - Price Drop: {data['price drop']}

    The model scored it as a {tier} ({score}% likelihood).

    In 1-2 sentences, explain why this is likely a {tier} based on the data.
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()

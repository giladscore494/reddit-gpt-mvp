import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def translate_if_needed(text):
    if any("\u0590" <= c <= "\u05EA" for c in text):
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except:
            return text
    return text

def analyze_topics_and_problems(keyword, posts=None, mode="topics"):
    keyword_en = translate_if_needed(keyword)

    if mode == "topics":
        prompt = f"""
        The user is interested in '{keyword_en}'.
        Generate up to 5 subtopics (short keywords) related to this field.
        Return only comma-separated keywords.
        """
    else:
        posts_text = "\n".join(posts[:20])
        prompt = f"""
        Analyze the following online posts:
        {posts_text}
        Find up to 3 recurring **problems** related to '{keyword_en}'.
        Return them as a simple bullet list (no explanations).
        """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.3
    )
    content = response.choices[0].message.content.strip()
    return [t.strip("-• ") for t in content.split(",")] if mode == "topics" else \
           [p.strip("-• ") for p in content.split("\n") if p.strip()]

def analyze_solutions(problems):
    problems_text = "\n".join(problems)
    prompt = f"""
    Problems detected:
    {problems_text}

    Suggest exactly 3 physical products from AliExpress
    that solve these problems effectively.
    For each product, provide:
    - Product name
    - Match score (0-100%)

    Return JSON like:
    [
      {{"product": "Example Product 1", "match": 95}},
      {{"product": "Example Product 2", "match": 90}},
      {{"product": "Example Product 3", "match": 85}}
    ]
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.4
    )
    try:
        return json.loads(response.choices[0].message.content)
    except:
        return []

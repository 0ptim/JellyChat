import openai
import numpy as np  # standard math module for python
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def gpt3_embedding(content, engine='text-embedding-ada-002'):
    content = content.encode(encoding='ASCII', errors='ignore').decode()
    response = openai.Embedding.create(input=content, engine=engine)
    vector = response['data'][0]['embedding']  # this is a normal list
    return vector


def similarity(v1, v2):  # return dot product of two vectors
    return np.dot(v1, v2)


def match_class(vector, classes):
    results = list()
    for c in classes:
        score = similarity(vector, c['vector'])
        info = {'category': c['category'], 'score': score}
        results.append(info)
    return results


categories = ['plant', 'reptile', 'mammal',
              'fish', 'bird', 'pet', 'wild animal']

classes = list()
for c in categories:
    vector = gpt3_embedding(c)
    info = {'category': c, 'vector': vector}
    classes.append(info)

while True:
    a = input('Enter a lifeform here: ')
    vector = gpt3_embedding(a)
    # print(a, vector)
    result = match_class(vector, classes)
    pprint(result)

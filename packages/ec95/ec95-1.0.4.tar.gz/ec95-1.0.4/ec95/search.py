import json
import os
import pickle

import numpy as np
import pyperclip
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

file_pref = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(file_pref, "teor_tasks.json"), "r+", encoding="UTF-8") as f:
    teor_tasks = json.load(f)

with open(os.path.join(file_pref, "pr_tasks.json"), "r+", encoding="UTF-8") as f:
    pr_tasks = json.load(f)

if os.path.isfile(os.path.join(file_pref, "test_tf_idf.pickle")):
    with open(os.path.join(file_pref, "vect_corpus.pickle"), "rb") as f:
        vect_corpus = pickle.load(f)

    with open(os.path.join(file_pref, "vectorizer.pickle"), "rb") as f:
        vectorizer = pickle.load(f)

else:
    corpus = list(teor_tasks.keys())

    vectorizer = TfidfVectorizer()
    vect_corpus = vectorizer.fit_transform(corpus)

    with open(os.path.join(file_pref, "vect_corpus.pickle"), "wb") as f:
        pickle.dump(vect_corpus, f)

    with open(os.path.join(file_pref, "vectorizer.pickle"), "wb") as f:
        pickle.dump(vectorizer, f)


def title_teor(query, top_k=1):
    query = vectorizer.transform([query])
    answer = ""
    for ind in np.argsort(cosine_similarity(query, vect_corpus)[0])[-top_k:][::-1]:
        answer += str(corpus[ind]) + "\n"

    pyperclip.copy(answer)

    return type("TempClass", (), {"__doc__": answer})()


def answer_teor(query):
    query = vectorizer.transform([query])
    ind = np.argmax(cosine_similarity(query, vect_corpus)[0])
    answer = teor_tasks[corpus[ind]]
    pyperclip.copy(answer)

    return type("TempClass", (), {"__doc__": answer})()


def search_pr(*args):
    query = "pr_tasks"
    for arg in args:
        query += f"['{arg}']"

    answer = eval(query)
    if isinstance(answer, dict):
        keys_ = answer.keys()
        answer = ""
        for key in keys_:
            answer += str(key) + "\n"

    pyperclip.copy(answer)

    return type("TempClass", (), {"__doc__": answer})()

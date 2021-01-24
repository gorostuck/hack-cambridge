
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

def normalized_term_frequency(word, document):
    raw_frequency = document.count(word)
    if raw_frequency == 0:
        return 0
    return 1 + math.log(raw_frequency)


def docs_contain_word(word, documents):
    counter = 0
    for document in documents:
        if word in document:
            counter += 1
    return counter

def get_vocabulary(documents):
    vocabulary = set([word for document in documents for word in document])
    return vocabulary


def cos_similarity(query, tfidf_matrix):
    cosine_distance = cosine_similarity(query, tfidf_matrix)
    similarity_list = cosine_distance[0]
    return similarity_list


def most_similar(similarity_list, min_items=1):
    most_similar = []
    while min_items > 0:
        tmp_index = np.argmax(similarity_list)
        most_similar.append(tmp_index)
        similarity_list[tmp_index] = 0
        min_items -= 1
    return most_similar

def TFIDF(query, documents):
    tfIdfVectorizer=TfidfVectorizer(use_idf=True)
    tfIdf = tfIdfVectorizer.fit_transform(documents)
    df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False)
    tfIdf2 = tfIdfVectorizer.transform(query)
    tf = pd.DataFrame(tfIdf2[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
    tf = tf.sort_values('TF-IDF', ascending=False)
    print(tf.head(25))
    return tf, df


#returns a dictionary of placeID : similarity_score for every company with respect to the query
def search(query, reviews):
    scores = {}
    count = 0
    for review in reviews:
        content = review.content
        try:
            tf, df = TFIDF(query,content)
            avg_score = tf.mean()
            placeID = review.company
            scores[placeID] = float(avg_score)
        except:
            print("review doesnt contain vocab words")
    return scores

def combine_all_reviews(all_reviews):
    all_docs = []
    for review in all_reviews:
        document = review.content
        all_docs.append(document)
    return all_docs

#takes the dictionary of placeID : similarityScore and returns a sorted list ranked by similarityScore
#the highest index in this list corresponds to the placeID of the highest similarity to the query
def sort_by_similarity(score_dict):
    sorted_dict = {}
    sorted_keys = sorted(score_dict, key=score_dict.get)
    for w in sorted_keys:
        sorted_dict[w] = score_dict[w]
    return sorted_dict


def get_sorted_scores(reviews, q):
    '''Returns sorted scores for a given set of reviews and a query.'''
    review_data = reviews #this is where you pass the review data list
    query = q #this is where you specify the user query

    all_reviews = combine_all_reviews(review_data)
    vocab = get_vocabulary(all_reviews)
    scores_dictionary = search(query, review_data)
    sorted_scores = sort_by_similarity(scores_dictionary)

    return sorted_scores



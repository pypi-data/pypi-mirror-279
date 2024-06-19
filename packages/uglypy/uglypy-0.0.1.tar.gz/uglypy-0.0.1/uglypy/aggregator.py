import re
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
import nltk
from nltk.corpus import stopwords
import spacy

# Ensure required resources are available
nltk.download('stopwords', quiet=True)

# Download and load spaCy model if not already downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Initialize other NLP tools
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    """Normalizes, removes punctuation, HTML tags, and applies tokenization and lemmatization."""
    text = re.sub(r"<[^<]+?>", "", text)  # Remove HTML tags
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = [word for word in text.split() if word not in stop_words]
    lemmatized_tokens = [token.lemma_ for token in nlp(" ".join(tokens))]
    return " ".join(lemmatized_tokens)

def group_similar_articles(
    articles: List[Dict[str, str]], 
    similarity_threshold: float, 
    similarity_options: dict
) -> List[List[Dict[str, str]]]:
    """Groups similar articles based on a similarity threshold and options."""
    if not articles:
        return []

    # Preprocess text
    texts = [f"{article['title']} {article['content']}" for article in articles]
    preprocessed_texts = [preprocess_text(text) for text in texts]

    # Vectorize texts using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_texts)

    # Compute cosine similarity matrix
    cosine_sim_matrix = cosine_similarity(tfidf_matrix)

    # Compute the distance matrix for clustering
    distance_matrix = 1 - cosine_sim_matrix
    distance_matrix[distance_matrix < 0] = 0  # Ensure no negative distances

    # Cluster articles using DBSCAN
    clustering = DBSCAN(metric='precomputed', **similarity_options).fit(distance_matrix)
    cluster_labels = clustering.labels_

    # Group articles by their cluster labels
    grouped_articles = []
    for label in set(cluster_labels):
        if label != -1:  # -1 indicates noise points
            group = [articles[i] for i in range(len(articles)) if cluster_labels[i] == label]
            grouped_articles.append(group)

    return grouped_articles


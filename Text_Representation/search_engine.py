import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


class SearchEngine:
    def __init__(self, preprocessed_csv: str = None, df: pd.DataFrame = None):
        if df is None:
            if preprocessed_csv is None:
                project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                preprocessed_csv = os.path.join(project_root, "preprocessed_financial_news.csv")
            df = pd.read_csv(preprocessed_csv)

        self.df = df
        self.documents = self.df["clean_text"].fillna("")

        # TF-IDF Vectorization
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

        print("TF-IDF completed!")
        print("Number of documents:", self.tfidf_matrix.shape[0])
        print("Number of unique terms:", self.tfidf_matrix.shape[1])

    def search(self, query: str, top_k: int = 5) -> pd.DataFrame:
        query_vector = self.vectorizer.transform([query])

        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        top_indices = similarity_scores.argsort()[::-1][:top_k]

        results = self.df.iloc[top_indices].copy()
        results["similarity_score"] = similarity_scores[top_indices]

        return results[["title", "source", "time_published", "similarity_score"]]


if __name__ == "__main__":
    engine = SearchEngine()
    print(engine.search("interest rates"))

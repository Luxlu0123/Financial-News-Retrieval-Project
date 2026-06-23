import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os


def preprocess(input_path: str = None, output_path: str = "preprocessed_financial_news.csv") -> pd.DataFrame:
    """Read raw articles CSV, clean text, and write preprocessed CSV.

    Returns the preprocessed dataframe.
    """
    if input_path is None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        input_path = os.path.join(project_root, "financial_news_articles.csv")

    df = pd.read_csv(input_path)

    # Check for missing values and duplicates
    print(df.head())
    print(df.shape)
    print(df.info())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDuplicate URLs:")
    print(df.duplicated(subset=["url"]).sum())

    # Convert title to string
    df["title"] = df["title"].astype(str)

    # Remove bracketed prefixes such as [424B2], [144], [Form 4]
    df["title"] = df["title"].str.replace(
        r"^\[[^\]]+\]\s*",
        "",
        regex=True
    )

    # Remove leading SEC form labels such as "Form 8K", "Form 4", "Form 144"
    df["title"] = df["title"].str.replace(
        r"^Form\s+\w+\s+",
        "",
        regex=True
    )

    # Remove date and source suffixes such as "For: 22 June By Investing.com"
    df["title"] = df["title"].str.replace(
        r"\s+For:\s+\d{1,2}\s+\w+\s+By\s+Investing\.com$",
        "",
        regex=True
    )

    # Remove simple source suffix such as "By Investing.com"
    df["title"] = df["title"].str.replace(
        r"\s+By\s+Investing\.com$",
        "",
        regex=True
    )

    # Remove extra spaces
    df["title"] = df["title"].str.replace(r"\s+", " ", regex=True).str.strip()

    # Remove duplicate titles after cleaning
    df = df.drop_duplicates(subset=["title"]).reset_index(drop=True)

    print("After title cleaning and duplicate removal:", df.shape)

    # Combine title and summary into a single text column
    df["text"] = df["title"].fillna("") + " " + df["summary"].fillna("")

    # Lowercase the text
    df["text"] = df["text"].str.lower()

    # Remove punctuation
    def remove_punctuation(text):
        return re.sub(r"[^\w\s]", "", str(text))

    df["text"] = df["text"].apply(remove_punctuation)

    # Tokenization
    df["tokens"] = df["text"].apply(lambda x: x.split())

    # Stopword removal
    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))
    df["tokens"] = df["tokens"].apply(
        lambda words: [w for w in words if w not in stop_words]
    )

    # Lemmatization
    nltk.download("wordnet", quiet=True)
    lemmatizer = WordNetLemmatizer()
    df["tokens"] = df["tokens"].apply(
        lambda words: [lemmatizer.lemmatize(w) for w in words]
    )

    # Save the preprocessed dataset to a new CSV file
    df["clean_text"] = df["tokens"].apply(lambda x: " ".join(x))

    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("Saved preprocessed dataset to", os.path.abspath(output_path))

    return df


if __name__ == "__main__":
    preprocess()
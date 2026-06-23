import os
import pandas as pd
import importlib.util


def load_module_from_path(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    # If this file is at the repository root, project_root should be its directory
    project_root = os.path.abspath(os.path.dirname(__file__))

    api_path = os.path.join(project_root, "Raw data", "api.py")
    preproc_path = os.path.join(project_root, "Cleansed data", "Data_preprocessing.py")
    search_path = os.path.join(project_root, "Text_Representation", "search_engine.py")

    api_mod = load_module_from_path("api_mod", api_path)
    preproc_mod = load_module_from_path("preproc_mod", preproc_path)
    search_mod = load_module_from_path("search_mod", search_path)

    # Step 1: Fetch articles (saves to financial_news_articles.csv by default)
    print("Fetching articles...")
    api_mod.fetch_articles()

    # Step 2: Preprocess and write preprocessed_financial_news.csv
    print("Preprocessing articles...")
    preprocessed_path = os.path.join(project_root, "preprocessed_financial_news.csv")
    preproc_mod.preprocess(output_path=preprocessed_path)

    # Step 3: Build search engine
    print("Building search index...")
    engine = search_mod.SearchEngine(preprocessed_csv=preprocessed_path)

    # Step 4: Evaluation queries
    test_queries = [
        "interest rates",
        "inflation",
        "stock market",
        "federal reserve",
        "economic growth",
    ]

    evaluation_results = []

    for query in test_queries:
        print("\n" + "=" * 80)
        print("Query:", query)
        results = engine.search(query)
        print(results)
        results["query"] = query
        evaluation_results.append(results)

    final_results = pd.concat(evaluation_results)
    out_path = os.path.join(project_root, "evaluation_results.csv")
    final_results.to_csv(out_path, index=False, encoding="utf-8-sig")
    print("Evaluation results saved to", out_path)


if __name__ == "__main__":
    main()
import os
import pandas as pd

import minsearch


DATA_PATH = os.getenv("DATA_PATH", "../data/Azure-DP-900.apkg.csv")


def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)

    documents = df.to_dict(orient="records")

    index = minsearch.Index(
        text_fields=[
            "question",
            "answer",
            "exam",
            "section",
        ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index

if __name__ == "__main__":
    print("Ingesting data...")
    index = load_index(data_path=DATA_PATH)
    print(f' Indexed {len(index.docs)} document(s)')
from rank_bm25 import BM25Okapi

from .tokenizer import tokenize


class SearchIndex:

    def __init__(self, documents):

        self.documents = documents

        tokenized_documents = []

        for document in documents:

            text = (document["title"] + " " + document["content"])

            tokens = tokenize(text)

            tokenized_documents.append(tokens)

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def search(
        self,
        query,
        limit=10
    ):

        tokens = tokenize(query)

        scores = self.bm25.get_scores(
            tokens
        )

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for index, score in ranked[:limit]:

            document = self.documents[
                index
            ]

            results.append({
                **document,
                "score": float(score)
            })

        return results
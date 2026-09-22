from app.database.db import get_all_documents

from app.indexer.bm25 import SearchIndex


class SearchEngine:

    def __init__(self):

        rows = get_all_documents()

        self.documents = []

        for row in rows:

            self.documents.append({
                "id": row[0],
                "url": row[1],
                "title": row[2] or "",
                "content": row[3] or ""
            })

        self.index = SearchIndex(
            self.documents
        )

    def search(self, query):

        return self.index.search(
            query,
            limit=10
        )
from fastapi import FastAPI, Query

from fastapi.middleware.cors import (
    CORSMiddleware
)

from .search.engine import SearchEngine


app = FastAPI(
    title="My Search Engine"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


engine = SearchEngine()


@app.get("/")
def root():

    return {
        "message":
            "My Search Engine API"
    }


@app.get("/search")
def search(
    q: str = Query(
        min_length=1
    )
):

    results = engine.search(q)
    formatted_results = []

    for result in results:
        item = {
            "title": result["title"],
            "url": result["url"],
            "score": result["score"],
            "snippet": result["content"][:300]
        }
        formatted_results.append(item)

    return {
        "query": q,
        "results": formatted_results
        
}
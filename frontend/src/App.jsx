import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function search(e) {

        e.preventDefault();

        if (!query.trim()) {
            return;
        }

        setLoading(true);
        setError("");

        try {

            const response =
                await axios.get(
                    "http://127.0.0.1:8000/search",
                    {
                        params: {
                            q: query
                        }
                    }
                );

            setResults(
                response.data.results
            );

        } catch (error) {

            console.error(error);
            setError("The search service is unavailable. Check that the backend is running.");

        } finally {

            setLoading(false);
        }
    }

    return (

        <div className="app-shell">
            <header className="site-header">
                <a className="brand" href="/">
                    <span className="brand-mark">K</span>
                    <span>khoj</span>
                </a>
                <span className="header-note">A focused index for the web</span>
            </header>

            <main className="content">
                <section className="intro" aria-labelledby="page-title">
                    <p className="eyebrow">Explore your index</p>
                    <h1 id="page-title">Find the signal.</h1>
                    <p className="intro-copy">
                        Search across the pages collected by your local crawler.
                    </p>

                    <form className="search-form" onSubmit={search}>
                        <label className="sr-only" htmlFor="search-input">Search your index</label>
                        <input
                            id="search-input"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Try a topic, phrase, or URL"
                            autoComplete="off"
                        />
                        <button type="submit" disabled={loading}>
                            {loading ? "Searching" : "Search"}
                        </button>
                    </form>
                </section>

                <section className="results-section" aria-live="polite">
                    {loading && <p className="status-message">Searching your index...</p>}
                    {error && <p className="status-message error-message">{error}</p>}

                    {!loading && !error && results.length > 0 && (
                        <div className="results-heading">
                            <span>Results</span>
                            <span className="result-count">{results.length} found</span>
                        </div>
                    )}

                    {!loading && !error && results.length === 0 && (
                        <div className="empty-state">
                            <span className="empty-line" />
                            <p>Results will appear here</p>
                            <span>Start with a search above.</span>
                        </div>
                    )}

                    <div className="result-list">
                        {results.map((result, index) => (
                            <article className="result" key={`${result.url}-${index}`}>
                                <p className="result-number">{String(index + 1).padStart(2, "0")}</p>
                                <div className="result-body">
                                    <a className="result-title" href={result.url} target="_blank" rel="noreferrer">
                                        {result.title || "Untitled document"}
                                    </a>
                                    <p className="result-url">{result.url}</p>
                                    <p className="result-snippet">{result.snippet}</p>
                                </div>
                            </article>
                        ))}
                    </div>
                </section>
            </main>

        </div>
    );
}

export default App;
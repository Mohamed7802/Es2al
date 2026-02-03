/**
 * SearchChunks Component
 * Allows searching for relevant document chunks
 */
import React, { useState } from 'react';
import { searchChunks } from '../services/api';

function SearchChunks({ isVideoProcessed }) {
    const [query, setQuery] = useState('');
    const [numChunks, setNumChunks] = useState(3);
    const [results, setResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);
    const [error, setError] = useState('');

    const handleSearch = async (e) => {
        e.preventDefault();

        if (!query.trim()) {
            setError('Please enter a search query');
            return;
        }

        if (!isVideoProcessed) {
            setError('Please process a video first');
            return;
        }

        setIsSearching(true);
        setError('');

        try {
            const response = await searchChunks(query, numChunks);

            if (response.success) {
                setResults(response.chunks);
            } else {
                setError(response.error || 'Search failed');
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setIsSearching(false);
        }
    };

    return (
        <div className="search-container">
            <h2>🔍 Search Chunks</h2>
            <p className="search-description">
                Find relevant sections without generating an answer
            </p>

            <form onSubmit={handleSearch} className="search-form">
                <div className="search-input-group">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Enter search query..."
                        className="search-input"
                        disabled={isSearching || !isVideoProcessed}
                    />

                    <div className="chunks-selector">
                        <label htmlFor="numChunks">Chunks:</label>
                        <input
                            type="number"
                            id="numChunks"
                            min="1"
                            max="10"
                            value={numChunks}
                            onChange={(e) => setNumChunks(parseInt(e.target.value))}
                            className="chunks-input"
                            disabled={isSearching}
                        />
                    </div>

                    <button
                        type="submit"
                        className="search-btn"
                        disabled={isSearching || !isVideoProcessed}
                    >
                        {isSearching ? '⏳ Searching...' : '🔍 Search'}
                    </button>
                </div>
            </form>

            {error && (
                <div className="status-message error">
                    ❌ {error}
                </div>
            )}

            {results.length > 0 && (
                <div className="search-results">
                    <h3>Found {results.length} relevant chunks:</h3>
                    {results.map((chunk, idx) => (
                        <div key={idx} className="chunk-card">
                            <div className="chunk-header">
                                <span className="chunk-number">Chunk {idx + 1}</span>
                            </div>
                            <div className="chunk-content">
                                {chunk.content}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default SearchChunks;
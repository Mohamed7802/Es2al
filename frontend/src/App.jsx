/**
 * Main App Component
 * Orchestrates the entire frontend application
 */
import React, { useState, useEffect } from 'react';
import VideoInput from './components/VideoInput';
import Chat from './components/Chat';
import SearchChunks from './components/SearchChunks';
import { getTranscription, getStatus } from './services/api';
import './App.css';

function App() {
    const [activeTab, setActiveTab] = useState('chat');
    const [isVideoProcessed, setIsVideoProcessed] = useState(false);
    const [transcription, setTranscription] = useState('');
    const [videoInfo, setVideoInfo] = useState(null);

    // Check system status on mount
    useEffect(() => {
        checkStatus();
    }, []);

    const checkStatus = async () => {
        try {
            const status = await getStatus();
            setIsVideoProcessed(status.initialized);
        } catch (err) {
            console.error('Failed to check status:', err);
        }
    };

    const handleVideoProcessed = (result) => {
        setIsVideoProcessed(true);
        setVideoInfo(result);
        setActiveTab('chat'); // Switch to chat tab
    };

    const handleShowTranscription = async () => {
        if (!transcription) {
            try {
                const response = await getTranscription();
                if (response.success) {
                    setTranscription(response.transcription);
                }
            } catch (err) {
                alert('Failed to load transcription: ' + err.message);
            }
        }
    };

    return (
        <div className="App">
            <header className="app-header">
                <h1>🎥 Video RAG Chat System</h1>
                <p>Ask questions about YouTube videos using AI</p>
            </header>

            <main className="app-main">
                {/* Video Input Section */}
                <section className="video-section">
                    <VideoInput onVideoProcessed={handleVideoProcessed} />
                </section>

                {/* Tabs Section */}
                <section className="tabs-section">
                    <div className="tabs-header">
                        <button
                            className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
                            onClick={() => setActiveTab('chat')}
                        >
                            💬 Chat
                        </button>
                        <button
                            className={`tab ${activeTab === 'search' ? 'active' : ''}`}
                            onClick={() => setActiveTab('search')}
                        >
                            🔍 Search
                        </button>
                        <button
                            className={`tab ${activeTab === 'transcription' ? 'active' : ''}`}
                            onClick={() => {
                                setActiveTab('transcription');
                                handleShowTranscription();
                            }}
                        >
                            📝 Transcription
                        </button>
                    </div>

                    <div className="tab-content">
                        {activeTab === 'chat' && (
                            <Chat isVideoProcessed={isVideoProcessed} />
                        )}

                        {activeTab === 'search' && (
                            <SearchChunks isVideoProcessed={isVideoProcessed} />
                        )}

                        {activeTab === 'transcription' && (
                            <div className="transcription-view">
                                <h2>📝 Full Transcription</h2>
                                {transcription ? (
                                    <div className="transcription-content">
                                        <textarea
                                            value={transcription}
                                            readOnly
                                            className="transcription-text"
                                        />
                                    </div>
                                ) : (
                                    <div className="empty-state">
                                        <p>Loading transcription...</p>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </section>

                {/* Info Section */}
                {videoInfo && (
                    <section className="info-section">
                        <div className="info-card">
                            <h3>Video Information</h3>
                            <p><strong>Title:</strong> {videoInfo.video_title}</p>
                            <p><strong>Transcription Length:</strong> {videoInfo.transcription_length} characters</p>
                            <p><strong>Chunks:</strong> {videoInfo.chunks_created}</p>
                        </div>
                    </section>
                )}
            </main>

            <footer className="app-footer">
                <p>Powered by FastAPI + React | OpenAI GPT & Whisper</p>
            </footer>
        </div>
    );
}

export default App;
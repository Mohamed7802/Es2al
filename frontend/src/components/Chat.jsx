/**
 * Chat Component
 * Handles conversation interface for asking questions about the video
 */
import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

function Chat({ isVideoProcessed }) {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!inputValue.trim()) return;

        if (!isVideoProcessed) {
            alert('Please process a video first!');
            return;
        }

        // Add user message
        const userMessage = {
            role: 'user',
            content: inputValue,
            timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const response = await sendChatMessage(inputValue);

            // Add assistant message
            const assistantMessage = {
                role: 'assistant',
                content: response.success ? response.answer : (response.error || 'Sorry, I couldn\'t process that.'),
                timestamp: new Date().toISOString(),
            };
            setMessages(prev => [...prev, assistantMessage]);
        } catch (err) {
            // Add error message
            const errorMessage = {
                role: 'assistant',
                content: `Error: ${err.message}`,
                timestamp: new Date().toISOString(),
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClear = () => {
        setMessages([]);
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h2>💬 Chat</h2>
                {messages.length > 0 && (
                    <button onClick={handleClear} className="clear-btn">
                        🗑️ Clear
                    </button>
                )}
            </div>

            <div className="messages-container">
                {messages.length === 0 ? (
                    <div className="empty-state">
                        <p>Ask questions about the video content!</p>
                        <ul className="suggestions">
                            <li>What is the main topic?</li>
                            <li>Summarize the key points</li>
                            <li>What does the speaker say about...?</li>
                        </ul>
                    </div>
                ) : (
                    messages.map((msg, idx) => (
                        <div key={idx} className={`message ${msg.role}`}>
                            <div className="message-avatar">
                                {msg.role === 'user' ? '👤' : '🤖'}
                            </div>
                            <div className="message-content">
                                <div className="message-text">{msg.content}</div>
                                <div className="message-time">
                                    {new Date(msg.timestamp).toLocaleTimeString()}
                                </div>
                            </div>
                        </div>
                    ))
                )}
                {isLoading && (
                    <div className="message assistant">
                        <div className="message-avatar">🤖</div>
                        <div className="message-content">
                            <div className="typing-indicator">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSubmit} className="chat-input-form">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder={isVideoProcessed ? "Ask a question..." : "Process a video first..."}
                    className="chat-input"
                    disabled={isLoading || !isVideoProcessed}
                />
                <button
                    type="submit"
                    className="send-btn"
                    disabled={isLoading || !isVideoProcessed || !inputValue.trim()}
                >
                    {isLoading ? '⏳' : '➤'}
                </button>
            </form>
        </div>
    );
}

export default Chat;
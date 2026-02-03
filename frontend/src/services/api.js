/**
 * API service for communicating with the backend.
 * Handles all HTTP requests to the FastAPI server.
 */
import axios from 'axios';

// Base URL for API - uses proxy in development
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 600000, // 10 minutes for video processing
});

/**
 * Process a YouTube video
 * @param {string} videoUrl - YouTube video URL
 * @returns {Promise} - Processing result
 */
export const processVideo = async (videoUrl) => {
    try {
        const response = await apiClient.post('/video/process', {
            video_url: videoUrl,
        });
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

/**
 * Send a chat message/question
 * @param {string} question - User question
 * @returns {Promise} - Answer from the AI
 */
export const sendChatMessage = async (question) => {
    try {
        const response = await apiClient.post('/chat', {
            question: question,
        });
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

/**
 * Search for similar chunks
 * @param {string} query - Search query
 * @param {number} numChunks - Number of chunks to retrieve
 * @returns {Promise} - Search results
 */
export const searchChunks = async (query, numChunks = 3) => {
    try {
        const response = await apiClient.post('/search', {
            query: query,
            num_chunks: numChunks,
        });
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

/**
 * Get the full transcription
 * @returns {Promise} - Transcription text
 */
export const getTranscription = async () => {
    try {
        const response = await apiClient.get('/transcription');
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

/**
 * Get system status
 * @returns {Promise} - System status
 */
export const getStatus = async () => {
    try {
        const response = await apiClient.get('/status');
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

/**
 * Health check
 * @returns {Promise} - Health status
 */
export const healthCheck = async () => {
    try {
        const response = await axios.get('/health');
        return response.data;
    } catch (error) {
        throw handleApiError(error);
    }
};

/**
 * Handle API errors consistently
 * @param {Error} error - Axios error object
 * @returns {Error} - Formatted error
 */
const handleApiError = (error) => {
    if (error.response) {
        // Server responded with error status
        const message = error.response.data?.detail || error.response.data?.error || error.message;
        return new Error(message);
    } else if (error.request) {
        // Request made but no response
        return new Error('No response from server. Please check your connection.');
    } else {
        // Other errors
        return new Error(error.message || 'An unexpected error occurred');
    }
};

export default {
    processVideo,
    sendChatMessage,
    searchChunks,
    getTranscription,
    getStatus,
    healthCheck,
};
/**
 * VideoInput Component
 * Handles YouTube URL input and video processing
 */
import React, { useState } from 'react';
import { processVideo } from '../services/api';

function VideoInput({ onVideoProcessed }) {
  const [videoUrl, setVideoUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!videoUrl.trim()) {
      setError('Please enter a YouTube URL');
      return;
    }

    setIsProcessing(true);
    setError('');
    setStatus('Processing video... This may take several minutes.');

    try {
      const result = await processVideo(videoUrl);
      
      if (result.success) {
        setStatus(`✅ Success! Processed "${result.video_title}" (${result.chunks_created} chunks created)`);
        onVideoProcessed(result);
      } else {
        setError(result.error || 'Failed to process video');
      }
    } catch (err) {
      setError(err.message);
      setStatus('');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="video-input-container">
      <h2>🎥 Process YouTube Video</h2>
      
      <form onSubmit={handleSubmit} className="video-form">
        <div className="input-group">
          <input
            type="text"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            placeholder="https://www.youtube.com/watch?v=..."
            className="url-input"
            disabled={isProcessing}
          />
          <button
            type="submit"
            className="process-btn"
            disabled={isProcessing}
          >
            {isProcessing ? '⏳ Processing...' : '🎬 Process Video'}
          </button>
        </div>
      </form>

      {status && (
        <div className="status-message success">
          {status}
        </div>
      )}

      {error && (
        <div className="status-message error">
          ❌ {error}
        </div>
      )}

      <div className="example-urls">
        <p>Example URL:</p>
        <button
          className="example-btn"
          onClick={() => setVideoUrl('https://www.youtube.com/watch?v=cdiD-9MMpb0')}
          disabled={isProcessing}
        >
          Use Example Video
        </button>
      </div>
    </div>
  );
}

export default VideoInput;
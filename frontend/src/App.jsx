import { useState, useRef } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import UploadZone from './components/UploadZone';
import ResultCard from './components/ResultCard';
import ImageViewer from './components/ImageViewer';
import ConfidenceChart from './components/ConfidenceChart';
import Suggestions from './components/Suggestions';
import Footer from './components/Footer';
import './App.css';

const API_BASE = '';

export default function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const resultsRef = useRef(null);

  const handleAnalyze = async (file) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Analysis failed (HTTP ${response.status})`);
      }

      const data = await response.json();
      setResult(data);

      // Scroll to results
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 200);

    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.message || 'Failed to analyze image. Make sure the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Navbar />
      <Hero />
      <UploadZone onAnalyze={handleAnalyze} isLoading={isLoading} />

      {/* Loading state */}
      {isLoading && (
        <div className="loading-section container">
          <div className="loading-card glass-card">
            <div className="loading-card__eye">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
            </div>
            <h3 className="loading-card__title">Analyzing Retinal Image</h3>
            <p className="loading-card__text">Running EfficientNet-B4 inference and generating Grad-CAM heatmap...</p>
            <div className="loading-card__bar">
              <div className="loading-card__bar-fill" />
            </div>
          </div>
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="error-section container">
          <div className="error-card glass-card">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#e74c3c" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <div className="error-card__content">
              <h4>Analysis Failed</h4>
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="results-section container" ref={resultsRef} id="results">
          <div className="results-divider">
            <span className="results-divider__line" />
            <span className="results-divider__text">Analysis Results</span>
            <span className="results-divider__line" />
          </div>

          <div className="results-grid">
            <div className="results-grid__left">
              <ResultCard result={result} />
              <ConfidenceChart probabilities={result.probabilities} />
            </div>
            <div className="results-grid__right">
              <ImageViewer result={result} />
            </div>
          </div>

          <Suggestions
            suggestions={result.suggestions}
            gradeColor={result.color}
          />
        </div>
      )}

      <Footer />
    </div>
  );
}

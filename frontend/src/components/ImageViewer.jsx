import { useState } from 'react';
import './ImageViewer.css';

export default function ImageViewer({ result }) {
  const [activeTab, setActiveTab] = useState('gradcam');

  if (!result) return null;

  const { preprocessed_image, gradcam_image } = result;

  return (
    <div className="image-viewer glass-card animate-fade-in-up delay-2" id="image-viewer">
      <div className="image-viewer__tabs">
        <button
          className={`image-viewer__tab ${activeTab === 'preprocessed' ? 'image-viewer__tab--active' : ''}`}
          onClick={() => setActiveTab('preprocessed')}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
            <circle cx="8.5" cy="8.5" r="1.5" />
            <polyline points="21 15 16 10 5 21" />
          </svg>
          Preprocessed
        </button>
        <button
          className={`image-viewer__tab ${activeTab === 'gradcam' ? 'image-viewer__tab--active' : ''}`}
          onClick={() => setActiveTab('gradcam')}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
          Grad-CAM Heatmap
        </button>
      </div>

      <div className="image-viewer__body">
        {activeTab === 'preprocessed' ? (
          <div className="image-viewer__panel animate-fade-in">
            <img
              src={`data:image/png;base64,${preprocessed_image}`}
              alt="Ben Graham enhanced retinal image"
              className="image-viewer__img"
            />
            <p className="image-viewer__caption">
              Ben Graham enhanced retinal image with circular mask
            </p>
          </div>
        ) : (
          <div className="image-viewer__panel animate-fade-in">
            <img
              src={`data:image/png;base64,${gradcam_image}`}
              alt="Grad-CAM heatmap"
              className="image-viewer__img"
            />
            <p className="image-viewer__caption">
              <span className="image-viewer__caption-red">Red regions</span> = areas that most influenced the model's prediction
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

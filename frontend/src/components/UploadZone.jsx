import { useState, useRef, useCallback } from 'react';
import './UploadZone.css';

export default function UploadZone({ onAnalyze, isLoading }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleFile = useCallback((selectedFile) => {
    if (!selectedFile) return;
    if (!selectedFile.type.startsWith('image/')) return;

    setFile(selectedFile);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(selectedFile);
  }, []);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, [handleFile]);

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  const handleAnalyze = () => {
    if (file && onAnalyze) {
      onAnalyze(file);
    }
  };

  return (
    <section className="upload-section" id="upload">
      <div className="container">
        <div className="upload-header animate-fade-in-up">
          <h2 className="upload-header__title">Upload Fundus Image</h2>
          <p className="upload-header__desc">
            Drag and drop or browse for a retinal fundus photograph (JPG, PNG)
          </p>
        </div>

        <div className="upload-content">
          {/* Drop zone */}
          <div
            className={`upload-zone glass-card ${dragActive ? 'upload-zone--active' : ''} ${preview ? 'upload-zone--has-file' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => !preview && inputRef.current?.click()}
            id="upload-dropzone"
          >
            <input
              ref={inputRef}
              type="file"
              accept="image/jpeg,image/png,image/jpg"
              onChange={handleChange}
              className="upload-zone__input"
              id="file-input"
            />

            {preview ? (
              <div className="upload-zone__preview animate-fade-in">
                <img src={preview} alt="Uploaded retinal image" className="upload-zone__image" />
                <div className="upload-zone__file-info">
                  <span className="upload-zone__filename">{file?.name}</span>
                  <span className="upload-zone__filesize">
                    {(file?.size / 1024).toFixed(1)} KB • {file?.type.split('/')[1].toUpperCase()}
                  </span>
                </div>
              </div>
            ) : (
              <div className="upload-zone__placeholder">
                <div className="upload-zone__icon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="17 8 12 3 7 8" />
                    <line x1="12" y1="3" x2="12" y2="15" />
                  </svg>
                </div>
                <p className="upload-zone__text">
                  <span className="upload-zone__text-primary">Click to upload</span> or drag and drop
                </p>
                <p className="upload-zone__text-sub">JPG, JPEG, or PNG • Max file size 10MB</p>
              </div>
            )}
          </div>

          {/* Action buttons */}
          {preview && (
            <div className="upload-actions animate-fade-in-up delay-1">
              <button
                className="btn btn--secondary"
                onClick={handleClear}
                disabled={isLoading}
                id="btn-clear"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                </svg>
                Clear
              </button>
              <button
                className="btn btn--primary"
                onClick={handleAnalyze}
                disabled={isLoading}
                id="btn-analyze"
              >
                {isLoading ? (
                  <>
                    <div className="btn__spinner" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
                    </svg>
                    Analyze Image
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

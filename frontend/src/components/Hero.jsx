import './Hero.css';

export default function Hero() {
  return (
    <section className="hero" id="hero">
      <div className="hero__inner container">
        <div className="hero__content animate-fade-in-up">
          <div className="hero__eyebrow">
            <span className="hero__eyebrow-dot" />
            AI-Powered Diagnostics
          </div>
          <h1 className="hero__title">
            Retinal Disease
            <span className="hero__title-accent"> Detection</span>
          </h1>
          <p className="hero__subtitle">
            Upload a retinal fundus image to detect the severity of
            <strong> Diabetic Retinopathy</strong> using our EfficientNet-B4 deep learning model
            with Grad-CAM visualization and AI-powered care recommendations.
          </p>
          <div className="hero__features">
            <div className="hero__feature">
              <span className="hero__feature-icon">🔬</span>
              <span>5-Grade Classification</span>
            </div>
            <div className="hero__feature">
              <span className="hero__feature-icon">🧠</span>
              <span>Grad-CAM Heatmaps</span>
            </div>
            <div className="hero__feature">
              <span className="hero__feature-icon">💡</span>
              <span>AI Care Suggestions</span>
            </div>
          </div>
        </div>

        <div className="hero__visual animate-fade-in-up delay-2">
          <div className="hero__orb hero__orb--1" />
          <div className="hero__orb hero__orb--2" />
          <div className="hero__orb hero__orb--3" />
          <div className="hero__eye-icon">
            <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="url(#heroGrad)" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
              <defs>
                <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#3b82f6" />
                  <stop offset="100%" stopColor="#8b5cf6" />
                </linearGradient>
              </defs>
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          </div>
        </div>
      </div>

      <div className="hero__scroll-indicator animate-fade-in delay-5">
        <span>Upload below</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 5v14M19 12l-7 7-7-7" />
        </svg>
      </div>
    </section>
  );
}

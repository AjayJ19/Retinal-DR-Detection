import { useState, useEffect } from 'react';
import './Navbar.css';

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`navbar ${scrolled ? 'navbar--scrolled' : ''}`} id="navbar">
      <div className="navbar__inner container">
        <div className="navbar__brand">
          <div className="navbar__icon">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <circle cx="12" cy="12" r="6" />
              <circle cx="12" cy="12" r="2" />
            </svg>
          </div>
          <div className="navbar__title">
            <span className="navbar__name">RetinaAI</span>
            <span className="navbar__badge">EfficientNet-B4</span>
          </div>
        </div>

        <div className="navbar__meta">
          <div className="navbar__stat">
            <span className="navbar__stat-label">Accuracy</span>
            <span className="navbar__stat-value">79.82%</span>
          </div>
          <div className="navbar__divider" />
          <div className="navbar__stat">
            <span className="navbar__stat-label">Kappa</span>
            <span className="navbar__stat-value">0.8612</span>
          </div>
          <div className="navbar__divider" />
          <div className="navbar__stat">
            <span className="navbar__stat-label">Dataset</span>
            <span className="navbar__stat-value">APTOS 2019</span>
          </div>
        </div>
      </div>
    </nav>
  );
}

import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer" id="footer">
      <div className="container">
        <div className="footer__inner">
          <div className="footer__brand">
            <div className="footer__logo">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <circle cx="12" cy="12" r="6" />
                <circle cx="12" cy="12" r="2" />
              </svg>
              <span>RetinaAI</span>
            </div>
            <p className="footer__desc">
              AI-powered diabetic retinopathy detection using deep learning.
            </p>
          </div>

          <div className="footer__info">
            <div className="footer__col">
              <h5 className="footer__col-title">Model Info</h5>
              <ul className="footer__list">
                <li>EfficientNet-B4</li>
                <li>APTOS 2019 Dataset</li>
                <li>5-Grade Classification</li>
                <li>Grad-CAM Visualization</li>
              </ul>
            </div>
            <div className="footer__col">
              <h5 className="footer__col-title">DR Grades</h5>
              <ul className="footer__list footer__grades">
                <li><span className="footer__dot" style={{ background: '#2ecc71' }} /> No DR</li>
                <li><span className="footer__dot" style={{ background: '#f1c40f' }} /> Mild</li>
                <li><span className="footer__dot" style={{ background: '#e67e22' }} /> Moderate</li>
                <li><span className="footer__dot" style={{ background: '#e74c3c' }} /> Severe</li>
                <li><span className="footer__dot" style={{ background: '#8e44ad' }} /> Proliferative</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="footer__bottom">
          <p>© {new Date().getFullYear()} RetinaAI — For screening assistance only. Not a substitute for professional medical advice.</p>
        </div>
      </div>
    </footer>
  );
}

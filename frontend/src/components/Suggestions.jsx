import { useState } from 'react';
import './Suggestions.css';

export default function Suggestions({ suggestions, gradeColor }) {
  const [expandedCategory, setExpandedCategory] = useState(null);

  if (!suggestions) return null;

  const { title, summary, recommendations } = suggestions;

  const toggleCategory = (idx) => {
    setExpandedCategory(expandedCategory === idx ? null : idx);
  };

  return (
    <section className="suggestions animate-fade-in-up delay-4" id="suggestions">
      {/* Built-in suggestions */}
      <div className="suggestions__main glass-card" style={{ '--grade-color': gradeColor }}>
        <div className="suggestions__header">
          <div className="suggestions__icon-wrap">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 18V5l12-2v13" /><circle cx="6" cy="18" r="3" /><circle cx="18" cy="16" r="3" />
            </svg>
          </div>
          <div>
            <h3 className="suggestions__title">💡 {title}</h3>
            <p className="suggestions__summary">{summary}</p>
          </div>
        </div>

        <div className="suggestions__categories">
          {recommendations.map((rec, idx) => (
            <div
              key={idx}
              className={`suggestion-category ${expandedCategory === idx ? 'suggestion-category--expanded' : ''}`}
            >
              <button
                className="suggestion-category__header"
                onClick={() => toggleCategory(idx)}
                id={`suggestion-cat-${idx}`}
              >
                <span className="suggestion-category__icon">{rec.icon}</span>
                <span className="suggestion-category__name">{rec.category}</span>
                <span className="suggestion-category__count">{rec.items.length} tips</span>
                <svg className="suggestion-category__arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </button>

              <div className="suggestion-category__body">
                <ul className="suggestion-category__list">
                  {rec.items.map((item, itemIdx) => (
                    <li key={itemIdx} className="suggestion-category__item">
                      <span className="suggestion-category__bullet" style={{ background: gradeColor }} />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Medical Disclaimer */}
      <div className="suggestions__disclaimer">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
          <line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        <p>
          <strong>Medical Disclaimer:</strong> This AI tool is intended for screening assistance only
          and does not replace professional medical diagnosis. Always consult a qualified
          ophthalmologist for medical decisions.
        </p>
      </div>
    </section>
  );
}

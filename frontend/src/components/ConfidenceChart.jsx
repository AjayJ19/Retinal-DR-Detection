import { useEffect, useRef } from 'react';
import './ConfidenceChart.css';

export default function ConfidenceChart({ probabilities }) {
  const chartRef = useRef(null);

  useEffect(() => {
    // Trigger bar animations once mounted
    if (chartRef.current) {
      const bars = chartRef.current.querySelectorAll('.conf-bar__fill');
      bars.forEach((bar, i) => {
        setTimeout(() => {
          bar.style.width = bar.dataset.width;
        }, i * 120);
      });
    }
  }, [probabilities]);

  if (!probabilities) return null;

  const maxConf = Math.max(...probabilities.map(p => p.confidence));

  return (
    <div className="conf-chart glass-card animate-fade-in-up delay-3" id="confidence-chart">
      <h3 className="conf-chart__title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" />
        </svg>
        Confidence Distribution
      </h3>

      <div className="conf-chart__bars" ref={chartRef}>
        {probabilities.map((item) => (
          <div
            key={item.grade}
            className={`conf-bar ${item.confidence === maxConf ? 'conf-bar--active' : ''}`}
          >
            <div className="conf-bar__label">
              <span className="conf-bar__dot" style={{ background: item.color }} />
              <span className="conf-bar__name">{item.name}</span>
              <span className="conf-bar__grade">Grade {item.grade}</span>
            </div>
            <div className="conf-bar__track">
              <div
                className="conf-bar__fill"
                style={{
                  '--bar-color': item.color,
                  width: '0%'
                }}
                data-width={`${item.confidence}%`}
              />
            </div>
            <span className="conf-bar__value" style={{ color: item.confidence === maxConf ? item.color : undefined }}>
              {item.confidence.toFixed(1)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

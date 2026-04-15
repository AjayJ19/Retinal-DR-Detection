import './ResultCard.css';

const URGENCY_ICONS = {
  'Low Risk': '✅',
  'Monitor': '⚠️',
  'Consult Doctor': '⚠️',
  'Urgent Consultation': '🚨',
  'Immediate Attention': '🚨'
};

export default function ResultCard({ result }) {
  if (!result) return null;

  const { grade, grade_name, description, urgency, color, confidence } = result;

  return (
    <div
      className="result-card glass-card animate-fade-in-up"
      style={{
        '--grade-color': color,
        '--grade-glow': `${color}40`
      }}
      id="result-card"
    >
      <div className="result-card__glow" />

      <div className="result-card__header">
        <div className="result-card__grade-badge">
          <span className="result-card__grade-number">Grade {grade}</span>
        </div>
        <h3 className="result-card__title">{grade_name}</h3>
        <div className="result-card__urgency">
          <span>{URGENCY_ICONS[urgency] || '📋'}</span>
          <span>{urgency}</span>
        </div>
      </div>

      <div className="result-card__body">
        <p className="result-card__description">{description}</p>
      </div>

      <div className="result-card__confidence">
        <div className="result-card__confidence-header">
          <span className="result-card__confidence-label">Model Confidence</span>
          <span className="result-card__confidence-value">{confidence.toFixed(1)}%</span>
        </div>
        <div className="result-card__confidence-bar">
          <div
            className="result-card__confidence-fill"
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>
    </div>
  );
}

import './LifetimePanel.css'

interface LifetimePanelProps {
  lifetimeTime: number
  lifetimeFreq: number
  lifetimeNatural: number
  lifetimeDamping: number
  averageLifetime: number
}

function LifetimePanel({ 
  lifetimeTime, 
  lifetimeFreq, 
  lifetimeNatural, 
  lifetimeDamping, 
  averageLifetime 
}: LifetimePanelProps) {
  return (
    <section className="panel">
      <h2>Lifetime Estimates</h2>
      <div className="lifetime-grid">
        <div className="lifetime-item">
          <span className="lifetime-label">Time-Domain:</span>
          <span className="lifetime-value">{lifetimeTime.toFixed(1)} hrs</span>
        </div>
        <div className="lifetime-item">
          <span className="lifetime-label">Frequency-Domain:</span>
          <span className="lifetime-value">{lifetimeFreq.toFixed(1)} hrs</span>
        </div>
        <div className="lifetime-item">
          <span className="lifetime-label">Natural Frequency:</span>
          <span className="lifetime-value">{lifetimeNatural.toFixed(1)} hrs</span>
        </div>
        <div className="lifetime-item">
          <span className="lifetime-label">Damping-Based:</span>
          <span className="lifetime-value">{lifetimeDamping.toFixed(1)} hrs</span>
        </div>
        <div className="lifetime-item average">
          <span className="lifetime-label">Weighted Average:</span>
          <span className="lifetime-value">{averageLifetime.toFixed(1)} hrs</span>
        </div>
      </div>
    </section>
  )
}

export default LifetimePanel

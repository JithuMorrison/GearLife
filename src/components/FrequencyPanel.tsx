import './MetricPanel.css'

interface FrequencyPanelProps {
  naturalFrequency: number
}

function FrequencyPanel({ naturalFrequency }: FrequencyPanelProps) {
  // Baseline natural frequency (from requirements 8.1, 8.4)
  const BASELINE_FREQUENCY = 50.0
  const SHIFT_THRESHOLD = 5.0 // Hz - threshold for showing shift indicator
  
  // Calculate frequency shift from baseline
  const frequencyShift = Math.abs(naturalFrequency - BASELINE_FREQUENCY)
  const hasSignificantShift = frequencyShift > SHIFT_THRESHOLD
  
  // Determine shift direction and severity
  const shiftDirection = naturalFrequency > BASELINE_FREQUENCY ? 'above' : 'below'
  const shiftSeverity = frequencyShift > 10 ? 'critical' : frequencyShift > 5 ? 'warning' : 'normal'
  
  return (
    <section className="panel">
      <h2>Natural Frequency</h2>
      <div className="metric-value">{naturalFrequency.toFixed(2)} Hz</div>
      
      {hasSignificantShift && (
        <div className={`frequency-shift-indicator ${shiftSeverity}`}>
          <span className="shift-icon">⚠</span>
          <span className="shift-text">
            {frequencyShift.toFixed(2)} Hz {shiftDirection} baseline ({BASELINE_FREQUENCY} Hz)
          </span>
        </div>
      )}
      
      {!hasSignificantShift && (
        <div className="frequency-baseline-indicator">
          <span className="baseline-icon">✓</span>
          <span className="baseline-text">Within normal range</span>
        </div>
      )}
    </section>
  )
}

export default FrequencyPanel

import './MetricPanel.css'

interface DampingPanelProps {
  dampingFactor: number
}

function DampingPanel({ dampingFactor }: DampingPanelProps) {
  // Determine color zone based on damping factor value
  // Normal: 0.01 - 0.10, Warning: 0.10 - 0.20, Critical: > 0.20
  const getGaugeClass = (value: number): string => {
    if (value <= 0.10) return 'normal'
    if (value <= 0.20) return 'warning'
    return 'critical'
  }

  // Calculate gauge percentage (0-100) for visualization
  // Map damping factor range 0-0.5 to 0-100%
  const gaugePercentage = Math.min((dampingFactor / 0.5) * 100, 100)
  
  // Calculate needle angle (-90 to 90 degrees)
  const gaugeAngle = (gaugePercentage / 100) * 180 - 90

  return (
    <section className="panel">
      <h2>Damping Factor</h2>
      <div className="gauge-container">
        <div 
          className={`gauge ${getGaugeClass(dampingFactor)}`}
          style={{
            '--gauge-percentage': gaugePercentage,
            '--gauge-angle': gaugeAngle
          } as React.CSSProperties}
        >
          <div className="gauge-value">{dampingFactor.toFixed(4)}</div>
          <div className="gauge-labels">
            <span className="gauge-label min">0.00</span>
            <span className="gauge-label max">0.50</span>
          </div>
        </div>
      </div>
      <div className="metric-value">{dampingFactor.toFixed(4)}</div>
    </section>
  )
}

export default DampingPanel

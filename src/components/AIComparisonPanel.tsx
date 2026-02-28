import './AIComparisonPanel.css'

interface AIComparisonPanelProps {
  aiLifetime: number
  averageLifetime: number
}

function AIComparisonPanel({ aiLifetime, averageLifetime }: AIComparisonPanelProps) {
  const percentDiff = averageLifetime > 0 
    ? Math.abs(aiLifetime - averageLifetime) / averageLifetime * 100
    : 0

  // Determine color coding based on percentage difference
  // Agreement: < 10%, Warning: 10-20%, Divergence: > 20%
  const getComparisonClass = (diff: number): string => {
    if (diff < 10) return 'agreement'
    if (diff < 20) return 'warning'
    return 'divergence'
  }

  const comparisonClass = getComparisonClass(percentDiff)

  return (
    <section className="panel">
      <h2>AI Prediction Comparison</h2>
      <div className="comparison-grid">
        <div className="comparison-item">
          <span className="comparison-label">AI Prediction:</span>
          <span className="comparison-value">{aiLifetime.toFixed(1)} hrs</span>
        </div>
        <div className="comparison-item">
          <span className="comparison-label">Average Lifetime:</span>
          <span className="comparison-value">{averageLifetime.toFixed(1)} hrs</span>
        </div>
        <div className={`comparison-item ${comparisonClass}`}>
          <span className="comparison-label">Difference:</span>
          <span className="comparison-value">{percentDiff.toFixed(1)}%</span>
        </div>
      </div>
    </section>
  )
}

export default AIComparisonPanel

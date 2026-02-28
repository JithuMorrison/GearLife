import './ErrorPanel.css'

interface ErrorPanelProps {
  message: string
  onClose: () => void
}

function ErrorPanel({ message, onClose }: ErrorPanelProps) {
  return (
    <section className="panel error-panel">
      <div className="error-header">
        <h2>System Messages</h2>
        <button className="close-btn" onClick={onClose}>×</button>
      </div>
      <div className="error-message">{message}</div>
    </section>
  )
}

export default ErrorPanel

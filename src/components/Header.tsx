import './Header.css'

interface HeaderProps {
  connected: boolean
}

function Header({ connected }: HeaderProps) {
  return (
    <header className="header">
      <h1>Mechanical System Lifetime Prediction Platform</h1>
      <div className="status-indicator">
        <span className={`status-dot ${connected ? 'connected' : 'disconnected'}`}></span>
        <span className="status-text">{connected ? 'Connected' : 'Disconnected'}</span>
      </div>
    </header>
  )
}

export default Header

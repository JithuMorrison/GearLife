import { useEffect, useState } from 'react'
import './App.css'
import Header from './components/Header'
import TimeChart from './components/TimeChart'
import FrequencyChart from './components/FrequencyChart'
import DampingPanel from './components/DampingPanel'
import FrequencyPanel from './components/FrequencyPanel'
import LifetimePanel from './components/LifetimePanel'
import AIComparisonPanel from './components/AIComparisonPanel'
import ErrorPanel from './components/ErrorPanel'

const BACKEND_URL = 'http://localhost:8000'
const POLL_INTERVAL = 2000 // 2 seconds

interface VibrationData {
  new_data_available: boolean
  time?: number[]
  acceleration?: number[]
  frequency: number[]
  amplitude: number[]
  damping_factor: number
  natural_frequency: number
  lifetime_time: number
  lifetime_freq: number
  lifetime_natural: number
  lifetime_damping: number
  average_lifetime: number
  ai_lifetime: number
}

function App() {
  const [data, setData] = useState<VibrationData | null>(null)
  const [connected, setConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Full refresh on mount
  useEffect(() => {
    fullRefresh()
    const interval = setInterval(pollData, POLL_INTERVAL)
    return () => clearInterval(interval)
  }, [])

  const fullRefresh = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/full-refresh`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const result = await response.json()
      setData(result)
      setConnected(true)
      setError(null)
    } catch (err) {
      console.error('Failed to refresh data:', err)
      setConnected(false)
      setError(`Failed to load data: ${err instanceof Error ? err.message : 'Unknown error'}`)
    }
  }

  const pollData = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/get-data`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const result = await response.json()
      
      if (result.new_data_available) {
        setData(result)
      }
      
      setConnected(true)
      setError(null)
    } catch (err) {
      console.error('Failed to fetch data:', err)
      setConnected(false)
      setError(`Connection error: ${err instanceof Error ? err.message : 'Unknown error'}`)
    }
  }

  return (
    <div className="app">
      {/* Animated gear decorations */}
      <svg className="gear-decoration gear-top-left" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <g className="gear-rotate">
          <circle cx="50" cy="50" r="30" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.3"/>
          <circle cx="50" cy="50" r="20" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.3"/>
          {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => (
            <rect
              key={i}
              x="48"
              y="15"
              width="4"
              height="15"
              fill="currentColor"
              opacity="0.3"
              transform={`rotate(${angle} 50 50)`}
            />
          ))}
        </g>
      </svg>
      
      <svg className="gear-decoration gear-top-right" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <g className="gear-rotate-reverse">
          <circle cx="50" cy="50" r="25" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.2"/>
          <circle cx="50" cy="50" r="15" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.2"/>
          {[0, 60, 120, 180, 240, 300].map((angle, i) => (
            <rect
              key={i}
              x="48"
              y="20"
              width="4"
              height="12"
              fill="currentColor"
              opacity="0.2"
              transform={`rotate(${angle} 50 50)`}
            />
          ))}
        </g>
      </svg>
      
      <svg className="gear-decoration gear-bottom-left" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <g className="gear-rotate">
          <circle cx="50" cy="50" r="28" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.25"/>
          <circle cx="50" cy="50" r="18" fill="none" stroke="currentColor" strokeWidth="2" opacity="0.25"/>
          {[0, 40, 80, 120, 160, 200, 240, 280, 320].map((angle, i) => (
            <rect
              key={i}
              x="48"
              y="18"
              width="4"
              height="14"
              fill="currentColor"
              opacity="0.25"
              transform={`rotate(${angle} 50 50)`}
            />
          ))}
        </g>
      </svg>

      <Header connected={connected} />
      
      <main className="dashboard">
        <TimeChart 
          time={data?.time || []} 
          acceleration={data?.acceleration || []} 
        />
        
        <FrequencyChart 
          frequency={data?.frequency || []} 
          amplitude={data?.amplitude || []}
          naturalFrequency={data?.natural_frequency || 0}
        />
        
        <DampingPanel dampingFactor={data?.damping_factor || 0} />
        
        <FrequencyPanel naturalFrequency={data?.natural_frequency || 0} />
        
        <LifetimePanel
          lifetimeTime={data?.lifetime_time || 0}
          lifetimeFreq={data?.lifetime_freq || 0}
          lifetimeNatural={data?.lifetime_natural || 0}
          lifetimeDamping={data?.lifetime_damping || 0}
          averageLifetime={data?.average_lifetime || 0}
        />
        
        <AIComparisonPanel
          aiLifetime={data?.ai_lifetime || 0}
          averageLifetime={data?.average_lifetime || 0}
        />
        
        {error && <ErrorPanel message={error} onClose={() => setError(null)} />}
      </main>
    </div>
  )
}

export default App

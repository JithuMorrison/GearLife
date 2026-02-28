import { useEffect, useRef } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  type ChartOptions,
  type Plugin,
} from 'chart.js'
import { Line } from 'react-chartjs-2'
import './Chart.css'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

interface FrequencyChartProps {
  frequency: number[]
  amplitude: number[]
  naturalFrequency: number
}

function FrequencyChart({ frequency, amplitude, naturalFrequency }: FrequencyChartProps) {
  const chartRef = useRef<ChartJS<'line'>>(null)

  // Incremental update: when new data arrives, update the chart
  useEffect(() => {
    if (chartRef.current && frequency.length > 0) {
      const chart = chartRef.current
      chart.data.labels = frequency
      chart.data.datasets[0].data = amplitude
      chart.update('none') // Update without animation for better performance
    }
  }, [frequency, amplitude, naturalFrequency])

  // Custom plugin to highlight natural frequency peak
  const naturalFrequencyPlugin: Plugin<'line'> = {
    id: 'naturalFrequencyMarker',
    afterDatasetsDraw: (chart) => {
      if (naturalFrequency <= 0 || frequency.length === 0) return

      const ctx = chart.ctx
      const xScale = chart.scales.x
      const yScale = chart.scales.y

      // Find the index closest to natural frequency
      let closestIndex = 0
      let minDiff = Math.abs(frequency[0] - naturalFrequency)
      
      for (let i = 1; i < frequency.length; i++) {
        const diff = Math.abs(frequency[i] - naturalFrequency)
        if (diff < minDiff) {
          minDiff = diff
          closestIndex = i
        }
      }

      const x = xScale.getPixelForValue(frequency[closestIndex])
      const y = yScale.getPixelForValue(amplitude[closestIndex])

      // Draw vertical line at natural frequency
      ctx.save()
      ctx.strokeStyle = '#ff6b6b'
      ctx.lineWidth = 2
      ctx.setLineDash([5, 5])
      ctx.beginPath()
      ctx.moveTo(x, yScale.top)
      ctx.lineTo(x, yScale.bottom)
      ctx.stroke()
      ctx.setLineDash([])

      // Draw marker circle at peak
      ctx.fillStyle = '#ff6b6b'
      ctx.strokeStyle = '#fff'
      ctx.lineWidth = 2
      ctx.beginPath()
      ctx.arc(x, y, 6, 0, 2 * Math.PI)
      ctx.fill()
      ctx.stroke()

      // Draw label
      ctx.fillStyle = '#ff6b6b'
      ctx.font = "bold 11px 'Roboto Mono', monospace"
      ctx.textAlign = 'center'
      ctx.fillText(`${naturalFrequency.toFixed(2)} Hz`, x, yScale.top - 5)

      ctx.restore()
    },
  }

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false, // Disable animation for real-time updates
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
      tooltip: {
        enabled: true,
        mode: 'nearest',
        intersect: false,
        callbacks: {
          label: (context) => {
            const value = context.parsed.y
            return value !== null ? `Amplitude: ${value.toFixed(4)}` : 'Amplitude: N/A'
          },
          title: (context) => {
            const value = context[0]?.parsed.x
            return value !== null && value !== undefined ? `Frequency: ${value.toFixed(2)} Hz` : 'Frequency: N/A'
          },
        },
      },
    },
    scales: {
      x: {
        type: 'linear',
        title: {
          display: true,
          text: 'Frequency (Hz)',
          color: '#00d9ff',
          font: {
            family: "'Roboto Mono', monospace",
            size: 12,
          },
        },
        ticks: {
          color: '#888',
          font: {
            family: "'Roboto Mono', monospace",
          },
        },
        grid: {
          color: 'rgba(0, 217, 255, 0.1)',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Amplitude',
          color: '#00d9ff',
          font: {
            family: "'Roboto Mono', monospace",
            size: 12,
          },
        },
        ticks: {
          color: '#888',
          font: {
            family: "'Roboto Mono', monospace",
          },
        },
        grid: {
          color: 'rgba(0, 217, 255, 0.1)',
        },
      },
    },
    elements: {
      point: {
        radius: 0, // Hide points for better performance
      },
      line: {
        borderWidth: 1.5,
      },
    },
  }

  const data = {
    labels: frequency,
    datasets: [
      {
        label: 'Amplitude',
        data: amplitude,
        borderColor: '#00d9ff',
        backgroundColor: 'rgba(0, 217, 255, 0.1)',
        tension: 0.2, // Slight smoothing for frequency spectrum
        fill: true,
      },
    ],
  }

  return (
    <section className="panel">
      <h2>Frequency Spectrum</h2>
      <div className="chart-container">
        {frequency.length > 0 ? (
          <Line 
            ref={chartRef} 
            options={options} 
            data={data} 
            plugins={[naturalFrequencyPlugin]}
          />
        ) : (
          <div className="chart-placeholder">
            <p>Waiting for data...</p>
          </div>
        )}
      </div>
    </section>
  )
}

export default FrequencyChart

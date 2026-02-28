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

interface TimeChartProps {
  time: number[]
  acceleration: number[]
}

function TimeChart({ time, acceleration }: TimeChartProps) {
  const chartRef = useRef<ChartJS<'line'>>(null)

  // Incremental update: when new data arrives, update the chart
  useEffect(() => {
    if (chartRef.current && time.length > 0) {
      const chart = chartRef.current
      chart.data.labels = time
      chart.data.datasets[0].data = acceleration
      chart.update('none') // Update without animation for better performance
    }
  }, [time, acceleration])

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
      },
    },
    scales: {
      x: {
        type: 'linear',
        title: {
          display: true,
          text: 'Time (s)',
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
          text: 'Acceleration (m/s²)',
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
        radius: 0, // Hide points for better performance with large datasets
      },
      line: {
        borderWidth: 1.5,
      },
    },
  }

  const data = {
    labels: time,
    datasets: [
      {
        label: 'Acceleration',
        data: acceleration,
        borderColor: '#00d9ff',
        backgroundColor: 'rgba(0, 217, 255, 0.1)',
        tension: 0, // Straight lines for signal data
      },
    ],
  }

  return (
    <section className="panel">
      <h2>Time-Domain Signal</h2>
      <div className="chart-container">
        {time.length > 0 ? (
          <Line ref={chartRef} options={options} data={data} />
        ) : (
          <div className="chart-placeholder">
            <p>Waiting for data...</p>
          </div>
        )}
      </div>
    </section>
  )
}

export default TimeChart


import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts'

function Dashboard(){
  const [progress, setProgress] = useState<any>({metrics:0, score:0, status:'idle'})
  const [data, setData] = useState<any[]>([])
  useEffect(()=>{
    // Example: connect to websocket for audit_run_id=1
    const ws = new WebSocket((location.origin.replace('http','ws')) + '/ws/audit-progress/1')
    ws.onmessage = (e)=>{
      const p = JSON.parse(e.data)
      setProgress(p)
      setData(d=>[...d, {x:d.length, score:p.score}])
    }
    return ()=>ws.close()
  },[])
  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold">Real-time Audit Dashboard</h1>
      <p className="mt-2">Status: <b>{progress.status}</b> | Metrics: <b>{progress.metrics}</b> | Score: <b>{progress.score?.toFixed?.(2)}</b></p>
      <div className="mt-4 bg-white p-4 rounded shadow">
        <LineChart width={600} height={280} data={data}>
          <Line type="monotone" dataKey="score" stroke="#0ea5e9" />
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="x" /><YAxis /><Tooltip />
        </LineChart>
      </div>
    </div>
  )
}

createRoot(document.getElementById('root')!).render(<Dashboard />)

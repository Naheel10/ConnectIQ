import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

export function SetupPage() {
  const [demo, setDemo] = useState(true)
  const [status, setStatus] = useState('')
  const run = async () => {
    const r = await api(`/sync/run?demo_mode=${demo}`, { method: 'POST' })
    setStatus(JSON.stringify(r))
  }
  return <div className='page'><h2>Setup</h2><button onClick={()=>window.location.href='/api/salesforce/oauth/start'}>Connect Salesforce</button><label><input type='checkbox' checked={demo} onChange={e=>setDemo(e.target.checked)} />Demo mode</label><button onClick={run}>Run Sync</button><pre>{status}</pre><Link to='/chat'>Go Chat</Link></div>
}

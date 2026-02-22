import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

export function ChatPage() {
  const [message, setMessage] = useState('What is my pipeline status?')
  const [answer, setAnswer] = useState('')
  const [cites, setCites] = useState<any[]>([])
  const ask = async () => {
    const r = await api('/chat', { method: 'POST', body: JSON.stringify({ message }) })
    setAnswer(r.answer); setCites(r.citations)
  }
  return <div className='page'><h2>Chat</h2><textarea value={message} onChange={e=>setMessage(e.target.value)} /><button onClick={ask}>Ask</button><p>{answer}</p><h3>Citations</h3><ul>{cites.map((c,i)=><li key={i}>{c.source_type} {c.source_sf_id} - {c.display}</li>)}</ul><Link to='/records'>View records</Link></div>
}

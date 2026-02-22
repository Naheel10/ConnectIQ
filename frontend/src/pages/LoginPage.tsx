import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, saveToken } from '../api/client'

export function LoginPage() {
  const [email, setEmail] = useState('demo@connectiq.local')
  const [password, setPassword] = useState('password123')
  const nav = useNavigate()
  const submit = async (e: FormEvent) => {
    e.preventDefault()
    const resp = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
    saveToken(resp.token)
    nav('/setup')
  }
  return <form className='card' onSubmit={submit}><h2>ConnectIQ Login</h2><input value={email} onChange={e=>setEmail(e.target.value)} /><input type='password' value={password} onChange={e=>setPassword(e.target.value)} /><button>Login</button></form>
}

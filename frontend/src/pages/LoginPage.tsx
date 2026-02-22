import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, saveToken } from '../api/client'

function extractErrorMessage(raw: string) {
  try {
    const parsed = JSON.parse(raw)
    if (typeof parsed?.detail === 'string') return parsed.detail
    if (Array.isArray(parsed?.detail)) {
      return parsed.detail.map((err: { msg?: string; loc?: string[] }) => `${err.loc?.join('.')}: ${err.msg}`).join('\n')
    }
  } catch {
    return raw
  }
  return raw
}

export function LoginPage() {
  const [email, setEmail] = useState('demo@connectiq.com')
  const [password, setPassword] = useState('password123')
  const [error, setError] = useState<string | null>(null)
  const nav = useNavigate()

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    try {
      const resp = await api('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
      saveToken(resp.token)
      nav('/setup')
    } catch (err) {
      const message = err instanceof Error ? extractErrorMessage(err.message) : 'Login failed'
      setError(message)
    }
  }

  return <form className='card' onSubmit={submit}><h2>ConnectIQ Login</h2><input value={email} onChange={e=>setEmail(e.target.value)} /><input type='password' value={password} onChange={e=>setPassword(e.target.value)} /><button>Login</button>{error && <pre>{error}</pre>}</form>
}

import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, saveToken } from '../api/client'

export function LoginPage() {
  const [email, setEmail] = useState('demo@connectiq.com')
  const [password, setPassword] = useState('password123')
  const [error, setError] = useState<string | null>(null)
  const nav = useNavigate()

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!email.trim() || !password.trim()) {
      setError('Email and password are required.')
      return
    }

    try {
      const resp = await api('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
      saveToken(resp.token)
      nav('/setup')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    }
  }

  return (
    <div className='flex min-h-screen items-center justify-center bg-slate-100 px-4'>
      <form className='w-full max-w-md rounded-xl border border-slate-200 bg-white p-6 shadow-sm' onSubmit={submit}>
        <h2 className='text-2xl font-semibold text-slate-900'>ConnectIQ Login</h2>
        <p className='mt-1 text-sm text-slate-500'>Sign in to run setup, chat, and inspect synced records.</p>

        <label className='mt-5 block text-sm font-medium text-slate-700'>Email</label>
        <input className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2' value={email} onChange={(e) => setEmail(e.target.value)} />

        <label className='mt-4 block text-sm font-medium text-slate-700'>Password</label>
        <input
          className='mt-1 w-full rounded-md border border-slate-300 px-3 py-2'
          type='password'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <p className='mt-3 rounded-md border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700'>{error}</p>}

        <button className='mt-5 w-full rounded-md bg-indigo-600 px-4 py-2.5 font-medium text-white hover:bg-indigo-700'>Login</button>
      </form>
    </div>
  )
}

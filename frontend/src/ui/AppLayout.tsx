import { Link, useLocation, useNavigate } from 'react-router-dom'
import { clearToken } from '../api/client'
import { ReactNode } from 'react'

const navItems = [
  { to: '/setup', label: 'Setup' },
  { to: '/chat', label: 'Chat' },
  { to: '/records', label: 'Records' },
]

export function AppLayout({ title, children }: { title: string; children: ReactNode }) {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <div className='min-h-screen bg-slate-100 text-slate-800'>
      <header className='border-b border-slate-200 bg-white/95 backdrop-blur'>
        <div className='mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4'>
          <div className='flex items-center gap-2'>
            <div className='h-8 w-8 rounded-md bg-indigo-600' />
            <span className='text-lg font-semibold'>ConnectIQ</span>
          </div>
          <nav className='flex items-center gap-2'>
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className={`rounded-md px-3 py-2 text-sm font-medium transition ${
                  location.pathname === item.to
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                {item.label}
              </Link>
            ))}
            <button
              onClick={() => {
                clearToken()
                navigate('/login')
              }}
              className='rounded-md px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 hover:text-slate-900'
            >
              Logout
            </button>
          </nav>
        </div>
      </header>
      <main className='mx-auto w-full max-w-6xl px-6 py-8'>
        <h1 className='mb-6 text-2xl font-semibold text-slate-900'>{title}</h1>
        {children}
      </main>
    </div>
  )
}

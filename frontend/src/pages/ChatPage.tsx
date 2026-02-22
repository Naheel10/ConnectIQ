import { useState } from 'react'
import { api } from '../api/client'
import { AppLayout } from '../ui/AppLayout'
import { useToast } from '../ui/ToastProvider'

type Citation = { source_type: string; source_sf_id: string; display: string }

type Message = {
  role: 'user' | 'assistant'
  content: string
  citations?: Citation[]
}

export function ChatPage() {
  const [message, setMessage] = useState('What is my pipeline status?')
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const { notifyError } = useToast()

  const ask = async () => {
    if (!message.trim()) return
    const userMessage = message.trim()
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setMessage('')

    try {
      setLoading(true)
      const r = await api('/chat', { method: 'POST', body: JSON.stringify({ message: userMessage }) })
      setMessages((prev) => [...prev, { role: 'assistant', content: r.answer, citations: r.citations }])
    } catch (err) {
      notifyError(err instanceof Error ? err.message : 'Chat request failed')
    } finally {
      setLoading(false)
    }
  }

  const latestAnswer = [...messages].reverse().find((m) => m.role === 'assistant')

  return (
    <AppLayout title='Chat'>
      <div className='grid gap-4 lg:grid-cols-[2fr_1fr]'>
        <section className='relative flex h-[70vh] flex-col rounded-xl border border-slate-200 bg-white shadow-sm'>
          <div className='flex-1 space-y-4 overflow-y-auto p-4 pb-24'>
            {messages.length === 0 ? <p className='text-sm text-slate-500'>Ask a question to start the conversation.</p> : null}
            {messages.map((item, i) => (
              <div key={i} className={`max-w-[85%] rounded-lg px-4 py-3 text-sm ${item.role === 'user' ? 'ml-auto bg-indigo-600 text-white' : 'bg-slate-100 text-slate-700'}`}>
                <p>{item.content}</p>
                {item.role === 'assistant' && item.citations?.length ? (
                  <p className='mt-2 text-xs text-slate-500'>Citations: {item.citations.map((c) => c.source_sf_id).join(', ')}</p>
                ) : null}
              </div>
            ))}
            {loading ? <p className='animate-pulse text-sm text-slate-400'>Generating answer…</p> : null}
          </div>

          <div className='absolute inset-x-0 bottom-0 border-t border-slate-200 bg-white p-3'>
            <div className='flex gap-2'>
              <textarea
                className='h-12 flex-1 resize-none rounded-md border border-slate-300 px-3 py-2 text-sm'
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder='Ask about pipeline, risk, forecast…'
              />
              <button onClick={ask} className='rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white'>
                Ask
              </button>
            </div>
          </div>
        </section>

        <aside className='rounded-xl border border-slate-200 bg-white p-4 shadow-sm'>
          <h3 className='font-semibold text-slate-900'>Sources</h3>
          {!latestAnswer?.citations?.length ? (
            <p className='mt-3 text-sm text-slate-500'>Sources will appear here after an answer is generated.</p>
          ) : (
            <ul className='mt-3 space-y-3'>
              {latestAnswer.citations.map((c, i) => (
                <li key={`${c.source_sf_id}-${i}`} className='rounded-md border border-slate-200 p-3'>
                  <div className='mb-2 flex flex-wrap gap-2'>
                    <span className='rounded-full bg-indigo-50 px-2 py-1 text-xs font-medium text-indigo-700'>{c.source_type}</span>
                    <span className='rounded-full bg-slate-100 px-2 py-1 text-xs text-slate-700'>{c.source_sf_id}</span>
                  </div>
                  <p className='text-sm text-slate-600'>{c.display}</p>
                </li>
              ))}
            </ul>
          )}
        </aside>
      </div>
    </AppLayout>
  )
}

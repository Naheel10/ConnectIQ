import { useEffect, useMemo, useState } from 'react'
import { api } from '../api/client'
import { AppLayout } from '../ui/AppLayout'
import { useToast } from '../ui/ToastProvider'

type Tab = 'opportunities' | 'contacts'

export function RecordsPage() {
  const [tab, setTab] = useState<Tab>('opportunities')
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('')
  const [opps, setOpps] = useState<any[]>([])
  const [contacts, setContacts] = useState<any[]>([])
  const { notifyError } = useToast()

  useEffect(() => {
    const load = async () => {
      try {
        const [oppData, contactData] = await Promise.all([api('/records/opportunities'), api('/records/contacts')])
        setOpps(oppData)
        setContacts(contactData)
      } catch (err) {
        notifyError(err instanceof Error ? err.message : 'Failed to load records')
      }
    }
    load()
  }, [])

  const filteredOpps = useMemo(
    () => opps.filter((o) => `${o.name} ${o.stage_name}`.toLowerCase().includes(search.toLowerCase()) && (!filter || o.stage_name === filter)),
    [opps, search, filter]
  )

  const filteredContacts = useMemo(
    () => contacts.filter((c) => `${c.first_name} ${c.last_name} ${c.email}`.toLowerCase().includes(search.toLowerCase()) && (!filter || c.account_name === filter)),
    [contacts, search, filter]
  )

  return (
    <AppLayout title='Records'>
      <section className='rounded-xl border border-slate-200 bg-white p-4 shadow-sm'>
        <div className='mb-4 flex flex-wrap items-center gap-2'>
          <button
            onClick={() => {
              setTab('opportunities')
              setFilter('')
            }}
            className={`rounded-md px-3 py-2 text-sm font-medium ${tab === 'opportunities' ? 'bg-indigo-50 text-indigo-700' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            Opportunities
          </button>
          <button
            onClick={() => {
              setTab('contacts')
              setFilter('')
            }}
            className={`rounded-md px-3 py-2 text-sm font-medium ${tab === 'contacts' ? 'bg-indigo-50 text-indigo-700' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            Contacts
          </button>
          <input
            className='ml-auto min-w-60 rounded-md border border-slate-300 px-3 py-2 text-sm'
            placeholder='Search records'
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <input
            className='rounded-md border border-slate-300 px-3 py-2 text-sm'
            placeholder={tab === 'opportunities' ? 'Filter stage' : 'Filter account'}
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
        </div>

        <div className='max-h-[60vh] overflow-auto'>
          {tab === 'opportunities' ? (
            <table className='w-full border-collapse text-left text-sm'>
              <thead className='sticky top-0 bg-slate-50 text-slate-500'>
                <tr>
                  <th className='px-3 py-2'>Name</th>
                  <th className='px-3 py-2'>Stage</th>
                  <th className='px-3 py-2'>Amount</th>
                </tr>
              </thead>
              <tbody>
                {filteredOpps.map((o) => (
                  <tr key={o.id} className='border-t border-slate-100'>
                    <td className='px-3 py-2'>{o.name}</td>
                    <td className='px-3 py-2'>{o.stage_name}</td>
                    <td className='px-3 py-2'>{o.amount}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <table className='w-full border-collapse text-left text-sm'>
              <thead className='sticky top-0 bg-slate-50 text-slate-500'>
                <tr>
                  <th className='px-3 py-2'>Name</th>
                  <th className='px-3 py-2'>Email</th>
                  <th className='px-3 py-2'>Account</th>
                </tr>
              </thead>
              <tbody>
                {filteredContacts.map((c) => (
                  <tr key={c.id} className='border-t border-slate-100'>
                    <td className='px-3 py-2'>
                      {c.first_name} {c.last_name}
                    </td>
                    <td className='px-3 py-2'>{c.email}</td>
                    <td className='px-3 py-2'>{c.account_name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </section>
    </AppLayout>
  )
}

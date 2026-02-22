import { useEffect, useState } from 'react'
import { AppLayout } from '../ui/AppLayout'
import { api } from '../api/client'
import { useToast } from '../ui/ToastProvider'

type SyncStatus = {
  status: string
  started_at?: string
  finished_at?: string
  counts?: { opportunities: number; contacts: number; documents: number }
  error?: string
}

export function SetupPage() {
  const [demo, setDemo] = useState(true)
  const [syncing, setSyncing] = useState(false)
  const [status, setStatus] = useState<SyncStatus>({ status: 'never' })
  const [sfConnected, setSfConnected] = useState(false)
  const { notifyError } = useToast()

  const loadStatus = async () => {
    try {
      const resp = await api('/sync/status')
      setStatus(resp)
      setSfConnected(resp.status !== 'never')
    } catch (err) {
      notifyError(err instanceof Error ? err.message : 'Unable to load sync status')
    }
  }

  useEffect(() => {
    loadStatus()
  }, [])

  const run = async () => {
    try {
      setSyncing(true)
      await api(`/sync/run?demo_mode=${demo}`, { method: 'POST' })
      await loadStatus()
    } catch (err) {
      notifyError(err instanceof Error ? err.message : 'Sync failed')
    } finally {
      setSyncing(false)
    }
  }

  return (
    <AppLayout title='Setup'>
      <div className='grid gap-4 md:grid-cols-3'>
        <section className='rounded-xl border border-slate-200 bg-white p-4 shadow-sm'>
          <h3 className='font-semibold text-slate-900'>Connect Salesforce</h3>
          <p className='mt-1 text-sm text-slate-500'>Use OAuth to pull live Salesforce opportunities and contacts.</p>
          <div className='mt-3 inline-flex items-center rounded-full bg-slate-100 px-3 py-1 text-sm'>
            <span className={`mr-2 h-2 w-2 rounded-full ${sfConnected ? 'bg-emerald-500' : 'bg-slate-400'}`} />
            {sfConnected ? 'Connected' : 'Not connected'}
          </div>
          <button
            onClick={() => (window.location.href = '/api/salesforce/oauth/start')}
            className='mt-4 w-full rounded-md border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-50'
          >
            Connect Salesforce
          </button>
        </section>

        <section className='rounded-xl border border-slate-200 bg-white p-4 shadow-sm'>
          <h3 className='font-semibold text-slate-900'>Demo mode</h3>
          <p className='mt-1 text-sm text-slate-500'>Use seeded demo data when Salesforce is unavailable.</p>
          <button
            onClick={() => setDemo((d) => !d)}
            className={`mt-4 inline-flex w-full items-center justify-between rounded-md border px-4 py-2 text-sm font-medium ${
              demo ? 'border-indigo-200 bg-indigo-50 text-indigo-700' : 'border-slate-300 text-slate-600'
            }`}
          >
            <span>{demo ? 'Enabled' : 'Disabled'}</span>
            <span className={`h-2.5 w-2.5 rounded-full ${demo ? 'bg-indigo-500' : 'bg-slate-400'}`} />
          </button>
        </section>

        <section className='rounded-xl border border-slate-200 bg-white p-4 shadow-sm'>
          <h3 className='font-semibold text-slate-900'>Run Sync</h3>
          <p className='mt-1 text-sm text-slate-500'>Trigger data ingestion and embedding updates.</p>
          <button
            onClick={run}
            disabled={syncing}
            className='mt-4 w-full rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-60'
          >
            {syncing ? 'Syncing…' : 'Run Sync'}
          </button>
          <p className='mt-3 text-xs text-slate-500'>Last sync: {status.finished_at ? new Date(status.finished_at).toLocaleString() : 'Never'}</p>
        </section>
      </div>

      <section className='mt-6 rounded-xl border border-slate-200 bg-white p-4 shadow-sm'>
        <h3 className='mb-3 font-semibold text-slate-900'>Sync Status</h3>
        <table className='w-full text-left text-sm'>
          <thead className='bg-slate-50 text-slate-500'>
            <tr>
              <th className='px-3 py-2'>Status</th>
              <th className='px-3 py-2'>Opportunities</th>
              <th className='px-3 py-2'>Contacts</th>
              <th className='px-3 py-2'>Documents</th>
            </tr>
          </thead>
          <tbody>
            <tr className='border-t border-slate-100'>
              <td className='px-3 py-2 capitalize'>{status.status}</td>
              <td className='px-3 py-2'>{status.counts?.opportunities ?? 0}</td>
              <td className='px-3 py-2'>{status.counts?.contacts ?? 0}</td>
              <td className='px-3 py-2'>{status.counts?.documents ?? 0}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </AppLayout>
  )
}

import { useEffect, useState } from 'react'
import { api } from '../api/client'

export function RecordsPage() {
  const [opps, setOpps] = useState<any[]>([])
  const [contacts, setContacts] = useState<any[]>([])
  useEffect(() => { api('/records/opportunities').then(setOpps); api('/records/contacts').then(setContacts) }, [])
  return <div className='page'><h2>Records</h2><h3>Opportunities</h3><table><tbody>{opps.map(o=><tr key={o.id}><td>{o.name}</td><td>{o.stage_name}</td><td>{o.amount}</td></tr>)}</tbody></table><h3>Contacts</h3><table><tbody>{contacts.map(c=><tr key={c.id}><td>{c.first_name} {c.last_name}</td><td>{c.email}</td></tr>)}</tbody></table></div>
}

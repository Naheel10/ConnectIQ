const tokenKey = 'connectiq_token'

export const saveToken = (t: string) => localStorage.setItem(tokenKey, t)
export const getToken = () => localStorage.getItem(tokenKey)

export async function api(path: string, opts: RequestInit = {}) {
  const token = getToken()
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...(opts.headers as Record<string, string> || {}) }
  if (token) headers.Authorization = `Bearer ${token}`
  const url = path.startsWith('/api/') ? path : `/api${path}`
  const resp = await fetch(url, { ...opts, headers })
  if (!resp.ok) throw new Error(await resp.text())
  return resp.json()
}

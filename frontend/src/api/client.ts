const tokenKey = 'connectiq_token'

export const saveToken = (t: string) => localStorage.setItem(tokenKey, t)
export const getToken = () => localStorage.getItem(tokenKey)
export const clearToken = () => localStorage.removeItem(tokenKey)

export function extractErrorMessage(raw: string) {
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

export async function api(path: string, opts: RequestInit = {}) {
  const token = getToken()
  const headers: Record<string, string> = { 'Content-Type': 'application/json', ...((opts.headers as Record<string, string>) || {}) }
  if (token) headers.Authorization = `Bearer ${token}`
  const url = path.startsWith('/api/') ? path : `/api${path}`
  const resp = await fetch(url, { ...opts, headers })
  if (!resp.ok) throw new Error(extractErrorMessage(await resp.text()))
  return resp.json()
}

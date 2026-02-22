import { createContext, ReactNode, useContext, useMemo, useState } from 'react'

type Toast = { id: number; message: string }

const ToastContext = createContext<{ notifyError: (message: string) => void }>({ notifyError: () => {} })

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const value = useMemo(
    () => ({
      notifyError: (message: string) => {
        const id = Date.now()
        setToasts((prev) => [...prev, { id, message }])
        window.setTimeout(() => setToasts((prev) => prev.filter((toast) => toast.id !== id)), 3500)
      },
    }),
    []
  )

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className='fixed right-4 top-4 z-50 flex w-96 max-w-[90vw] flex-col gap-2'>
        {toasts.map((toast) => (
          <div key={toast.id} className='rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 shadow'>
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export function useToast() {
  return useContext(ToastContext)
}

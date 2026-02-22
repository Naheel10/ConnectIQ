import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { LoginPage } from './pages/LoginPage'
import { SetupPage } from './pages/SetupPage'
import { ChatPage } from './pages/ChatPage'
import { RecordsPage } from './pages/RecordsPage'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      <Route path='/login' element={<LoginPage />} />
      <Route path='/setup' element={<SetupPage />} />
      <Route path='/chat' element={<ChatPage />} />
      <Route path='/records' element={<RecordsPage />} />
      <Route path='*' element={<Navigate to='/login' />} />
    </Routes>
  </BrowserRouter>
)

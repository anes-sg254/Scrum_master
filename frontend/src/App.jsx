import { useEffect, useState } from 'react'
import Login from './pages/Login'
import UserDashboard from './pages/UserDashboard'
import AdminDashboard from './pages/AdminDashboard'
import axios from 'axios'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [role, setRole] = useState("")

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.get("http://127.0.0.1:3000/auth/me", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        setRole(res.data.role) 
        setIsLoggedIn(true)
      })
      .catch(() => {
        setIsLoggedIn(false)
      })
    }
  }, [])

  const handleLogin = (token) => {
    localStorage.setItem('token', token)
    setIsLoggedIn(true)

    axios.get("http://127.0.0.1:3000/auth/me", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setRole(res.data.role))
  }

  const handleLogout = () => {
    localStorage.clear()
    setIsLoggedIn(false)
    setRole("")
  }

  return (
    <>
      {isLoggedIn ? (
        role === "admin" ? (
          <AdminDashboard onLogout={handleLogout} />
        ) : (
          <AdminDashboard onLogout={handleLogout} />
        )
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </>
  )
}

export default App

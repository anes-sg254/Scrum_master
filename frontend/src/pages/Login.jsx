import { useState } from 'react'
import axios from 'axios'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.post('http://127.0.0.1:3000/auth/login', {
        email,
        password
      })
      const { access_token, user_id } = response.data

      // Enregistre le token localement
      localStorage.setItem('token', access_token)
      localStorage.setItem('user_id', user_id)

      //Déclenche le login dans App.jsx
      onLogin(access_token)
    } catch (err) {
      console.log("🔥 Erreur Axios:", err)
      if (err.response) {
        setError(err.response.data.detail || 'Erreur inconnue')
      } else {
        setError('Erreur réseau ou serveur injoignable')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Connexion</h1>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            className="input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Mot de passe"
            className="input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="error-text">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="button-orange"
          >
            {loading ? 'Connexion...' : 'Se connecter'}
          </button>
        </form>
      </div>
    </div>
  )
}

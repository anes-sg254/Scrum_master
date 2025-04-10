import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Dashboard({ onLogout }) {
  const [locations, setLocations] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const userId = localStorage.getItem('user_id')

  useEffect(() => {
    if (!userId) return

    axios.get(`http://127.0.0.1:3000/location/locations/${userId}`)
      .then(res => {
        setLocations(res.data.locations)
      })
      .catch(err => {
        setError("Erreur lors de la récupération des locations ❌")
        console.log("Erreur API:", err)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [userId])

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Mes réservations</h1>

        {error && <p className="error-text">{error}</p>}

        {loading ? (
          <p className="loading">Chargement...</p>
        ) : locations.length > 0 ? (
          <ul className="location-list">
            {locations.map(loc => (
              <li key={loc.id}>
                <strong>{loc.materiel}</strong><br />
                  du {loc.date_debut} au {loc.date_fin || '---'}<br />
                  Statut : {loc.statut}
              </li>
            ))}
          </ul>
        ) : (
          <p>Aucune location pour l’instant.</p>
        )}

        <button onClick={onLogout} className="button-gray">
          Déconnexion
        </button>
      </div>
    </div>
  )
}

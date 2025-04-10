import { useEffect, useState } from 'react'
import axios from 'axios'

export default function AdminDashboard({ onLogout }) {
  const [locations, setLocations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const token = localStorage.getItem("token")

  const fetchLocations = () => {
    axios.get("http://127.0.0.1:3000/location/locationsad", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setLocations(res.data.locations))
    .catch(err => {
      console.error("Erreur chargement locations", err)
      setError("Erreur de chargement.")
    })
    .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchLocations()
  }, [])

  const changerStatut = async (id, statut) => {
    try {
      await axios.patch(`http://127.0.0.1:3000/location/locationsad/${id}?status=${statut}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      fetchLocations()
    } catch (err) {
      console.error("Erreur changement statut :", err)
      setError("Impossible de mettre à jour.")
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Demandes en attente</h1>
        {error && <p className="error-text">{error}</p>}
        {loading ? (
          <p>Chargement...</p>
        ) : locations.length > 0 ? (
          <ul className="materiel-list">
            {locations.map(loc => (
              <li key={loc.id}>
                <strong>{loc.utilisateur}</strong> demande <strong>{loc.materiel}</strong><br />
                Du {loc.date_debut} au {loc.date_fin || "---"}<br />
                <p>
                  <button onClick={() => changerStatut(loc.id, "validée")} className="button-green">Valider</button>
                  {" "}
                  <button onClick={() => changerStatut(loc.id, "refusée")} className="button-red">Refuser</button>
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p>Aucune demande en attente.</p>
        )}
        <button onClick={onLogout} className="button-gray">Déconnexion</button>
      </div>
    </div>
  )
}

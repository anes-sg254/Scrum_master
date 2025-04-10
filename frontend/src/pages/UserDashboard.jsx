import { useEffect, useState } from 'react'
import axios from 'axios'

export default function UserDashboard({ onLogout }) {
  const [materiels, setMateriels] = useState([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState("")
  const [error, setError] = useState("")

  const token = localStorage.getItem("token")
  const userId = localStorage.getItem("user_id")

  useEffect(() => {
    axios.get("http://127.0.0.1:3000/location/materiels/disponibles", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(res => setMateriels(res.data.materiels))
    .catch(err => {
      console.error("Erreur chargement matériels", err)
      setError("Impossible de charger les matériels.")
    })
    .finally(() => setLoading(false))
  }, [])

  const reserverMateriel = async (materiel_id) => {
    try {
      await axios.post("http://127.0.0.1:3000/location/reserver", {
        materiel_id,
        date_fin: "2025-04-30T00:00:00"  // tu peux améliorer ça plus tard
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      setMessage(`Réservation du matériel ${materiel_id} envoyée`)
    } catch (err) {
      console.error("Erreur réservation :", err)
      setError("Erreur lors de la réservation.")
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">Matériels disponibles</h1>
        {error && <p className="error-text">{error}</p>}
        {message && <p className="success-text">{message}</p>}
        {loading ? (
          <p>Chargement...</p>
        ) : materiels.length > 0 ? (
          <ul className="materiel-list">
            {materiels.map(m => (
              <li key={m.id}>
                <strong>{m.nom}</strong> — {m.categorie} <br />
                {m.description}<br />
                <button onClick={() => reserverMateriel(m.id)} className="button-orange">
                  Réserver
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>Aucun matériel disponible.</p>
        )}
        <button onClick={onLogout} className="button-gray">Déconnexion</button>
      </div>
    </div>
  )
}

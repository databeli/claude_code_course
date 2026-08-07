import { useEffect, useState } from 'react'
import { getHistory } from '../api/resume'
import { tierClass } from '../utils/tier'
import TapeIcon from '../components/TapeIcon'

function formatTimestamp(isoString) {
  return new Date(isoString).toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

function LedgerRow({ entry }) {
  return (
    <div className="ledger-row">
      <div className="ledger-row__score">
        <span className="ledger-row__number">{entry.score}</span>
        <span className={`ledger-row__tier tier--${tierClass(entry.tier)}`}>{entry.tier}</span>
      </div>

      <div className="ledger-row__detail">
        <p className="ledger-row__filename">{entry.resume_filename || 'Untitled resume'}</p>
        <p className="ledger-row__jd">{entry.job_description}</p>
      </div>

      <span className="ledger-row__time">{formatTimestamp(entry.created_at)}</span>
    </div>
  )
}

function Archive() {
  const [entries, setEntries] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    getHistory()
      .then((data) => {
        if (!cancelled) setEntries(data)
      })
      .catch((err) => {
        if (!cancelled) setError(err.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [])

  if (loading) {
    return (
      <section className="panel ledger">
        <div className="measuring">
          <div className="measuring__bar" />
          <p className="measuring__text">Loading archive…</p>
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="panel ledger error-panel">
        <p className="error-panel__heading">Couldn't load the archive</p>
        <p className="error-panel__detail">{error}</p>
      </section>
    )
  }

  if (entries.length === 0) {
    return (
      <section className="panel ledger">
        <div className="empty-state">
          <TapeIcon width="56" height="56" />
          <p>Nothing measured yet — analyses you run will collect here.</p>
        </div>
      </section>
    )
  }

  return (
    <section className="panel ledger ledger-panel">
      {entries.map((entry) => (
        <LedgerRow key={entry.id} entry={entry} />
      ))}
    </section>
  )
}

export default Archive

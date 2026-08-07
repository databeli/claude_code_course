import { useEffect, useState } from 'react'
import { tierClass } from '../utils/tier'

const TICKS = Array.from({ length: 11 }, (_, i) => i * 10)

function FitGauge({ score, tier }) {
  const clamped = Math.max(0, Math.min(100, score))
  const [displayScore, setDisplayScore] = useState(0)

  useEffect(() => {
    const frame = requestAnimationFrame(() => setDisplayScore(clamped))
    return () => cancelAnimationFrame(frame)
  }, [clamped])

  return (
    <div className="fit-gauge">
      <div className="fit-gauge__track">
        {TICKS.map((tick) => (
          <span
            key={tick}
            className={tick % 20 === 0 ? 'fit-gauge__tick fit-gauge__tick--major' : 'fit-gauge__tick'}
            style={{ left: `${tick}%` }}
          />
        ))}
        <div className="fit-gauge__fill" style={{ width: `${displayScore}%` }} />
        <div className="fit-gauge__pin" style={{ left: `${displayScore}%` }} />
      </div>
      <div className="fit-gauge__scale">
        {TICKS.filter((t) => t % 20 === 0).map((tick) => (
          <span key={tick}>{tick}</span>
        ))}
      </div>
      <div className="fit-gauge__readout">
        <span className="fit-gauge__score">{clamped}</span>
        <span className={`fit-gauge__tier tier--${tierClass(tier)}`}>{tier}</span>
      </div>
    </div>
  )
}

export default FitGauge

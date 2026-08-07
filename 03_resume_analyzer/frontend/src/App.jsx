import { useState } from 'react'
import ResumeReview from './pages/ResumeReview'
import Archive from './pages/Archive'
import TapeIcon from './components/TapeIcon'
import './App.css'

const TABS = [
  { id: 'measure', label: 'Measure' },
  { id: 'archive', label: 'Archive' },
]

function App() {
  const [activeTab, setActiveTab] = useState('measure')

  return (
    <div className="app-shell">
      <header className="page-header">
        <span className="eyebrow">Resume × Job Description</span>
        <div className="brand">
          <span className="brand__mark">
            <TapeIcon />
          </span>
          <h1 className="brand__name">Resume Analyzer</h1>
        </div>
        <p className="tagline">
          Upload a resume, paste the job description — get a fitment score down to the stitch.
        </p>
      </header>

      <nav className="tab-nav">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            className={
              tab.id === activeTab ? 'tab-nav__btn tab-nav__btn--active' : 'tab-nav__btn'
            }
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {activeTab === 'measure' ? <ResumeReview /> : <Archive />}
    </div>
  )
}

export default App

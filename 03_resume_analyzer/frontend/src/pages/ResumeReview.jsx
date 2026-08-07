import { useState } from 'react'
import { analyzeResume } from '../api/resume'
import AnalysisReport from '../components/AnalysisReport'
import TapeIcon from '../components/TapeIcon'

function ReportPanel({ loading, error, report }) {
  if (loading) {
    return (
      <section className="panel panel--report">
        <div className="measuring">
          <div className="measuring__bar" />
          <p className="measuring__text">Measuring fit…</p>
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="panel panel--report error-panel">
        <p className="error-panel__heading">Couldn't measure fit</p>
        <p className="error-panel__detail">{error}</p>
      </section>
    )
  }

  if (report) {
    return (
      <section className="panel panel--report">
        <AnalysisReport report={report} />
      </section>
    )
  }

  return (
    <section className="panel panel--report">
      <div className="empty-state">
        <TapeIcon width="56" height="56" />
        <p>Your fitment report will appear here once you measure a resume against a job description.</p>
      </div>
    </section>
  )
}

function ResumeReview() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!resumeFile) {
      setError('Choose a resume file (.pdf or .md) before measuring.')
      setReport(null)
      return
    }

    setLoading(true)
    setError(null)
    setReport(null)
    try {
      const data = await analyzeResume(resumeFile, jobDescription)
      setReport(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="workspace">
      <section className="panel panel--input">
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="resume-file" className="field__label">
              Resume <span className="field__hint">.pdf or .md</span>
            </label>
            <div className="dropzone">
              <input
                id="resume-file"
                type="file"
                accept=".pdf,.md"
                onChange={(event) => setResumeFile(event.target.files[0] ?? null)}
              />
              <span className={resumeFile ? 'dropzone__name' : 'dropzone__name dropzone__name--empty'}>
                {resumeFile ? resumeFile.name : 'No file chosen yet'}
              </span>
            </div>
          </div>

          <div className="field">
            <label htmlFor="job-description" className="field__label">
              Job Description
            </label>
            <textarea
              id="job-description"
              className="textarea"
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
              placeholder="Paste the job posting here"
            />
          </div>

          <button type="submit" className="btn-measure" disabled={loading}>
            {loading ? 'Measuring…' : 'Measure Fit'}
          </button>
        </form>
      </section>

      <ReportPanel loading={loading} error={error} report={report} />
    </div>
  )
}

export default ResumeReview

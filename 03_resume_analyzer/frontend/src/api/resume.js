const API_BASE_URL = 'http://localhost:8000'

export async function analyzeResume(resumeFile, jobDescription) {
  const formData = new FormData()
  formData.append('resume', resumeFile)
  formData.append('job_description', jobDescription)

  const res = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData,
  })

  const data = await res.json().catch(() => null)
  if (!res.ok) {
    throw new Error(data?.detail || `Request failed with status ${res.status}`)
  }
  return data
}

export async function getHistory() {
  const res = await fetch(`${API_BASE_URL}/api/history`)
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    throw new Error(data?.detail || `Request failed with status ${res.status}`)
  }
  return data
}

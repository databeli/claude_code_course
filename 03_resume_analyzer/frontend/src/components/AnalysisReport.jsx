import FitGauge from './FitGauge'

function AnalysisReport({ report }) {
  return (
    <div>
      <FitGauge score={report.score} tier={report.tier} />

      <div className="recommendations">
        {report.missing_keywords.length > 0 && (
          <div>
            <p className="rec-section__label">Missing Keywords</p>
            <ul className="rec-tags">
              {report.missing_keywords.map((keyword) => (
                <li key={keyword} className="rec-tag">
                  {keyword}
                </li>
              ))}
            </ul>
          </div>
        )}

        {report.skill_gaps.length > 0 && (
          <div>
            <p className="rec-section__label">Skill Gaps</p>
            <ul className="rec-list">
              {report.skill_gaps.map((gap) => (
                <li key={gap}>{gap}</li>
              ))}
            </ul>
          </div>
        )}

        {report.phrasing_suggestions.length > 0 && (
          <div>
            <p className="rec-section__label">Phrasing Suggestions</p>
            <ul className="rec-list">
              {report.phrasing_suggestions.map((suggestion) => (
                <li key={suggestion}>{suggestion}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default AnalysisReport

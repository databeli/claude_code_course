function TapeIcon(props) {
  return (
    <svg width="36" height="36" viewBox="0 0 36 36" fill="none" aria-hidden="true" {...props}>
      <rect x="3" y="13" width="30" height="10" rx="2" stroke="currentColor" strokeWidth="2" />
      <path
        d="M8 13V17M13 13V19M18 13V17M23 13V19M28 13V17"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  )
}

export default TapeIcon

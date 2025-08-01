const Results = () => {
  const data = window.resultsData;
  const chartRef = React.useRef(null);

  React.useEffect(() => {
    const ctx = chartRef.current.getContext('2d');
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Plagiarism', 'Original'],
        datasets: [{
          data: [data.similarity_score, 100 - data.similarity_score],
          backgroundColor: ['#ff6384', '#4CAF50']
        }]
      },
      options: { responsive: true, maintainAspectRatio: false }
    });
  }, []);

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <a className="navbar-brand" href="/">HackX</a>
        </div>
      </nav>

      <div className="container py-5">
        <h2 className="mb-4">Results</h2>
        <div className="row">
          <div className="col-md-4">
            <ul className="list-group">
              <li className="list-group-item d-flex justify-content-between align-items-center">
                Exact Match
                <span className="badge bg-secondary">{data.exact_match === 'true' ? '✔' : '✖'}</span>
              </li>
              <li className="list-group-item d-flex justify-content-between align-items-center">
                Variable Renaming
                <span className="badge bg-secondary">{data.variable_renaming === 'true' ? '✔' : '✖'}</span>
              </li>
              <li className="list-group-item d-flex justify-content-between align-items-center">
                Structural Similarity
                <span className="badge bg-secondary">{data.structural_similarity === 'true' ? '✔' : '✖'}</span>
              </li>
            </ul>
          </div>
          <div className="col-md-4">
            <canvas ref={chartRef} height="250"></canvas>
          </div>
        </div>

        <div className="mt-4">
          <button className="btn btn-primary" onClick={fetchFeedback}>Generate Feedback</button>
          <textarea id="feedback-text" className="form-control mt-3" rows="4" placeholder="Feedback"></textarea>
        </div>
      </div>

      <footer className="bg-light text-center py-4 mt-5">
        <div className="container">
          <p className="text-muted">&copy; 2025 HackX</p>
        </div>
      </footer>
    </div>
  );
};

function fetchFeedback() {
  fetch('/generate_feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      submitted_code: window.resultsData.submitted_code,
      original_code: window.resultsData.original_code
    })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById('feedback-text').value = data.feedback;
    });
}

ReactDOM.render(<Results />, document.getElementById('root'));

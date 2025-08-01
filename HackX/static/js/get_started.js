const GetStarted = () => {
  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <a className="navbar-brand" href="/">HackX</a>
        </div>
      </nav>

      <div className="container py-5">
        <h2 className="mb-4">Submit Your Code</h2>
        <form method="POST" action="/get_started">
          <input type="hidden" name="csrf_token" value={window.csrfToken} />
          <div className="mb-3">
            <label className="form-label">Code</label>
            <textarea className="form-control" name="code" rows="8" required></textarea>
          </div>
          <div className="mb-3">
            <label className="form-label">Question</label>
            <textarea className="form-control" name="question" rows="4" required></textarea>
          </div>
          <div className="mb-3">
            <label className="form-label">Original Solution</label>
            <textarea className="form-control" name="original_code" rows="4" required></textarea>
          </div>
          <button type="submit" className="btn btn-primary">Submit</button>
        </form>
      </div>

      <footer className="bg-light text-center py-4 mt-5">
        <div className="container">
          <p className="text-muted">&copy; 2025 HackX</p>
        </div>
      </footer>
    </div>
  );
};

ReactDOM.render(<GetStarted />, document.getElementById('root'));

const App = () => (
  <div>
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">HackX</a>
        <div className="collapse navbar-collapse">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item"><a className="nav-link" href="#">Home</a></li>
            <li className="nav-item"><a className="nav-link" href="#">About</a></li>
            <li className="nav-item"><a className="nav-link" href="#">Team</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <header className="bg-primary text-white text-center py-5">
      <div className="container">
        <h1 className="display-4">Advanced Plagiarism Detection</h1>
        <p className="lead">Check your code for originality</p>
        <a href="/get_started" className="btn btn-light btn-lg mt-3">Get Started</a>
      </div>
    </header>

    <footer className="bg-light text-center py-4 mt-5">
      <div className="container">
        <p className="text-muted">&copy; 2025 HackX</p>
      </div>
    </footer>
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));

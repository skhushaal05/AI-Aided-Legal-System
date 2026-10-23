function Home() {
  return (
    <div className="home-page">

      <main className="home-main">

        <section className="home-introduction">

          <p className="eyebrow">
            POSH PLATFORM
          </p>

          <h1>
            Respect belongs
            <br />
            in every workplace.
          </h1>

          <p className="home-description">
            A workplace should provide every individual
            with dignity, safety and an environment where
            concerns can be understood and addressed.
          </p>

          <div className="home-rule"></div>

          <p className="home-note">
            Prevention · Awareness · Accountability
          </p>

        </section>

        <section className="home-side-content">

          <div className="home-number">
            01
          </div>

          <div className="home-side-text">
            <p>
              A platform designed to make workplace
              safety, awareness and complaint
              management easier to understand.
            </p>
          </div>

        </section>

      </main>

      <footer className="home-footer">

        <span>
          Workplace safety & awareness platform
        </span>

        <div className="home-footer-links">
          <a href="#privacy">
            Privacy Policy
          </a>

          <a href="#terms">
            Terms of Service
          </a>
        </div>

      </footer>

    </div>
  );
}

export default Home;
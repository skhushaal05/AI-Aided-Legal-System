import { useState } from "react";
import LoginDropdown from "../components/LoginDropdown";

import vritonaLogo from "../assets/vritona-logo.jpeg";

function Landing({ onLogin }) {
  const [accountOpen, setAccountOpen] = useState(false);

  function toggleAccount() {
    setAccountOpen((previous) => !previous);
  }

  return (
    <div className="landing-page">

      {/* =====================================================
          HEADER
          ===================================================== */}

      <header className="landing-header">

        <div className="landing-brand">
          <img
            src={vritonaLogo}
            alt="Vritona"
            className="landing-vritona-logo"
          />
        </div>

        <button
          className="account-button"
          onClick={toggleAccount}
          aria-label="Open account menu"
          aria-expanded={accountOpen}
        >
          <svg
            width="22"
            height="22"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <circle cx="12" cy="8" r="3.2" />
            <path d="M5.5 20c.7-3.4 3-5.2 6.5-5.2s5.8 1.8 6.5 5.2" />
          </svg>
        </button>

      </header>


      {/* =====================================================
          LOGIN / SIGNUP DROPDOWN
          ===================================================== */}

      <LoginDropdown
        isOpen={accountOpen}
        onLogin={onLogin}
      />


      {/* =====================================================
          MAIN CONTENT
          ===================================================== */}

      <main className="landing-main">

        <section className="landing-copy">

          <p className="eyebrow">
            WORKPLACE SAFETY & COMPLIANCE
          </p>

          <h1>
            A safer workplace
            <br />
            begins with
            <br />
            awareness.
          </h1>

          <p className="landing-description">
            Vritona helps organizations understand,
            manage and strengthen their workplace
            safety practices while making important
            information easier to access.
          </p>

          <div className="landing-rule"></div>

          <p className="landing-note">
            Prevention · Awareness · Accountability
          </p>

        </section>


        {/* =================================================
            SIDE GLASS CARD
            ================================================= */}

        <section className="landing-side">

          <p className="side-number">
            01
          </p>

          <p>
            Creating workplaces where every person
            can work with dignity, safety and respect.
          </p>

        </section>

      </main>


      {/* =====================================================
          FOOTER
          ===================================================== */}

      <footer className="landing-footer">

        <span>
          Workplace safety & awareness platform
        </span>

        <div>
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

export default Landing;
import { useState } from "react";

function LoginDropdown({ isOpen, onLogin }) {
  const [mode, setMode] = useState("selection");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  if (!isOpen) {
    return null;
  }

  function handleLogin(event) {
    event.preventDefault();

    if (!email || !password) {
      return;
    }

    /*
      Temporary frontend login.

      Later this will be replaced with:
      POST /api/login
    */

    onLogin();
  }

  function handleSignup(event) {
    event.preventDefault();

    setMode("login");
  }

  return (
    <div className="auth-dropdown">

      {mode === "selection" && (
        <>
          <p className="auth-label">
            ACCOUNT
          </p>

          <h2>
            Welcome
          </h2>

          <p className="auth-description">
            Sign in to your POSH account or create a
            new account to continue.
          </p>

          <button
            className="auth-primary"
            onClick={() => setMode("login")}
          >
            Login
          </button>

          <button
            className="auth-secondary"
            onClick={() => setMode("signup")}
          >
            Sign Up
          </button>
        </>
      )}


      {mode === "login" && (
        <>
          <p className="auth-label">
            ACCOUNT / LOGIN
          </p>

          <h2>
            Sign in
          </h2>

          <form onSubmit={handleLogin}>

            <label>
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              required
            />


            <label>
              Password
            </label>

            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter your password"
              required
            />


            <button
              type="submit"
              className="auth-primary"
            >
              Login
            </button>

          </form>

          <button
            className="auth-back"
            onClick={() => setMode("selection")}
          >
            Back
          </button>
        </>
      )}


      {mode === "signup" && (
        <>
          <p className="auth-label">
            ACCOUNT / REGISTRATION
          </p>

          <h2>
            Create account
          </h2>

          <form onSubmit={handleSignup}>

            <label>
              Full name
            </label>

            <input
              type="text"
              placeholder="Your full name"
              required
            />


            <label>
              Email
            </label>

            <input
              type="email"
              placeholder="you@example.com"
              required
            />


            <label>
              Password
            </label>

            <input
              type="password"
              placeholder="Create a password"
              required
            />


            <button
              type="submit"
              className="auth-primary"
            >
              Create Account
            </button>

          </form>

          <button
            className="auth-back"
            onClick={() => setMode("selection")}
          >
            Back
          </button>
        </>
      )}

    </div>
  );
}

export default LoginDropdown;
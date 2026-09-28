import { useEffect, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [mode, setMode] = useState("login");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [token, setToken] = useState(
    () => localStorage.getItem("access_token") || ""
  );

  const [user, setUser] = useState(null);

  const [authLoading, setAuthLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    house_age: 10,
    location_risk: 0.5,
    roof_type: 1,
    past_claims: 1,
    property_value: 500000,
  });

  const [result, setResult] = useState(null);
  const [predictLoading, setPredictLoading] = useState(false);

  useEffect(() => {
    if (token) {
      loadCurrentUser(token);
    }
  }, [token]);

  async function loadCurrentUser(accessToken) {
    try {
      const response = await fetch(`${API_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!response.ok) {
        logout();
        return;
      }

      const data = await response.json();
      setUser(data);
    } catch {
      setError("Unable to connect to the API.");
    }
  }

  async function handleAuth(event) {
    event.preventDefault();

    setAuthLoading(true);
    setError("");
    setMessage("");

    try {
      const endpoint =
        mode === "register" ? "/auth/register" : "/auth/login";

      const payload = {
        email,
        password,
      };

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Authentication failed.");
      }

      if (mode === "register") {
        setMessage("Registration successful. You can now log in.");
        setMode("login");
        setPassword("");
      } else {
        localStorage.setItem("access_token", data.access_token);
        setToken(data.access_token);
        setMessage("Login successful.");
        setPassword("");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setAuthLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("access_token");
    setToken("");
    setUser(null);
    setResult(null);
    setMessage("");
    setError("");
  }

  function updateForm(field, value) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function predictRisk(event) {
    event.preventDefault();

    setPredictLoading(true);
    setError("");
    setMessage("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          house_age: Number(form.house_age),
          location_risk: Number(form.location_risk),
          roof_type: Number(form.roof_type),
          past_claims: Number(form.past_claims),
          property_value: Number(form.property_value),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (response.status === 401) {
          logout();
          throw new Error("Your session has expired. Please log in again.");
        }

        throw new Error(data.detail || "Prediction failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setPredictLoading(false);
    }
  }

  if (!token || !user) {
    return (
      <div className="page">
        <div className="auth-card">
          <div className="brand">
            <div className="brand-icon">🏠</div>
            <div>
              <h1>House Insurance Risk</h1>
              <p>AI-powered property risk assessment</p>
            </div>
          </div>

          <div className="tabs">
            <button
              className={mode === "login" ? "active" : ""}
              onClick={() => {
                setMode("login");
                setError("");
                setMessage("");
              }}
            >
              Login
            </button>

            <button
              className={mode === "register" ? "active" : ""}
              onClick={() => {
                setMode("register");
                setError("");
                setMessage("");
              }}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleAuth}>
            <label>Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              minLength={6}
              required
            />

            <button className="primary-button" disabled={authLoading}>
              {authLoading
                ? "Please wait..."
                : mode === "login"
                ? "Login"
                : "Create Account"}
            </button>
          </form>

          {message && <div className="success">{message}</div>}
          {error && <div className="error">{error}</div>}

          <p className="demo-note">
            Secure JWT-protected insurance risk prediction demo.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="page dashboard-page">
      <header className="topbar">
        <div className="brand compact">
          <div className="brand-icon">🏠</div>
          <div>
            <h2>House Insurance Risk</h2>
            <span>AI Risk Assessment</span>
          </div>
        </div>

        <div className="user-area">
          <span>{user.email}</span>
          <button onClick={logout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="hero">
          <div>
            <h1>Property Risk Assessment</h1>
            <p>
              Enter your property information to calculate an AI-based risk
              score and illustrative annual premium.
            </p>
          </div>
        </section>

        <div className="dashboard-grid">
          <section className="panel">
            <h2>Property Details</h2>

            <form onSubmit={predictRisk}>
              <div className="field">
                <label>House Age</label>
                <div className="input-row">
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={form.house_age}
                    onChange={(e) =>
                      updateForm("house_age", e.target.value)
                    }
                  />
                  <span>years</span>
                </div>
              </div>

              <div className="field">
                <label>Location Risk</label>
                <div className="input-row">
                  <input
                    type="number"
                    min="0"
                    max="1"
                    step="0.01"
                    value={form.location_risk}
                    onChange={(e) =>
                      updateForm("location_risk", e.target.value)
                    }
                  />
                  <span>0–1</span>
                </div>
              </div>

              <div className="field">
                <label>Roof Type</label>
                <select
                  value={form.roof_type}
                  onChange={(e) =>
                    updateForm("roof_type", e.target.value)
                  }
                >
                  <option value="1">Type 1</option>
                  <option value="2">Type 2</option>
                  <option value="3">Type 3</option>
                  <option value="4">Type 4</option>
                  <option value="5">Type 5</option>
                </select>
              </div>

              <div className="field">
                <label>Past Claims</label>
                <input
                  type="number"
                  min="0"
                  max="10"
                  value={form.past_claims}
                  onChange={(e) =>
                    updateForm("past_claims", e.target.value)
                  }
                />
              </div>

              <div className="field">
                <label>Property Value</label>
                <div className="input-row">
                  <span>₹</span>
                  <input
                    type="number"
                    min="10000"
                    step="10000"
                    value={form.property_value}
                    onChange={(e) =>
                      updateForm("property_value", e.target.value)
                    }
                  />
                </div>
              </div>

              <button className="primary-button predict-button">
                {predictLoading ? "Calculating..." : "Calculate Risk"}
              </button>
            </form>

            {error && <div className="error">{error}</div>}
          </section>

          <section className="panel result-panel">
            <h2>Risk Assessment</h2>

            {!result ? (
              <div className="empty-result">
                <div className="empty-icon">📊</div>
                <h3>Ready for assessment</h3>
                <p>
                  Enter the property details and click Calculate Risk.
                </p>
              </div>
            ) : (
              <>
                <div className="risk-score">
                  <span>Risk Score</span>
                  <strong>
                    {(result.risk_percentage ?? result.risk_score * 100).toFixed(
                      2
                    )}
                    %
                  </strong>
                  <div className="risk-bar">
                    <div
                      style={{
                        width: `${Math.min(
                          100,
                          Math.max(
                            0,
                            result.risk_percentage ??
                              result.risk_score * 100
                          )
                        )}%`,
                      }}
                    />
                  </div>
                </div>

                <div className="result-grid">
                  <div className="result-box">
                    <span>Risk Category</span>
                    <strong>{result.risk_category}</strong>
                  </div>

                  <div className="result-box">
                    <span>Annual Premium</span>
                    <strong>
                      ₹
                      {Number(
                        result.recommended_premium || 0
                      ).toLocaleString("en-IN", {
                        minimumFractionDigits: 2,
                      })}
                    </strong>
                  </div>

                  <div className="result-box">
                    <span>Premium Rate</span>
                    <strong>
                      {(
                        Number(result.premium_rate || 0) * 100
                      ).toFixed(3)}
                      %
                    </strong>
                  </div>

                  <div className="result-box">
                    <span>Property Value</span>
                    <strong>
                      ₹
                      {Number(form.property_value).toLocaleString("en-IN")}
                    </strong>
                  </div>
                </div>

                {result.feature_importance && (
                  <div className="importance">
                    <h3>Feature Importance</h3>

                    {Object.entries(result.feature_importance).map(
                      ([feature, value]) => (
                        <div className="importance-row" key={feature}>
                          <div className="importance-label">
                            <span>{feature}</span>
                            <span>
                              {(Number(value) * 100).toFixed(1)}%
                            </span>
                          </div>

                          <div className="importance-bar">
                            <div
                              style={{
                                width: `${Math.min(
                                  100,
                                  Number(value) * 100
                                )}%`,
                              }}
                            />
                          </div>
                        </div>
                      )
                    )}
                  </div>
                )}
              </>
            )}
          </section>
        </div>

        <footer>
          Demonstration estimate only — not an actuarial insurance quote.
        </footer>
      </main>
    </div>
  );
}

export default App;
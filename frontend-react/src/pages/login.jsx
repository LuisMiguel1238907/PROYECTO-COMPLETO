// src/pages/login.jsx
import { useState } from "react";
import { API_URL } from "../config";
import "./login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const manejarSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setCargando(true);

    try {
      // Construimos un form-urlencoded como lo espera OAuth2PasswordRequestForm
      const formData = new URLSearchParams();
      formData.append("username", email);   // 👈 si en tu backend es email, igual se puede usar como username
      formData.append("password", password);

      const resp = await fetch(`${API_URL}/token`, {
        // 👈 cambia /token si en /docs ves que la ruta es /login u otra
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!resp.ok) {
        setError("Credenciales incorrectas o error en el servidor");
        setCargando(false);
        return;
      }

      const data = await resp.json();

      const token = data.access_token || data.token;
      if (!token) {
        setError("No se recibió token del servidor");
        setCargando(false);
        return;
      }

      localStorage.setItem("token", token);

      // Luego esto será navegación con React Router. Por ahora, redirección simple:
      window.location.href = "/dashboard";
    } catch (err) {
      console.error(err);
      setError("No se pudo conectar con el backend");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Iniciar Sesión</h1>

        <form id="login-form" onSubmit={manejarSubmit}>
          <input
            type="email"
            id="email"
            placeholder="Correo"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            id="password"
            placeholder="Contraseña"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && (
            <p style={{ color: "salmon", marginTop: "8px" }}>{error}</p>
          )}

          <button type="submit" disabled={cargando}>
            {cargando ? "Ingresando..." : "Ingresar"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
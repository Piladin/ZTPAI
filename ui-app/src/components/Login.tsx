import React, { useState } from "react";
import axios from "axios";
import "./Login.css"; // Import stylów
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/api/login/", {
        username,
        password,
      });
      const { access, refresh } = response.data;
      sessionStorage.setItem("access_token", access);
      sessionStorage.setItem("refresh_token", refresh);
      alert("Login successful!");
      navigate('/profile');
    } catch (error) {
      console.error("Login error:", error);
      alert("Login failed. Please check your credentials.");
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleLogin}>
        <h1 className="login-header">Login</h1>

        <div className="login-group">
          <label className="login-label">Login</label>
          <input
            type="text"
            className="login-input"
            placeholder="Enter your login"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="login-group">
          <label className="login-label">Password</label>
          <input
            type="password"
            className="login-input"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit" className="login-button">
          Sign In
        </button>

        <a href="#" className="forgot-password">
          Forgot password?
        </a>
        <a href="/register" className="forgot-password">
          Don't have an account? Register here!
        </a>
      </form>
    </div>
  );
};

export default Login;

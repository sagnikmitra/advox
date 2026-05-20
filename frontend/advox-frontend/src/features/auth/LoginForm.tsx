import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../../api/axios';
import './LoginForm.css'; // Assuming your CSS is here
import { useAuth } from '../../context/useAuth';
import { runtimeConfig } from '../../config/runtime';

const LoginForm = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (runtimeConfig.isDemoMode) {
      auth.login('demo-token');
      navigate('/home');
      return;
    }

    try {
      const response = await axios.post('/auth/login', { email, password });
      const token = response.data.data.token;
      auth.login(token); // ✅ Update auth context & localStorage
      navigate('/home');
    } catch (error) {
      console.error(error);
      setError('Login failed');
    }
  };

  return (
    <div className="login-container">
      <h1>Login</h1>
      {runtimeConfig.isDemoMode && (
        <p style={{ marginBottom: '1rem', color: '#555' }}>
          Demo mode active. Any email/password works.
        </p>
      )}
      <form className="login-form" onSubmit={handleLogin}>
        {error && <p style={{ color: 'red', marginBottom: '1rem' }}>{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      <div className="switch-form">
        <p>Don't have an account?</p>
        <button type="button" onClick={() => navigate('/register')}>
          Register here
        </button>
      </div>
    </div>
  );
};

export default LoginForm;

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../../api/axios';
import './RegisterForm.css';
import { runtimeConfig } from '../../config/runtime';

const RegisterForm = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [barCouncilId, setBarCouncilId] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (runtimeConfig.isDemoMode) {
      navigate('/login');
      return;
    }

    try {
      await axios.post('/auth/register', {
        email,
        password,
        name,
        phoneNumber,
        barCouncilId,
      });
      navigate('/login');
    } catch (err) {
      console.error(err);
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="register-container">
      <h1>Register</h1>
      {runtimeConfig.isDemoMode && (
        <p style={{ marginBottom: '1rem', color: '#555' }}>
          Demo mode active. Registration disabled in public preview.
        </p>
      )}
      <form className="register-form" onSubmit={handleRegister}>
        {error && <p style={{ color: 'red', marginBottom: '1rem' }}>{error}</p>}
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
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
        <input
          type="text"
          placeholder="Phone Number"
          value={phoneNumber}
          onChange={e => setPhoneNumber(e.target.value)}
        />
        <input
          type="text"
          placeholder="Bar Council ID"
          value={barCouncilId}
          onChange={e => setBarCouncilId(e.target.value)}
        />
        <button type="submit">Register</button>
      </form>
      <div className="switch-form">
        <p>Already have an account?</p>
        <button type="button" onClick={() => navigate('/login')}>
          Login here
        </button>
      </div>
    </div>
  );
};

export default RegisterForm;

import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/useAuth';
import { useState } from 'react';

const Homepage = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [searchInput, setSearchInput] = useState('');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const goToProfile = () => {
    navigate('/profile');
  };

  const handleSearch = () => {
    if (searchInput.trim()) {
      navigate(`/search-results?query=${encodeURIComponent(searchInput)}`);
    }
  };

  return (
    <div className="homepage-container" style={styles.container}>
      <h1 style={styles.title}>Welcome to Advox!</h1>
      <div> Use : WBBB0F0000562012</div>

      <div style={styles.search}>
        <input
          type="text"
          placeholder="Enter CNR Number"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          style={styles.input}
        />
        <button style={styles.searchButton} onClick={handleSearch}>
          Search
        </button>
      </div>

      <div style={styles.buttons}>
        <button style={styles.button} onClick={goToProfile}>
          View / Edit Profile
        </button>
        <button style={{ ...styles.button, backgroundColor: '#dc3545' }} onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '600px',
    margin: '5rem auto',
    padding: '2rem',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 8px 20px rgba(0, 0, 0, 0.1)',
    textAlign: 'center' as const,
  },
  title: {
    fontSize: '2rem',
    color: '#333',
    marginBottom: '2rem',
  },
  search: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '2rem',
    justifyContent: 'center',
  },
  input: {
    padding: '0.7rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: '1px solid #ccc',
    width: '60%',
  },
  searchButton: {
    padding: '0.7rem 1.2rem',
    fontSize: '1rem',
    fontWeight: 600,
    borderRadius: '6px',
    border: 'none',
    color: '#fff',
    cursor: 'pointer',
    backgroundColor: '#28a745',
  },
  buttons: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1rem',
  },
  button: {
    padding: '0.9rem',
    fontSize: '1rem',
    fontWeight: 600,
    borderRadius: '8px',
    border: 'none',
    color: '#fff',
    cursor: 'pointer',
    backgroundColor: '#007bff',
    transition: 'background-color 0.3s',
  },
};

export default Homepage;

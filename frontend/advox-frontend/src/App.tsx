import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './features/auth/LoginForm';
import RegisterForm from './features/auth/RegisterForm';
import Homepage from './pages/HomePage';
import ProfileDetails from './features/profile/ProfileDetails';
import SearchResults from './features/search/SearchResults';
import { useAuth } from './context/useAuth';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />

        <Route
          path="/home"
          element={isAuthenticated ? <Homepage /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/profile"
          element={isAuthenticated ? <ProfileDetails /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/search-results"
          element={isAuthenticated ? <SearchResults /> : <Navigate to="/login" replace />}
        />

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;

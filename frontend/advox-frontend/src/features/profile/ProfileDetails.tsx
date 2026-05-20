import { useEffect, useState } from 'react';
import axios from '../../api/axios';
import { useAuth } from '../../context/useAuth';
import './ProfileDetails.css';
import { useNavigate } from 'react-router-dom';
import { runtimeConfig } from '../../config/runtime';

interface UserDetails {
  id: number;
  name: string;
  phoneNumber: string;
  barCounselId: string;
  email: string;
}

export default function ProfileDetails() {
  const { token, logout } = useAuth();
  const [profile, setProfile] = useState<UserDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      if (runtimeConfig.isDemoMode) {
        setProfile({
          id: 0,
          name: 'Demo Advocate',
          phoneNumber: '+91 90000 00000',
          barCounselId: 'DEMO-001',
          email: 'demo@advox.in',
        });
        setLoading(false);
        return;
      }

      try {
        const tempToken = localStorage.getItem('token');
        const response = await axios.get('/auth/me', {
          headers: { Authorization: `Bearer ${tempToken}` },
        });
        setProfile(response.data.data);
      } catch (err) {
        console.error(err);
        setError('Failed to fetch profile');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [token]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!profile) return;
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (runtimeConfig.isDemoMode) {
      setSuccess('Demo mode: profile changes are not persisted.');
      return;
    }

    try {
      await axios.put(
        '/auth/me',
        {
          name: profile?.name,
          phoneNumber: profile?.phoneNumber,
          barCouncilId: profile?.barCounselId,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Profile updated successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to update profile');
    }
  };

  if (loading) return <div className="container">Loading profile...</div>;
  if (error) return <div className="container text-red-500">{error}</div>;

  return (
    <div className="container max-w-md mx-auto mt-10 bg-white p-6 rounded-lg shadow">
        <button
        onClick={() => navigate('/home')}
        className="mb-4 text-blue-600 underline hover:text-blue-800"
      >
        ← Back to Home
      </button>
      <h1 className="text-2xl font-bold mb-4">My Profile</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={profile?.name || ''}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          type="text"
          name="phoneNumber"
          placeholder="Phone Number"
          value={profile?.phoneNumber || ''}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <input
          type="text"
          name="barCounselId"
          placeholder="Bar Council ID"
          value={profile?.barCounselId || ''}
          onChange={handleChange}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Save Changes
        </button>
      </form>
      {success && <p className="text-green-600 mt-4">{success}</p>}
      <button
  onClick={logout}
  className="logout"
>
  Logout
</button>
    </div>
  );
}

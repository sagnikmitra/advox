import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { runtimeConfig } from '../../config/runtime';

interface Party {
  name: string;
  advocate: string | null;
}

interface CaseData {
  court_name: string;
  case_details: Record<string, string>;
  case_status: Record<string, string>;
  parties: {
    petitioners: Party[];
    respondents: Party[];
  };
  case_history: {
    judge: string;
    business_on: string;
    hearing_date: string;
    purpose: string;
  }[];
}

const mockCaseData: CaseData = {
  court_name: 'Civil Judge, Jr. Divn. Bolpur, Birbhum',
  case_details: {
    'Case Type': 'Title Suit',
    'Filing Number': '111/2014 Filing Date 07-05-2012',
    'Registration Number': '127/2014 Registration Date: 07-05-2012',
    'CNR Number': 'WBBB0F0000562012',
  },
  case_status: {
    'First Hearing Date': '07th May 2012',
    'Decision Date': '23rd May 2025',
    'Case Status': 'Case disposed',
    'Nature of Disposal': 'Contested--DISMISSED',
    'Court Number and Judge': '4-Civil Judge Jr Div I',
  },
  parties: {
    petitioners: [{ name: '1) Sri Tapan Kr. Chanda', advocate: 'Goutam Sarkar' }],
    respondents: [{ name: '1) Smt. Sujata Chanda', advocate: null }],
  },
  case_history: [
    {
      judge: 'Civil Judge Jr Div I',
      business_on: '04-07-2015',
      hearing_date: '21-04-2016',
      purpose: 'Issues',
    },
    {
      judge: 'Civil Judge Jr Div I',
      business_on: '21-04-2016',
      hearing_date: '05-04-2017',
      purpose: '-',
    },
    {
      judge: 'Civil Judge Jr Div I',
      business_on: '21-05-2025',
      hearing_date: '23-05-2025',
      purpose: 'Judgement',
    },
  ],
};

const SearchResults = () => {
  const [data, setData] = useState<CaseData | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const location = useLocation();
  const navigate = useNavigate();

  const initialQuery = new URLSearchParams(location.search).get('query') || '';

  useEffect(() => {
    if (initialQuery) {
      setSearchQuery(initialQuery);
      void fetchCaseDetails(initialQuery);
    }
  }, [initialQuery]);

  const fetchCaseDetails = async (query: string) => {
    setLoading(true);

    if (runtimeConfig.isDemoMode) {
      window.setTimeout(() => {
        setData(mockCaseData);
        setLoading(false);
      }, 300);
      return;
    }

    try {
      const response = await axios.post(
        runtimeConfig.scrapeApiUrl,
        { cino: query },
        { headers: { 'Content-Type': 'application/json' } }
      );
      setData(response.data);
    } catch (err) {
      console.error('API error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      navigate(`/search-results?query=${encodeURIComponent(searchQuery)}`);
    }
  };

  const goBack = () => {
    navigate('/home');
  };

  return (
    <div style={styles.container}>
      <div>
        Use: WBBB0F0000562012
        {runtimeConfig.isDemoMode ? ' | Demo data mode' : ''}
      </div>
      <div style={styles.topBar}>
        <input
          type="text"
          placeholder="Enter CNR Number"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleSearch} style={styles.searchButton}>Search</button>
        <button onClick={goBack} style={styles.backButton}>Back to Homepage</button>
      </div>

      {loading ? (
        <p style={{ textAlign: 'center' }}>Loading...</p>
      ) : data ? (
        <div>
          <h2 style={{ textAlign: 'center' }}>Search Result for: <em>{initialQuery}</em></h2>
          <h3 style={{ textAlign: 'center' }}>{data.court_name}</h3>

          <section style={styles.section}>
            <h4>Case Details</h4>
            <ul>
              {Object.entries(data.case_details).map(([key, value]) => (
                <li key={key}><strong>{key}:</strong> {value}</li>
              ))}
            </ul>
          </section>

          <section style={styles.section}>
            <h4>Case Status</h4>
            <ul>
              {Object.entries(data.case_status).map(([key, value]) => (
                <li key={key}><strong>{key}:</strong> {value}</li>
              ))}
            </ul>
          </section>

          <section style={styles.section}>
            <h4>Parties</h4>
            <div>
              <strong>Petitioners:</strong>
              <ul>
                {data.parties.petitioners.map((party, index) => (
                  <li key={index}>
                    {party.name} {party.advocate && <>| Advocate: {party.advocate}</>}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <strong>Respondents:</strong>
              <ul>
                {data.parties.respondents.map((party, index) => (
                  <li key={index}>
                    {party.name} {party.advocate && <>| Advocate: {party.advocate}</>}
                  </li>
                ))}
              </ul>
            </div>
          </section>

          <section style={styles.section}>
            <h4>Case History</h4>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th>Judge</th>
                  <th>Business On</th>
                  <th>Hearing Date</th>
                  <th>Purpose</th>
                </tr>
              </thead>
              <tbody>
                {data.case_history.map((entry, index) => (
                  <tr key={index}>
                    <td>{entry.judge}</td>
                    <td>{entry.business_on}</td>
                    <td>{entry.hearing_date || '-'}</td>
                    <td>{entry.purpose || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </div>
      ) : (
        <p style={{ textAlign: 'center' }}>No data found.</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '900px',
    margin: '2rem auto',
    padding: '2rem',
    backgroundColor: '#fff',
    borderRadius: '10px',
    boxShadow: '0 6px 16px rgba(0, 0, 0, 0.1)',
    fontFamily: 'Arial, sans-serif' as const,
  },
  topBar: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '2rem',
    justifyContent: 'center',
    flexWrap: 'wrap' as const,
  },
  input: {
    padding: '0.6rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: '1px solid #ccc',
    flex: '1 0 300px',
  },
  searchButton: {
    padding: '0.6rem 1.2rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#28a745',
    color: '#fff',
    cursor: 'pointer',
  },
  backButton: {
    padding: '0.6rem 1.2rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#6c757d',
    color: '#fff',
    cursor: 'pointer',
  },
  section: {
    marginTop: '2rem',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse' as const,
    marginTop: '1rem',
  },
};

export default SearchResults;

const env = import.meta.env;

const loginApiBaseUrl =
  env.VITE_LOGIN_API_BASE_URL?.trim() ||
  (window.location.hostname === 'localhost' ? 'http://localhost:8080/login/api' : '');

const scrapeApiUrl =
  env.VITE_SCRAPE_API_URL?.trim() ||
  (window.location.hostname === 'localhost' ? 'http://localhost:8080/scrape/submit-form' : '');

export const runtimeConfig = {
  loginApiBaseUrl,
  scrapeApiUrl,
  isDemoMode: !loginApiBaseUrl || !scrapeApiUrl,
};

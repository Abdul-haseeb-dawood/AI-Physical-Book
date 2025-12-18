// Environment configuration for API integration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const API_CONFIG = {
  BASE_URL: API_BASE_URL,
  ENDPOINTS: {
    AUTH: {
      REGISTER: `${API_BASE_URL}/api/auth/register`,
      LOGIN: `${API_BASE_URL}/api/auth/login`,
    },
    CHAPTERS: {
      ALL: `${API_BASE_URL}/api/chapters`,
      BY_SLUG: (slug) => `${API_BASE_URL}/api/chapters/${slug}`,
    },
    CHAT: {
      START_SESSION: `${API_BASE_URL}/api/chat/start-session`,
      QUERY: (sessionId) => `${API_BASE_URL}/api/chat/${sessionId}/query`,
    },
    PERSONALIZATION: {
      PROFILE: `${API_BASE_URL}/api/personalization/profile`,
    },
    TRANSLATION: {
      TOGGLE: `${API_BASE_URL}/api/translation/toggle`,
    },
  },
  HEADERS: {
    'Content-Type': 'application/json',
  },
};
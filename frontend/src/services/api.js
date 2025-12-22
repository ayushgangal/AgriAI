import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens if needed
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
};

// Query API
export const queryAPI = {
  // Text query
  processQuery: (queryData) => api.post('/', queryData),

  // Voice query
  processVoiceQuery: (audioFile, language = 'en-IN', userLocation = null, userContext = null) => {
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    formData.append('language', language);
    if (userLocation) formData.append('user_location', JSON.stringify(userLocation));
    if (userContext) formData.append('user_context', JSON.stringify(userContext));

    return api.post('/voice', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Image query
  processImageQuery: (imageFile, queryText = '', language = 'en') => {
    const formData = new FormData();
    formData.append('image_file', imageFile);
    formData.append('query_text', queryText);
    formData.append('language', language);

    return api.post('/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Get query history
  getQueryHistory: (limit = 10, offset = 0) =>
    api.get('/history', { params: { limit, offset } }),

  // Submit feedback
  submitFeedback: (queryId, rating, feedback = null) =>
    api.post('/feedback', { query_id: queryId, rating, feedback }),

  // Get query types
  getQueryTypes: () => api.get('/types'),

  // Get AI capabilities
  getAICapabilities: () => api.get('/capabilities'),
};

// Weather API
export const weatherAPI = {
  getCurrentWeather: (latitude, longitude) =>
    api.get('/current', { params: { latitude, longitude } }),

  getForecast: (latitude, longitude, days = 7) =>
    api.get('/forecast', { params: { latitude, longitude, days } }),

  getAlerts: (latitude, longitude) =>
    api.get('/alerts', { params: { latitude, longitude } }),

  getRecommendations: (latitude, longitude) =>
    api.get('/recommendations', { params: { latitude, longitude } }),
};

// Crops API
export const cropsAPI = {
  getCropRecommendations: (latitude, longitude, temperature = null, rainfall = null, humidity = null) =>
    api.get('/recommendations', {
      params: { latitude, longitude, temperature, rainfall, humidity }
    }),

  getCropManagementAdvice: (cropName, growthStage, latitude, longitude, temperature = null, rainfall = null, humidity = null) =>
    api.get(`/management/${cropName}`, {
      params: { growth_stage: growthStage, latitude, longitude, temperature, rainfall, humidity }
    }),

  getCropInfo: (cropName) => api.get(`/info/${cropName}`),
};

// Finance API
export const financeAPI = {
  getLoanCalculator: (loanAmount, repaymentPeriodMonths, loanType = 'crop_loan') =>
    api.get('/finance/loan-calculator', { params: { loan_amount: loanAmount, repayment_period_months: repaymentPeriodMonths, loan_type: loanType } }),

  getMarketTrends: (crop = null) =>
    crop ? api.get(`/finance/market-trends/${crop}`) : api.get('/finance/market-trends'), // Get all trends if no crop specified

  getFinancialInfo: (state = null, loanAmountNeeded = null) =>
    api.get('/finance/schemes', { params: { state, loan_amount_needed: loanAmountNeeded } }),
};

// Voice API
export const voiceAPI = {
  speechToText: (audioFile, language = 'en-IN') => {
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    formData.append('language', language);

    return api.post('/speech-to-text', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  textToSpeech: (text, language = 'en-IN') =>
    api.post('/text-to-speech', { text, language }),

  detectLanguage: (text) =>
    api.post('/detect-language', { text }),

  getLanguages: () => api.get('/languages'),

  validateAudio: (audioFile) => {
    const formData = new FormData();
    formData.append('audio_file', audioFile);

    return api.post('/validate-audio', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getSettings: () => api.get('/settings'),
};

export default api; 
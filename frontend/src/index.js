import React from 'react';
import ReactDOM from 'react-dom/client';

// 1. Global Styles (Tailwind directives & Plus Jakarta Sans)
import './index.css';

// 2. Component Logic Styles (Bioluminescent scrollbars & animations)
import './App.css';

// 3. Main Application Entry
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
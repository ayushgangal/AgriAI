import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

// Component & Page Imports
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Weather from './pages/Weather';
import Crops from './pages/Crops';
import Finance from './pages/Finance';
import Voice from './pages/Voice';

// Style Imports
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('user');

    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (error) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setShowLogin(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        {/* THE MAIN WRAPPER: Applying the Nature-Tech Base */}
        <div className="page-container selection:bg-accent-green/30">
          <div className="page-overlay" />
          <div className="bg-grain absolute inset-0 opacity-[0.02] pointer-events-none" />

          <div className="relative z-10 flex flex-col min-h-screen">
            <Navbar user={user} onLogout={handleLogout} />

            <main className="flex-grow pt-24"> {/* Padding top for fixed navbar */}
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/chat" element={<Chat />} />
                <Route path="/weather" element={<Weather />} />
                <Route path="/crops" element={<Crops />} />
                <Route path="/finance" element={<Finance />} />
                <Route path="/voice" element={<Voice />} />

                <Route
                  path="/login"
                  element={
                    showLogin ? (
                      <Login
                        onLoginSuccess={handleLoginSuccess}
                        onSwitchToRegister={() => setShowLogin(false)}
                      />
                    ) : (
                      <Register
                        onRegisterSuccess={handleLoginSuccess}
                        onSwitchToLogin={() => setShowLogin(true)}
                      />
                    )
                  }
                />
                <Route path="/register" element={<Navigate to="/login" replace />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </div>

          {/* PREMIUM BIOLUMINESCENT NOTIFICATIONS */}
          <Toaster
            position="bottom-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'rgba(8, 13, 11, 0.85)',
                color: '#fff',
                backdropFilter: 'blur(12px)',
                border: '1px solid rgba(0, 255, 171, 0.2)',
                borderRadius: '1.5rem',
                fontSize: '12px',
                fontWeight: '600',
                letterSpacing: '0.05em',
                textTransform: 'uppercase'
              },
              success: {
                iconTheme: {
                  primary: '#00ffab',
                  secondary: '#080d0b',
                },
              },
              error: {
                iconTheme: {
                  primary: '#EF4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
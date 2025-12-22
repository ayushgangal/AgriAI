import React, { useState, useEffect, useRef } from 'react';
import { EyeIcon, EyeSlashIcon, LockClosedIcon, UserIcon } from '@heroicons/react/24/outline';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';
import gsap from 'gsap';

const Login = ({ onLoginSuccess, onSwitchToRegister }) => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Ref for Antigravity Floating
  const cardRef = useRef(null);

  useEffect(() => {
    // 1. Entrance Animation
    gsap.fromTo(cardRef.current,
      { opacity: 0, scale: 0.9, y: 30 },
      { opacity: 1, scale: 1, y: 0, duration: 1, ease: "back.out(1.7)" }
    );

    // 2. Subtle Constant Floating (Antigravity)
    gsap.to(cardRef.current, {
      y: "-=10",
      duration: 4,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    });
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await authAPI.login(formData);
      const { access_token, user } = response.data;
      localStorage.setItem('authToken', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      toast.success('Access Granted. Welcome back.');
      onLoginSuccess(user);
    } catch (error) {
      toast.error('Authentication failed. Check credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container min-h-screen flex items-center justify-center px-4 relative">
      <div className="page-overlay opacity-20" />

      {/* THE LOGIN NODE */}
      <div
        ref={cardRef}
        className="max-w-md w-full space-y-8 glass-card p-10 relative overflow-hidden border-accent-green/20"
      >
        {/* Bioluminescent Top Bar */}
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-accent-green via-accent-cyan to-accent-lime"></div>

        <div className="text-center">
          <div className="mx-auto h-20 w-20 flex items-center justify-center rounded-[2rem] bg-accent-green/10 border border-accent-green/20 shadow-2xl shadow-accent-green/20 mb-8 animate-pulse-slow">
            <LockClosedIcon className="h-10 w-10 text-accent-green" />
          </div>
          <h2 className="text-4xl font-bold text-white tracking-tighter">
            Secure <span className="text-gradient">Gateway</span>
          </h2>
          <p className="mt-4 text-sm text-gray-400 font-light italic">
            Synchronizing your agricultural profile...
          </p>
        </div>

        <form className="mt-10 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-6">
            {/* EMAIL NODE */}
            <div className="group">
              <label className="block text-[10px] font-bold text-accent-green uppercase tracking-widest mb-2 ml-1">
                Field Coordinator Email
              </label>
              <div className="relative">
                <input
                  name="email"
                  type="email"
                  required
                  className="glass-input pl-10 group-hover:border-accent-green/40 transition-all"
                  placeholder="coordinator@agriai.com"
                  value={formData.email}
                  onChange={handleChange}
                />
                <UserIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-600 group-hover:text-accent-green transition-colors" />
              </div>
            </div>

            {/* PASSWORD NODE */}
            <div className="group">
              <label className="block text-[10px] font-bold text-accent-green uppercase tracking-widest mb-2 ml-1">
                Access Protocol
              </label>
              <div className="relative">
                <input
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  className="glass-input pl-10 pr-10 group-hover:border-accent-green/40 transition-all"
                  placeholder="                        "
                  value={formData.password}
                  onChange={handleChange}
                />
                <LockClosedIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-600 group-hover:text-accent-green transition-colors" />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-600 hover:text-accent-cyan transition-colors"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeSlashIcon className="h-5 w-5" /> : <EyeIcon className="h-5 w-5" />}
                </button>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between text-xs px-1">
            <div className="flex items-center gap-2 cursor-pointer group">
              <div className="w-4 h-4 rounded border border-white/20 flex items-center justify-center group-hover:border-accent-green transition-all">
                <div className="w-2 h-2 bg-accent-green rounded-sm opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <span className="text-gray-400">Remember Node</span>
            </div>
            <a href="#" className="font-bold text-accent-cyan hover:text-white transition-colors uppercase tracking-tighter">
              Reset Key?
            </a>
          </div>

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full py-4 text-lg font-black uppercase tracking-widest shadow-accent-green/20 group overflow-hidden relative"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-nature-900 mr-3"></div>
                  Verifying...
                </div>
              ) : (
                'Initialize Access'
              )}
              {/* Shimmer Effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
            </button>
          </div>

          <div className="text-center pt-4">
            <p className="text-xs text-gray-500">
              New coordinator?{' '}
              <button
                type="button"
                onClick={onSwitchToRegister}
                className="font-bold text-accent-lime hover:text-white transition-colors uppercase tracking-widest"
              >
                Register Sector
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
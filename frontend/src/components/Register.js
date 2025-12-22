import React, { useState, useEffect, useRef } from 'react';
import { EyeIcon, EyeSlashIcon, UserPlusIcon, EnvelopeIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';
import { authAPI } from '../services/api';
import toast from 'react-hot-toast';
import gsap from 'gsap';

const Register = ({ onRegisterSuccess, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Ref for Antigravity Floating
  const cardRef = useRef(null);

  useEffect(() => {
    // 1. Entrance Animation: Snapping into the digital space
    gsap.fromTo(cardRef.current,
      { opacity: 0, scale: 0.95, y: 40 },
      { opacity: 1, scale: 1, y: 0, duration: 1.2, ease: "back.out(1.5)" }
    );

    // 2. Continuous Antigravity Float
    gsap.to(cardRef.current, {
      y: "-=12",
      duration: 5,
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
    if (formData.password !== formData.confirmPassword) {
      toast.error('Identity keys do not match.');
      return;
    }
    setIsLoading(true);

    try {
      await authAPI.register({
        name: formData.name,
        email: formData.email,
        password: formData.password
      });
      toast.success('Sector Registered. Please initialize access.');
      onSwitchToLogin();
    } catch (error) {
      toast.error('Registration failed. Frequency error.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page-container min-h-screen flex items-center justify-center px-4 relative py-20">
      <div className="page-overlay opacity-25" />

      {/* REGISTRATION NODE */}
      <div
        ref={cardRef}
        className="max-w-lg w-full space-y-8 glass-card p-10 relative overflow-hidden border-accent-cyan/20 shadow-[0_0_50px_rgba(0,229,255,0.05)]"
      >
        {/* Bioluminescent Top Bar */}
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-accent-cyan via-accent-green to-accent-lime"></div>

        <div className="text-center">
          <div className="mx-auto h-20 w-20 flex items-center justify-center rounded-[2.5rem] bg-accent-cyan/10 border border-accent-cyan/20 shadow-2xl shadow-accent-cyan/20 mb-8 animate-float">
            <UserPlusIcon className="h-10 w-10 text-accent-cyan" />
          </div>
          <h2 className="text-4xl font-bold text-white tracking-tighter">
            Register <span className="text-gradient">Sector</span>
          </h2>
          <p className="mt-4 text-sm text-gray-400 font-light italic">
            Initialize your agricultural data node.
          </p>
        </div>

        <form className="mt-10 space-y-6" onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 gap-6">

            {/* FULL NAME */}
            <div className="group">
              <label className="block text-[10px] font-bold text-accent-cyan uppercase tracking-widest mb-2 ml-1">
                Coordinator Name
              </label>
              <div className="relative">
                <input
                  name="name"
                  type="text"
                  required
                  className="glass-input pl-10 border-white/10 focus:border-accent-cyan/50"
                  placeholder="Enter full name"
                  value={formData.name}
                  onChange={handleChange}
                />
                <ShieldCheckIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-600 group-hover:text-accent-cyan transition-colors" />
              </div>
            </div>

            {/* EMAIL */}
            <div className="group">
              <label className="block text-[10px] font-bold text-accent-cyan uppercase tracking-widest mb-2 ml-1">
                Network Identifier (Email)
              </label>
              <div className="relative">
                <input
                  name="email"
                  type="email"
                  required
                  className="glass-input pl-10 border-white/10 focus:border-accent-cyan/50"
                  placeholder="name@sector.com"
                  value={formData.email}
                  onChange={handleChange}
                />
                <EnvelopeIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-600 group-hover:text-accent-cyan transition-colors" />
              </div>
            </div>

            {/* PASSWORDS GRID */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="group">
                <label className="block text-[10px] font-bold text-accent-cyan uppercase tracking-widest mb-2 ml-1">
                  Access Key
                </label>
                <div className="relative">
                  <input
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    className="glass-input pr-10 border-white/10"
                    placeholder="Create key"
                    value={formData.password}
                    onChange={handleChange}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-600 hover:text-accent-cyan"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeSlashIcon className="h-4 w-4" /> : <EyeIcon className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <div className="group">
                <label className="block text-[10px] font-bold text-accent-cyan uppercase tracking-widest mb-2 ml-1">
                  Confirm Key
                </label>
                <div className="relative">
                  <input
                    name="confirmPassword"
                    type={showConfirmPassword ? 'text' : 'password'}
                    required
                    className="glass-input pr-10 border-white/10"
                    placeholder="Repeat key"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-600 hover:text-accent-cyan"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  >
                    {showConfirmPassword ? <EyeSlashIcon className="h-4 w-4" /> : <EyeIcon className="h-4 w-4" />}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full py-4 text-lg font-black uppercase tracking-widest group relative overflow-hidden"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                  Planting Node...
                </div>
              ) : (
                'Plant Identity'
              )}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
            </button>
          </div>

          <div className="text-center pt-2">
            <p className="text-xs text-gray-500 uppercase tracking-widest font-bold">
              Already Synced?{' '}
              <button
                type="button"
                onClick={onSwitchToLogin}
                className="text-accent-green hover:text-white transition-colors"
              >
                Access Gateway
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
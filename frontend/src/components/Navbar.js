import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation } from 'react-router-dom';
import gsap from 'gsap';
// Keep HeroIcons for standard navigation
import {
  HomeIcon,
  ChatBubbleLeftRightIcon,
  CloudIcon,
  CurrencyDollarIcon,
  MicrophoneIcon,
  Bars3Icon,
  XMarkIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/react/24/outline';

// Import Leaf and Sprout for the "Plant" identity
import { Leaf, Sprout } from 'lucide-react';

const Navbar = ({ user, onLogout }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const navRef = useRef(null);
  const linksRef = useRef([]);

  const navigation = [
    { name: 'Home', href: '/', icon: HomeIcon },
    { name: 'Advisor', href: '/chat', icon: ChatBubbleLeftRightIcon },
    { name: 'Climate', href: '/weather', icon: CloudIcon },
    { name: 'Crops', href: '/crops', icon: Sprout }, // Swapped Sparkles for Sprout
    { name: 'Finance', href: '/finance', icon: CurrencyDollarIcon },
    { name: 'Voice', href: '/voice', icon: MicrophoneIcon },
  ];

  useEffect(() => {
    gsap.fromTo(linksRef.current,
      { opacity: 0, y: -20 },
      { opacity: 1, y: 0, duration: 0.8, stagger: 0.1, ease: "power3.out" }
    );
  }, []);

  return (
    <nav ref={navRef} className="fixed w-full z-50 transition-all duration-500 bg-nature-900/40 backdrop-blur-2xl border-b border-white/5 selection:bg-accent-green/30">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between h-20">

          {/* --- BRAND LOGO (PLANT THEMED) --- */}
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center group relative">
              <div className="absolute -inset-2 bg-accent-green/20 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative flex items-center">
                {/* BRAND ICON: Swapped Sparkles for Leaf */}
                <Leaf className="h-8 w-8 text-accent-green animate-pulse-slow transform group-hover:rotate-12 transition-transform duration-500" />
                <span className="ml-3 font-black text-2xl tracking-tighter uppercase italic">
                  <span className="text-white">Agri</span>
                  <span className="text-gradient">AI</span>
                </span>
              </div>
            </Link>
          </div>

          {/* --- DESKTOP NODES --- */}
          <div className="hidden md:flex items-center space-x-1">
            {navigation.map((item, index) => {
              const isActive = location.pathname === item.href;
              const Icon = item.icon; // Handle component reference correctly
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  ref={el => linksRef.current[index] = el}
                  className={`relative px-5 py-2 rounded-full text-xs font-bold uppercase tracking-widest transition-all duration-500 group
                    ${isActive ? 'text-white' : 'text-gray-500 hover:text-white'}`}
                >
                  <div className="flex items-center relative z-10">
                    <Icon className={`h-4 w-4 mr-2 transition-colors ${isActive ? 'text-accent-green' : 'text-gray-600 group-hover:text-accent-green'}`} />
                    {item.name}
                  </div>
                  {isActive && (
                    <div className="absolute inset-0 bg-white/5 border border-white/10 rounded-full shadow-[0_0_20px_rgba(255,255,255,0.05)]" />
                  )}
                </Link>
              );
            })}

            <div className="h-4 w-px bg-white/10 mx-4" />

            {/* --- USER PROFILE NODE --- */}
            <div ref={el => linksRef.current[6] = el}>
              {user ? (
                <div className="flex items-center gap-4 pl-2">
                  <div className="text-right hidden lg:block">
                    <div className="text-[10px] font-black text-white uppercase tracking-tighter leading-none">{user.name}</div>
                    <div className="text-[9px] text-accent-cyan font-bold uppercase tracking-widest mt-1">Sector 01 Alpha</div>
                  </div>
                  <button
                    onClick={onLogout}
                    className="p-2.5 rounded-full bg-red-500/5 border border-red-500/10 text-red-500 hover:bg-red-500 hover:text-white transition-all duration-500"
                    title="Terminate Session"
                  >
                    <ArrowRightOnRectangleIcon className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <Link
                  to="/login"
                  className="btn-primary py-2 px-6 text-[10px] font-black uppercase tracking-[0.2em] rounded-full"
                >
                  Access Gateway
                </Link>
              )}
            </div>
          </div>

          {/* --- MOBILE TOGGLE --- */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 rounded-full bg-white/5 border border-white/10 text-white transition-all active:scale-90"
            >
              {isOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* --- MOBILE MENU --- */}
      <div className={`md:hidden overflow-hidden transition-all duration-700 ease-in-out ${isOpen ? 'max-h-screen opacity-100' : 'max-h-0 opacity-0'}`}>
        <div className="bg-nature-900/95 backdrop-blur-3xl px-6 py-10 space-y-4 border-t border-white/5">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setIsOpen(false)}
                className={`flex items-center p-4 rounded-[2rem] border transition-all duration-500
                  ${location.pathname === item.href
                    ? 'bg-accent-green/10 border-accent-green/30 text-white'
                    : 'bg-white/5 border-white/5 text-gray-400'}`}
              >
                <Icon className={`h-6 w-6 mr-4 ${location.pathname === item.href ? 'text-accent-green' : ''}`} />
                <span className="font-bold uppercase tracking-widest text-sm">{item.name}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
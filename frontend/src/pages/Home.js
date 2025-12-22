import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import gsap from 'gsap';
import Spline from '@splinetool/react-spline'; // Ensure this is installed
import {
  ChatBubbleLeftRightIcon,
  CloudIcon,
  SparklesIcon,
  CurrencyDollarIcon,
  MicrophoneIcon,
  LightBulbIcon,
  ShieldCheckIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';

const Home = () => {
  const containerRef = useRef(null);
  const cardsRef = useRef([]);
  const blobRef = useRef(null);
  const particlesRef = useRef(null);

  const features = [
    {
      name: 'AI Chat Assistant',
      description: 'Ask questions about farming, weather, crops, and get intelligent responses',
      icon: ChatBubbleLeftRightIcon,
      href: '/chat',
      color: 'accent-green',
    },
    {
      name: 'Weather Intelligence',
      description: 'Get real-time weather data and agricultural alerts for your location',
      icon: CloudIcon,
      href: '/weather',
      color: 'accent-cyan',
    },
    {
      name: 'Crop Recommendations',
      description: 'Get personalized crop suggestions based on soil, weather, and market conditions',
      icon: SparklesIcon,
      href: '/crops',
      color: 'accent-lime',
    },
    {
      name: 'Financial Guidance',
      description: 'Access credit schemes, subsidies, and market price information',
      icon: CurrencyDollarIcon,
      href: '/finance',
      color: 'amber-400',
    },
    {
      name: 'Voice Interface',
      description: 'Use voice commands in multiple Indian languages for easy access',
      icon: MicrophoneIcon,
      href: '/voice',
      color: 'indigo-400',
    }
  ];

  const benefits = [
    { title: 'Multi-Language Support', description: 'Available in 10 Indian languages', icon: GlobeAltIcon },
    { title: 'Offline Capability', description: 'Core features work without internet', icon: ShieldCheckIcon },
    { title: 'Expert Knowledge', description: 'Powered by government data sources', icon: LightBulbIcon }
  ];

  useEffect(() => {
    // 1. Initial Entrance Animation
    gsap.fromTo(cardsRef.current,
      { y: 80, opacity: 0 },
      { y: 0, opacity: 1, duration: 1.2, stagger: 0.1, ease: "power4.out" }
    );

    // 2. Continuous Antigravity Floating
    cardsRef.current.forEach((card, i) => {
      if (!card) return;
      gsap.to(card, {
        y: "-=20",
        duration: 3 + Math.random(),
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
        delay: i * 0.15
      });
    });

    // 3. Background Parallax Logic
    const handleMouseMove = (e) => {
      const { clientX, clientY } = e;
      const xPos = (clientX / window.innerWidth - 0.5) * 40;
      const yPos = (clientY / window.innerHeight - 0.5) * 40;

      gsap.to(particlesRef.current, { x: xPos, y: yPos, duration: 2, ease: "power2.out" });
      gsap.to(blobRef.current, { x: xPos * -0.8, y: yPos * -0.8, duration: 4, ease: "power2.out" });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      gsap.killTweensOf(cardsRef.current);
    };
  }, []);

  return (
    <div ref={containerRef} className="page-container selection:bg-accent-green/30">

      {/* --- LAYER 1: BIOPHILIC BACKGROUND --- */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="page-overlay" />
        {/* Organic Texture */}
        <div className="absolute inset-0 bg-grain opacity-[0.03]" />

        {/* Interactive "Pollen" Particles */}
        <div ref={particlesRef} className="absolute inset-0">
          {[...Array(20)].map((_, i) => (
            <div key={i} className="absolute bg-accent-green/20 rounded-full blur-[2px]"
              style={{
                width: Math.random() * 6 + 2 + 'px',
                height: Math.random() * 6 + 2 + 'px',
                top: Math.random() * 100 + '%',
                left: Math.random() * 100 + '%',
              }}
            />
          ))}
        </div>

        {/* Floating Light Blob */}
        <div ref={blobRef} className="absolute top-1/4 -right-20 w-[600px] h-[600px] bg-emerald-500/10 rounded-full blur-[120px]" />
      </div>

      {/* --- LAYER 2: CONTENT --- */}
      <div className="content-wrapper relative z-10">

        {/* HERO SECTION: AI Biosphere */}
        <div className="flex flex-col lg:flex-row items-center justify-between gap-12 py-16 lg:py-24">
          <div className="lg:w-1/2 text-left">
            <div className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full border border-accent-green/20 bg-accent-green/5 text-accent-green text-sm backdrop-blur-md animate-fade-in">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-green opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-green"></span>
              </span>
              AI Soil Intelligence Active
            </div>
            <h1 className="text-6xl lg:text-8xl font-bold tracking-tighter mb-6 leading-[0.9]">
              Nurture your <br />
              <span className="text-gradient">Harvest.</span>
            </h1>
            <p className="text-xl text-gray-400 leading-relaxed max-w-lg mb-10">
              Welcome back to <span className="text-white font-medium">AgriAI</span>.
              Today's data shows high soil resilience. Let's optimize your yields.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link to="/chat" className="btn-primary">Start Chatting</Link>
              <Link to="/weather" className="btn-secondary">Check Weather</Link>
            </div>
          </div>

          {/* 3D CENTERPIECE */}
          <div className="lg:w-1/2 h-[500px] w-full relative group">
            <div className="absolute inset-0 bg-accent-green/5 blur-[100px] rounded-full group-hover:bg-accent-green/10 transition-all duration-700" />
            {/* REPLACE the URL below with your Spline scene URL */}
            <Spline scene="https://prod.spline.design/GZe9sGdBXwITKlqh/scene.splinecode" />
          </div>
        </div>

        {/* FEATURES GRID */}
        <div className="py-20">
          <h2 className="text-3xl font-bold text-center text-white mb-16">
            Intelligent Advisor Modules
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Link
                key={feature.name}
                to={feature.href}
                ref={el => cardsRef.current[index] = el}
                className="glass-card group relative overflow-hidden"
              >
                <div className={`w-14 h-14 rounded-2xl bg-${feature.color}/10 flex items-center justify-center mb-6 ring-1 ring-${feature.color}/20 group-hover:ring-${feature.color}/50 transition-all duration-500`}>
                  <feature.icon className={`h-7 w-7 text-${feature.color}`} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-3 group-hover:text-accent-green transition-colors">
                  {feature.name}
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  {feature.description}
                </p>
                {/* Glow effect */}
                <div className={`absolute -bottom-10 -right-10 w-32 h-32 bg-${feature.color}/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity`} />
              </Link>
            ))}
          </div>
        </div>

        {/* BENEFITS SECTION */}
        <div className="py-20 my-20 glass-card bg-opacity-[0.02]">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {benefits.map((benefit) => (
              <div key={benefit.title} className="text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-accent-green to-emerald-700 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-accent-green/10 group-hover:scale-110 group-hover:rotate-3 transition-all duration-500">
                  <benefit.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">{benefit.title}</h3>
                <p className="text-gray-500 group-hover:text-gray-400 transition-colors">{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* FOOTER */}
        <footer className="py-12 text-center border-t border-white/5 opacity-50">
          <p className="text-sm tracking-widest uppercase">Built for the future of Indian Agriculture</p>
        </footer>
      </div>
    </div>
  );
};

export default Home;
import React, { useState, useEffect, useRef } from 'react';
import { MapPinIcon, BellAlertIcon, BeakerIcon, SunIcon as HeroSun } from '@heroicons/react/24/outline';
import { useCurrentWeather, useWeatherForecast, useWeatherAlerts, useWeatherRecommendations } from '../hooks/useAPI';
import { Sun, Cloud, CloudRain, CloudSnow, CloudLightning, ShieldCheck, AlertTriangle, Activity } from 'lucide-react';
import toast from 'react-hot-toast';
import gsap from 'gsap';

const Weather = () => {
  const [location, setLocation] = useState({ lat: 28.6139, lng: 77.2090 });
  const [isLocationEnabled, setIsLocationEnabled] = useState(false);

  // Refs for Animations
  const cardsRef = useRef([]);
  const headerRef = useRef(null);

  const { data: weatherData, isLoading: weatherLoading } = useCurrentWeather(location.lat, location.lng, isLocationEnabled);
  const { data: forecastData } = useWeatherForecast(location.lat, location.lng, 7, isLocationEnabled);
  const { data: alertsData } = useWeatherAlerts(location.lat, location.lng, isLocationEnabled);
  const { data: recommendationsData } = useWeatherRecommendations(location.lat, location.lng, isLocationEnabled);

  useEffect(() => {
    // Header Entrance
    gsap.fromTo(headerRef.current, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 1, ease: "power3.out" });

    // Cards Entrance
    if (!weatherLoading) {
      gsap.fromTo(cardsRef.current,
        { opacity: 0, scale: 0.9, y: 40 },
        { opacity: 1, scale: 1, y: 0, duration: 0.8, stagger: 0.15, ease: "back.out(1.2)" }
      );
    }
  }, [weatherLoading]);

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setLocation({ lat: position.coords.latitude, lng: position.coords.longitude });
        setIsLocationEnabled(true);
        toast.success('Location Synced!');
      });
    }
  };

  // Helper to get the correct Lucide icon based on weather description
  const getWeatherIcon = (description, gradient) => {
    const desc = description.toLowerCase();
    const iconProps = { 
      size: 48, 
      className: `text-transparent bg-clip-text bg-gradient-to-br ${gradient} drop-shadow-md` 
    };

    if (desc.includes('clear')) return <Sun {...iconProps} className="text-orange-400 drop-shadow-lg" />;
    if (desc.includes('rain') || desc.includes('drizzle')) return <CloudRain {...iconProps} className="text-blue-400 drop-shadow-lg" />;
    if (desc.includes('snow')) return <CloudSnow {...iconProps} className="text-sky-200 drop-shadow-lg" />;
    if (desc.includes('storm') || desc.includes('thunder')) return <CloudLightning {...iconProps} className="text-indigo-400 drop-shadow-lg" />;
    if (desc.includes('cloud')) return <Cloud {...iconProps} className="text-gray-200 drop-shadow-lg" />;
    
    return <Sun {...iconProps} className="text-yellow-400" />;
  };

  return (
    <div className="page-container min-h-screen pb-20">
      <div className="page-overlay opacity-40" />

      <div className="content-wrapper relative z-10">

        {/* --- HEADER --- */}
        <header ref={headerRef} className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div>
            <h1 className="text-5xl lg:text-6xl font-bold tracking-tighter text-white">
              Atmospheric <span className="text-gradient">Intelligence</span>
            </h1>
            <p className="text-gray-400 mt-2">Precision climate analytics for Field Sector {location.lat.toFixed(2)}</p>
          </div>
          <button onClick={getUserLocation} className="btn-secondary group flex items-center gap-2">
            <MapPinIcon className="h-5 w-5 text-accent-green group-hover:animate-bounce" />
            Sync Local Atmosphere
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* --- MAIN WEATHER NODE (Left 5 Cols) --- */}
          <div ref={el => cardsRef.current[0] = el} className="lg:col-span-5 flex flex-col gap-8">
            <div className="glass-card relative overflow-hidden group border-accent-cyan/20 bg-accent-cyan/5">
              <div className="absolute top-0 right-0 p-6 opacity-20 group-hover:opacity-40 transition-opacity">
                <HeroSun className="h-32 w-32 text-accent-cyan animate-pulse-slow" />
              </div>

              <h2 className="text-accent-cyan font-bold uppercase tracking-widest text-xs mb-8">Live Telemetry</h2>

              {weatherLoading ? (
                <div className="h-40 flex items-center justify-center animate-pulse text-accent-cyan">Reading Sensors...</div>
              ) : (
                <div className="relative z-10">
                  <div className="text-8xl font-bold text-white tracking-tighter mb-2">
                    {weatherData?.data?.temperature || '--'}  
                  </div>
                  <div className="text-2xl text-gray-300 capitalize font-light mb-8 italic">
                    {weatherData?.data?.description || 'Clear Skies'}
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 rounded-3xl bg-white/5 border border-white/5">
                      <span className="text-gray-500 text-xs uppercase font-bold block mb-1">Humidity</span>
                      <span className="text-2xl text-white">{weatherData?.data?.humidity}%</span>
                    </div>
                    <div className="p-4 rounded-3xl bg-white/5 border border-white/5">
                      <span className="text-gray-500 text-xs uppercase font-bold block mb-1">Precipitation</span>
                      <span className="text-2xl text-white">{weatherData?.data?.rainfall || 0}mm</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Recommendations Node */}
            <div ref={el => cardsRef.current[1] = el} className="glass-card border-accent-lime/20 bg-accent-lime/5">
              <div className="flex items-center gap-3 mb-6">
                <BeakerIcon className="h-6 w-6 text-accent-lime" />
                <h2 className="text-xl font-bold text-white">AI Cultivation Strategy</h2>
              </div>
              <div className="space-y-4">
                {recommendationsData?.data?.recommendations?.map((rec, i) => (
                  <div key={i} className="text-sm p-4 rounded-2xl bg-white/5 border border-white/5 hover:border-accent-lime/30 transition-colors">
                    <span className="text-accent-lime font-bold block mb-1">{rec.title}</span>
                    <p className="text-gray-400">{rec.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* --- ALERTS & FORECAST (Right 7 Cols) --- */}
          <div ref={el => cardsRef.current[2] = el} className="lg:col-span-7 flex flex-col gap-8">

            {/* Alerts Node (Upgraded High-Tech Look) */}
            <div className="glass-card relative overflow-hidden">
              {/* Header with Live Pulse */}
              <div className="flex items-center justify-between mb-6 relative z-10">
                <div className="flex items-center gap-3">
                    <div className="p-2 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-500">
                        <BellAlertIcon className="h-6 w-6" />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-white">Critical Alerts</h2>
                        <p className="text-xs text-gray-400 flex items-center gap-1">
                           <Activity size={12} className="text-accent-green" /> 
                           Real-time Monitoring Active
                        </p>
                    </div>
                </div>
                {/* Live Indicator */}
                <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/5 backdrop-blur-sm">
                   <span className="relative flex h-2 w-2">
                     <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-green opacity-75"></span>
                     <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-green"></span>
                   </span>
                   <span className="text-[10px] font-bold text-accent-green tracking-wider">LIVE</span>
                </div>
              </div>

              <div className="space-y-3 relative z-10">
                {alertsData?.data?.alerts?.length > 0 ? (
                  // --- ACTIVE ALERT STATE (Red/Amber Warning) ---
                  alertsData.data.alerts.map((alert, i) => (
                    <div key={i} className="relative overflow-hidden p-6 rounded-[2rem] bg-gradient-to-br from-amber-900/40 via-orange-900/20 to-black/40 border border-amber-500/50 group hover:scale-[1.02] transition-transform duration-300">
                      
                      {/* Animated Background Pulse */}
                      <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity animate-pulse">
                         <AlertTriangle size={120} />
                      </div>

                      <div className="flex items-start gap-5 relative z-10">
                         <div className="p-3 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-600 shadow-lg shadow-orange-500/20 shrink-0">
                            <AlertTriangle className="h-6 w-6 text-white" />
                         </div>
                         <div>
                            <div className="font-bold text-amber-400 text-lg mb-1 tracking-wide uppercase flex items-center gap-2">
                               {alert.title}
                               <span className="px-2 py-0.5 rounded text-[10px] bg-amber-500/20 border border-amber-500/30 text-amber-200">CRITICAL</span>
                            </div>
                            <p className="text-sm text-gray-300 leading-relaxed font-light">{alert.message}</p>
                         </div>
                      </div>
                    </div>
                  ))
                ) : (
                  // --- SAFE STATE (Glowing Green Shield) ---
                  <div className="relative overflow-hidden py-12 px-6 rounded-[2rem] bg-gradient-to-br from-emerald-900/10 via-teal-900/5 to-black/20 border border-emerald-500/10 text-center flex flex-col items-center justify-center gap-4 group hover:border-emerald-500/30 transition-all duration-500">
                    
                    {/* Background Radar Effect */}
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-emerald-500/5 via-transparent to-transparent opacity-50 group-hover:opacity-100 transition-opacity duration-700"></div>

                    {/* Animated Icon Container */}
                    <div className="relative group-hover:scale-110 transition-transform duration-500">
                        <div className="absolute inset-0 bg-emerald-500 blur-2xl opacity-20 rounded-full animate-pulse-slow"></div>
                        <div className="bg-gradient-to-br from-emerald-500/20 to-teal-500/10 p-5 rounded-full border border-emerald-500/20 relative z-10 shadow-[0_0_30px_-5px_rgba(16,185,129,0.3)]">
                            <ShieldCheck className="w-12 h-12 text-emerald-400 drop-shadow-md" />
                        </div>
                    </div>

                    <div className="relative z-10">
                        <h3 className="text-white font-bold text-lg mb-1 tracking-tight">Atmosphere Stable</h3>
                        <p className="text-emerald-400/60 text-xs uppercase tracking-widest font-medium">
                            No Anomalies Detected
                        </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Forecast Node (UPDATED: Colorful & Creative) */}
            <div className="glass-card overflow-hidden relative">
              <div className="flex justify-between items-end mb-6">
                 <div>
                   <h2 className="text-xl font-bold bg-gradient-to-r from-white via-accent-green to-accent-cyan bg-clip-text text-transparent">
                     7-Day Projection
                   </h2>
                   <p className="text-xs text-gray-400 mt-1">AI-Predicted Atmospheric Trend</p>
                 </div>
                 <div className="h-1 w-20 bg-gradient-to-r from-accent-green to-transparent rounded-full opacity-50"></div>
              </div>

              <div className="flex gap-4 overflow-x-auto pb-8 pt-4 px-2 no-scrollbar snap-x p-2">
                {forecastData?.data?.forecasts?.map((day, i) => {
                  const isToday = i === 0;
                  const weatherDesc = day.description.toLowerCase();
                  
                  // Dynamic Color Logic
                  let gradient = 'from-gray-400 via-gray-300 to-gray-500';
                  let glowColor = 'rgba(255,255,255,0.1)';

                  if (weatherDesc.includes('clear')) {
                    gradient = 'from-orange-400 via-yellow-300 to-orange-500';
                    glowColor = 'rgba(255, 165, 0, 0.4)';
                  } else if (weatherDesc.includes('cloud')) {
                    gradient = 'from-blue-400 via-blue-300 to-blue-500';
                    glowColor = 'rgba(135, 206, 235, 0.4)';
                  } else if (weatherDesc.includes('rain') || weatherDesc.includes('drizzle')) {
                    gradient = 'from-indigo-400 via-blue-500 to-indigo-600';
                    glowColor = 'rgba(75, 0, 130, 0.4)';
                  }

                  return (
                    <div 
                      key={i} 
                      className={`
                        snap-center min-w-[150px] p-5 rounded-[2.5rem] border transition-all duration-500 group relative overflow-hidden
                        flex flex-col items-center justify-between gap-5
                        bg-gradient-to-br ${isToday ? 'from-accent-green/40 via-emerald-500/20 to-teal-600/10' : `${gradient.split(' ')[0]}/30 ${gradient.split(' ')[2]}/10`}
                        ${isToday 
                          ? 'border-accent-green/60 shadow-[0_0_40px_-10px_rgba(0,255,127,0.5)] scale-105 z-10' 
                          : `border-white/10 hover:border-white/30 hover:-translate-y-3 hover:shadow-[0_10px_30px_-10px_${glowColor}]`
                        }
                      `}
                    >
                      {/* Date Badge */}
                      <div className={`
                        px-4 py-1.5 rounded-full text-[11px] font-bold tracking-wider uppercase shadow-sm
                        ${isToday ? 'bg-accent-green text-black' : 'bg-black/40 text-white/80 backdrop-blur-md'}
                      `}>
                        {isToday ? 'Today' : new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}
                      </div>

                      {/* Dynamic Lucide Icon */}
                      <div className="relative z-10 my-2 transform group-hover:scale-110 group-hover:rotate-3 transition-all duration-500">
                         {/* Back Glow */}
                         <div className={`absolute inset-0 blur-2xl rounded-full scale-125 opacity-0 group-hover:opacity-70 transition-opacity duration-500 bg-gradient-to-tr ${gradient}`} />
                         {getWeatherIcon(weatherDesc, gradient)}
                      </div>

                      {/* Temperature & Desc */}
                      <div className="text-center relative z-10">
                        <div className="text-5xl font-extrabold text-white tracking-tighter mb-2 flex justify-center leading-none">
                          {Math.round(day.temperature)}
                          <span className={`text-3xl align-super ${isToday ? 'text-accent-green' : 'text-white/70'}`}>°</span>
                        </div>
                        <div className="text-xs font-bold text-white/90 uppercase tracking-widest group-hover:text-white transition-colors">
                          {day.description}
                        </div>
                      </div>
                      
                      {/* Glassy Shine Overlay */}
                      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-white/5 to-black/20 pointer-events-none rounded-[2.5rem]" />
                    </div>
                  );
                })}
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default Weather;
import React, { useState, useEffect, useRef } from 'react';
import { CloudIcon, SunIcon, MapPinIcon, BellAlertIcon, BeakerIcon } from '@heroicons/react/24/outline';
import { useCurrentWeather, useWeatherForecast, useWeatherAlerts, useWeatherRecommendations } from '../hooks/useAPI';
import toast from 'react-hot-toast';
import gsap from 'gsap';

const Weather = () => {
  const [location, setLocation] = useState({ lat: 28.6139, lng: 77.2090 });
  const [isLocationEnabled, setIsLocationEnabled] = useState(false);

  // Refs for Antigravity Animations
  const cardsRef = useRef([]);
  const headerRef = useRef(null);

  const { data: weatherData, isLoading: weatherLoading, refetch: refetchWeather } = useCurrentWeather(location.lat, location.lng, isLocationEnabled);
  const { data: forecastData } = useWeatherForecast(location.lat, location.lng, 7, isLocationEnabled);
  const { data: alertsData } = useWeatherAlerts(location.lat, location.lng, isLocationEnabled);
  const { data: recommendationsData } = useWeatherRecommendations(location.lat, location.lng, isLocationEnabled);

  useEffect(() => {
    // Entrance Animation
    gsap.fromTo(headerRef.current, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 1, ease: "power3.out" });

    if (!weatherLoading && weatherData) {
      gsap.fromTo(cardsRef.current,
        { opacity: 0, scale: 0.9, y: 40 },
        { opacity: 1, scale: 1, y: 0, duration: 0.8, stagger: 0.15, ease: "back.out(1.2)" }
      );
    }
  }, [weatherLoading, weatherData]);

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setLocation({ lat: position.coords.latitude, lng: position.coords.longitude });
        setIsLocationEnabled(true);
        toast.success('Location Synced!');
      });
    }
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
                <SunIcon className="h-32 w-32 text-accent-cyan animate-pulse-slow" />
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

            {/* Alerts Node */}
            <div className="glass-card">
              <div className="flex items-center gap-3 mb-6">
                <BellAlertIcon className="h-6 w-6 text-amber-500" />
                <h2 className="text-xl font-bold text-white">Critical Alerts</h2>
              </div>
              <div className="space-y-3">
                {alertsData?.data?.alerts?.length > 0 ? alertsData.data.alerts.map((alert, i) => (
                  <div key={i} className="p-5 rounded-3xl bg-amber-500/10 border border-amber-500/20 text-white animate-float">
                    <div className="font-bold text-amber-400 mb-1">{alert.title}</div>
                    <p className="text-sm text-gray-300">{alert.message}</p>
                  </div>
                )) : (
                  <div className="py-10 text-center text-gray-500 border-2 border-dashed border-white/5 rounded-3xl">
                    Atmosphere is stable. No alerts detected.
                  </div>
                )}
              </div>
            </div>

            {/* Forecast Node */}
            <div className="glass-card">
              <h2 className="text-xl font-bold text-white mb-6">7-Day Projection</h2>
              <div className="flex gap-4 overflow-x-auto pb-4 no-scrollbar">
                {forecastData?.data?.forecast?.map((day, i) => (
                  <div key={i} className="min-w-[120px] p-5 rounded-3xl bg-white/5 border border-white/5 text-center hover:bg-accent-green/10 hover:border-accent-green/30 transition-all group">
                    <div className="text-xs font-bold text-gray-500 uppercase mb-3">
                      {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' })}
                    </div>
                    <div className="text-3xl font-bold text-white mb-2 group-hover:scale-110 transition-transform">
                      {day.temperature}  
                    </div>
                    <div className="text-[10px] text-gray-400 uppercase tracking-widest">{day.description}</div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default Weather;
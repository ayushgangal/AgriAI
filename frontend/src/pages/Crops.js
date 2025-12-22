import React, { useState, useEffect, useRef } from 'react';
import { SparklesIcon, MapPinIcon, BeakerIcon, LifebuoyIcon } from '@heroicons/react/24/outline';
import { useCropRecommendations, useCropManagementAdvice } from '../hooks/useAPI';
import toast from 'react-hot-toast';
import gsap from 'gsap';

const Crops = () => {
  const [selectedCrop, setSelectedCrop] = useState(null);
  const [location, setLocation] = useState({ lat: 28.6139, lng: 77.2090 });
  const [weatherParams, setWeatherParams] = useState({ temperature: 25, rainfall: 0, humidity: 60 });
  const [isLocationEnabled, setIsLocationEnabled] = useState(false);
  const [selectedGrowthStage, setSelectedGrowthStage] = useState('vegetative');

  // Refs for Animations
  const cardsRef = useRef([]);
  const detailRef = useRef(null);

  const { data: cropRecommendations, isLoading: recommendationsLoading, refetch: refetchRecommendations } = useCropRecommendations(
    location.lat, location.lng, weatherParams.temperature, weatherParams.rainfall, weatherParams.humidity, isLocationEnabled
  );

  const { data: managementAdvice, isLoading: adviceLoading } = useCropManagementAdvice(
    selectedCrop?.crop, selectedGrowthStage, location.lat, location.lng, weatherParams.temperature, weatherParams.rainfall, weatherParams.humidity, isLocationEnabled && !!selectedCrop
  );

  // --- NEW: FUNCTION DEFINITIONS ---

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const newLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setLocation(newLocation);
          setIsLocationEnabled(true);
          toast.success('Geo-Coordinates Synced!');
          refetchRecommendations(); // Refresh AI matches for new location
        },
        (error) => {
          console.error('Location Error:', error);
          toast.error('Location Access Denied. Please input manually.');
        }
      );
    } else {
      toast.error('Geolocation is not supported by your browser.');
    }
  };

  // --- ANIMATION LOGIC ---
  useEffect(() => {
    if (!recommendationsLoading && cropRecommendations?.data?.recommendations) {
      gsap.fromTo(cardsRef.current,
        { opacity: 0, x: -30 },
        { opacity: 1, x: 0, duration: 0.8, stagger: 0.1, ease: "power2.out" }
      );

      cardsRef.current.forEach((card, i) => {
        if (!card) return;
        gsap.to(card, {
          y: i % 2 === 0 ? "-=10" : "+=10",
          duration: 3 + Math.random(),
          repeat: -1,
          yoyo: true,
          ease: "sine.inOut"
        });
      });
    }
  }, [recommendationsLoading, cropRecommendations]);

  useEffect(() => {
    if (selectedCrop) {
      gsap.fromTo(detailRef.current, { opacity: 0, scale: 0.95 }, { opacity: 1, scale: 1, duration: 0.5 });
    }
  }, [selectedCrop]);

  const growthStages = ['seedling', 'vegetative', 'flowering', 'fruiting', 'maturity'];

  return (
    <div className="page-container min-h-screen pb-20">
      <div className="page-overlay opacity-30" />

      <div className="content-wrapper relative z-10">
        <header className="mb-12">
          <h1 className="text-5xl lg:text-6xl font-bold tracking-tighter text-white">
            Crop <span className="text-gradient">Intelligence</span>
          </h1>
          <p className="text-gray-400 mt-2 italic font-light">Bio-matching algorithms for optimal harvest cycles.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">

          {/* LEFT: Recommended Crop Nodes */}
          <div className="lg:col-span-7 space-y-6">
            <h2 className="text-accent-green font-bold uppercase tracking-[0.2em] text-xs mb-6">Algorithm Matches</h2>

            {recommendationsLoading ? (
              <div className="h-60 flex flex-col items-center justify-center space-y-4">
                <div className="w-12 h-12 border-4 border-accent-green/20 border-t-accent-green rounded-full animate-spin" />
                <p className="text-accent-green text-sm animate-pulse uppercase tracking-widest">Sequencing soil data...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-4">
                {cropRecommendations?.data?.recommendations?.map((crop, index) => (
                  <div
                    key={index}
                    ref={el => cardsRef.current[index] = el}
                    onClick={() => setSelectedCrop(crop)}
                    className={`glass-card group cursor-pointer border-l-4 transition-all duration-500 
                      ${selectedCrop?.crop === crop.crop ? 'border-accent-green bg-accent-green/5 translate-x-4' : 'border-white/10 hover:border-accent-green/50'}`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className={`p-3 rounded-2xl bg-white/5 group-hover:bg-accent-green/10 transition-colors`}>
                          <SparklesIcon className="h-8 w-8 text-accent-green" />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-white leading-none">{crop.crop}</h3>
                          <p className="text-xs text-gray-500 mt-1 uppercase tracking-tighter">{crop.scientific_name}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-black text-accent-green">{Math.round(crop.suitability_score * 100)}%</div>
                        <div className="text-[10px] text-gray-500 uppercase font-bold">Suitability</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* RIGHT: Crop Details & Bio-Advice */}
          <div className="lg:col-span-5">
            <div ref={detailRef} className="sticky top-24">
              {selectedCrop ? (
                <div className="glass-card border-accent-lime/20 bg-accent-lime/5 overflow-hidden">
                  <div className="absolute -top-10 -right-10 w-40 h-40 bg-accent-lime/10 blur-[60px] rounded-full" />
                  <div className="relative z-10">
                    <div className="flex items-center justify-between mb-8">
                      <h2 className="text-2xl font-bold text-white tracking-tight">{selectedCrop.crop}</h2>
                      <span className="px-3 py-1 rounded-full bg-white/5 text-accent-lime text-[10px] font-bold uppercase ring-1 ring-accent-lime/30">
                        {selectedCrop.category}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-8">
                      <div className="p-4 rounded-3xl bg-black/20 border border-white/5">
                        <span className="text-gray-500 text-[10px] uppercase font-bold block mb-1">Growth Season</span>
                        <span className="text-white font-medium">{selectedCrop.season}</span>
                      </div>
                      <div className="p-4 rounded-3xl bg-black/20 border border-white/5">
                        <span className="text-gray-500 text-[10px] uppercase font-bold block mb-1">Risk Assessment</span>
                        <span className="text-red-400 font-medium">{selectedCrop.disease_risks?.length || 0} Threats</span>
                      </div>
                    </div>

                    <div className="space-y-6">
                      <div>
                        <label className="block text-[10px] font-bold text-accent-lime uppercase tracking-widest mb-3">Target Growth Stage</label>
                        <select
                          value={selectedGrowthStage}
                          onChange={(e) => setSelectedGrowthStage(e.target.value)}
                          className="glass-input text-sm border-white/10"
                        >
                          {growthStages.map((stage) => (
                            <option key={stage} value={stage} className="bg-nature-900">{stage.toUpperCase()}</option>
                          ))}
                        </select>
                      </div>

                      {adviceLoading ? (
                        <p className="text-center text-accent-lime animate-pulse">Analyzing...</p>
                      ) : managementAdvice ? (
                        <div className="space-y-4 pt-4 border-t border-white/10 animate-fade-in">
                          <div className="flex gap-3">
                            <BeakerIcon className="h-5 w-5 text-accent-cyan shrink-0" />
                            <div>
                              <p className="text-xs font-bold text-accent-cyan uppercase mb-1">Irrigation Sync</p>
                              <p className="text-sm text-gray-300 italic">"{managementAdvice.data?.irrigation_advice || "Optimal levels detected."}"</p>
                            </div>
                          </div>
                          <div className="flex gap-3">
                            <LifebuoyIcon className="h-5 w-5 text-accent-lime shrink-0" />
                            <div>
                              <p className="text-xs font-bold text-accent-lime uppercase mb-1">Nutrient Protocol</p>
                              <p className="text-sm text-gray-300 italic">"{managementAdvice.data?.nutrient_advice || "Soil nitrogen sufficient."}"</p>
                            </div>
                          </div>
                        </div>
                      ) : (
                        <button className="btn-primary w-full py-4 rounded-3xl">Analyze Management Protocol</button>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="glass-card flex flex-col items-center justify-center py-20 border-dashed opacity-50">
                  <SparklesIcon className="h-12 w-12 text-gray-600 mb-4 animate-float" />
                  <p className="text-gray-500 text-sm">Select a Genetic Node for Advice</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* --- DYNAMIC SETTINGS DOCK --- */}
        <div className="mt-12 glass-card border-white/5 bg-white/[0.01] hover:bg-white/[0.03] transition-all">
          <div className="flex items-center gap-2 mb-6 text-accent-green">
            <MapPinIcon className="h-5 w-5" />
            <h2 className="text-sm font-bold uppercase tracking-widest">Environmental Sensors</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {['Temperature', 'Rainfall', 'Humidity'].map((param) => (
              <div key={param}>
                <label className="block text-[10px] text-gray-500 font-bold uppercase mb-2">{param}</label>
                <input
                  type="number"
                  value={weatherParams[param.toLowerCase()]}
                  onChange={(e) => setWeatherParams(prev => ({ ...prev, [param.toLowerCase()]: parseFloat(e.target.value) || 0 }))}
                  className="glass-input"
                />
              </div>
            ))}
            <div className="flex items-end">
              <button onClick={getUserLocation} className="btn-secondary w-full py-4 text-xs font-bold uppercase tracking-tighter">Sync Geo-Coordinates</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Crops;
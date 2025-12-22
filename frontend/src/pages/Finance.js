import React, { useState, useEffect, useRef } from 'react';
import { CurrencyDollarIcon, CalculatorIcon, ArrowTrendingUpIcon, ArrowTrendingDownIcon, BanknotesIcon } from '@heroicons/react/24/outline';
import { useLoanCalculator, useMarketTrends, useFinancialInfo } from '../hooks/useAPI';
import toast from 'react-hot-toast';
import gsap from 'gsap';

const Finance = () => {
  const [selectedScheme, setSelectedScheme] = useState(null);
  const [loanParams, setLoanParams] = useState({ amount: 100000, tenure: 60, loanType: 'crop_loan' });

  // Refs for Antigravity & Pollen Animations
  const cardsRef = useRef([]);
  const bubblesRef = useRef([]);
  const containerRef = useRef(null);

  const { data: loanCalculation, isLoading: loanLoading } = useLoanCalculator(loanParams.amount, loanParams.tenure, loanParams.loanType, true);
  const { data: marketTrends, isLoading: trendsLoading } = useMarketTrends();
  const { data: financialSchemes, isLoading: infoLoading } = useFinancialInfo();

  const creditSchemes = financialSchemes?.data?.credit_schemes || [];

  // Logic for calculations
  const calculateEMI = (principal, rate, time) => {
    const monthlyRate = rate / 12 / 100;
    const emi = principal * monthlyRate * Math.pow(1 + monthlyRate, time) / (Math.pow(1 + monthlyRate, time) - 1);
    return Math.round(emi);
  };

  const emi = loanCalculation?.data?.monthly_emi || calculateEMI(loanParams.amount, 9.0, loanParams.tenure);
  const totalAmount = emi * loanParams.tenure;
  const totalInterest = totalAmount - loanParams.amount;

  // --- ANIMATION LOGIC ---
  useEffect(() => {
    // 1. Entrance Stagger for cards
    gsap.fromTo(cardsRef.current,
      { opacity: 0, y: 50 },
      { opacity: 1, y: 0, duration: 1, stagger: 0.2, ease: "power4.out" }
    );

    // 2. Pollen Bubbles Floating Logic
    bubblesRef.current.forEach((bubble, i) => {
      if (!bubble) return;
      gsap.to(bubble, {
        y: "-=30",
        x: "+=15",
        duration: 3 + Math.random() * 2,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
        delay: i * 0.3
      });
    });
  }, [trendsLoading, marketTrends]);

  return (
    <div ref={containerRef} className="page-container min-h-screen pb-20">
      <div className="page-overlay opacity-30" />

      <div className="content-wrapper relative z-10">
        <header className="mb-12">
          <h1 className="text-5xl lg:text-6xl font-bold tracking-tighter text-white">
            Capital <span className="text-gradient">Intelligence</span>
          </h1>
          <p className="text-gray-400 mt-2 font-light">Secure credit protocols and real-time market pollination.</p>
        </header>

        <div className="grid grid-cols-1 xl:grid-cols-12 gap-10">

          {/* --- LEFT: CREDIT SCHEMES (The Bank Vault) --- */}
          <div ref={el => cardsRef.current[0] = el} className="xl:col-span-5 space-y-6">
            <div className="flex items-center justify-between px-2">
              <h2 className="text-sm font-bold text-accent-cyan uppercase tracking-widest">Active Credit Nodes</h2>
              <span className="text-[10px] bg-accent-cyan/10 text-accent-cyan px-2 py-1 rounded-md border border-accent-cyan/20">
                {creditSchemes.length} FOUND
              </span>
            </div>

            <div className="space-y-4 max-h-[700px] overflow-y-auto no-scrollbar pr-2">
              {creditSchemes.map((scheme, index) => (
                <div
                  key={index}
                  onClick={() => setSelectedScheme(scheme)}
                  className={`glass-card group cursor-pointer border-l-2 transition-all duration-500 
                    ${selectedScheme?.scheme_name === scheme.scheme_name ? 'border-accent-cyan bg-accent-cyan/5 scale-[1.02]' : 'border-white/5 hover:border-accent-cyan/40'}`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold text-lg text-white group-hover:text-accent-cyan transition-colors">{scheme.scheme_name}</h3>
                      <p className="text-xs text-gray-500 uppercase tracking-tighter">{scheme.bank_name || 'Central Reserve'}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-black text-accent-cyan">{scheme.interest_rate}%</div>
                      <div className="text-[10px] text-gray-500 font-bold uppercase">Annual Rate</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* --- RIGHT: MARKET POLLEN & CALCULATOR --- */}
          <div className="xl:col-span-7 space-y-10">

            {/* Market Pollen Bubbles Section */}
            <div ref={el => cardsRef.current[1] = el} className="relative h-[300px] glass-card overflow-hidden bg-accent-green/[0.02]">
              <h2 className="absolute top-6 left-6 text-xs font-bold text-accent-green uppercase tracking-widest z-20">Market Pollination</h2>

              <div className="relative h-full w-full flex flex-wrap items-center justify-center gap-6 p-10">
                {marketTrends?.data?.prices ? marketTrends.data.prices.map((item, i) => (
                  <div
                    key={i}
                    ref={el => bubblesRef.current[i] = el}
                    className="flex flex-col items-center justify-center w-28 h-28 rounded-full glass-card border-white/10 bg-white/[0.02] backdrop-blur-md transition-transform hover:scale-110 cursor-default"
                  >
                    <span className="text-[10px] font-bold text-gray-500 uppercase">{item.crop}</span>
                    <span className="text-lg font-black text-white">   {item.price}</span>
                    {item.trend === 'rising' ?
                      <ArrowTrendingUpIcon className="w-4 h-4 text-accent-green" /> :
                      <ArrowTrendingDownIcon className="w-4 h-4 text-red-400" />
                    }
                  </div>
                )) : <div className="text-gray-600 italic">Syncing market ticker...</div>}
              </div>
            </div>

            {/* Loan Estimator Console */}
            <div ref={el => cardsRef.current[2] = el} className="glass-card border-accent-lime/20 bg-accent-lime/5">
              <div className="flex items-center gap-3 mb-8">
                <CalculatorIcon className="h-6 w-6 text-accent-lime" />
                <h2 className="text-xl font-bold text-white tracking-tight">Loan Simulation Console</h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-gray-500 uppercase ml-1">Principal Amount</label>
                  <div className="relative">
                    <input
                      type="number"
                      className="glass-input pl-10 border-white/10 focus:border-accent-lime/50"
                      value={loanParams.amount}
                      onChange={(e) => setLoanParams(prev => ({ ...prev, amount: parseFloat(e.target.value) || 0 }))}
                    />
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-accent-lime">   </span>
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-gray-500 uppercase ml-1">Tenure (Months)</label>
                  <input
                    type="number"
                    className="glass-input border-white/10"
                    value={loanParams.tenure}
                    onChange={(e) => setLoanParams(prev => ({ ...prev, tenure: parseInt(e.target.value) || 0 }))}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-gray-500 uppercase ml-1">Credit Type</label>
                  <select
                    className="glass-input border-white/10"
                    value={loanParams.loanType}
                    onChange={(e) => setLoanParams(prev => ({ ...prev, loanType: e.target.value }))}
                  >
                    <option className="bg-nature-900" value="crop_loan">CROP LOAN</option>
                    <option className="bg-nature-900" value="term_loan">TERM LOAN</option>
                    <option className="bg-nature-900" value="kisan_credit_card">KCC</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'Monthly Installment', val: `   ${emi.toLocaleString()}`, color: 'text-white' },
                  { label: 'Total Payback', val: `   ${totalAmount.toLocaleString()}`, color: 'text-gray-300' },
                  { label: 'Total Interest', val: `   ${totalInterest.toLocaleString()}`, color: 'text-red-400' },
                  { label: 'Interest Rate', val: `${loanCalculation?.data?.interest_rate_annual || 9}%`, color: 'text-accent-cyan' }
                ].map((stat, i) => (
                  <div key={i} className="p-5 rounded-[2rem] bg-black/40 border border-white/5 text-center">
                    <p className="text-[9px] font-bold text-gray-500 uppercase mb-2 tracking-tighter">{stat.label}</p>
                    <p className={`text-xl font-bold ${stat.color}`}>{stat.val}</p>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </div>

      {/* --- ELIGIBILITY MODAL --- */}
      {selectedScheme && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/80 backdrop-blur-md animate-fade-in" onClick={() => setSelectedScheme(null)}>
          <div className="glass-card max-w-2xl w-full border-accent-cyan/30 shadow-[0_0_50px_rgba(0,229,255,0.1)]" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-8">
              <div>
                <h2 className="text-3xl font-bold text-white tracking-tighter">{selectedScheme.scheme_name}</h2>
                <p className="text-accent-cyan font-bold text-xs uppercase tracking-widest mt-1">{selectedScheme.bank_name}</p>
              </div>
              <button onClick={() => setSelectedScheme(null)} className="p-3 rounded-full bg-white/5 hover:bg-white/10 text-gray-400 transition-all">   </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
              <div className="space-y-4">
                <div className="p-5 rounded-3xl bg-white/5 border border-white/5">
                  <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">Detailed Eligibility</p>
                  <p className="text-sm text-gray-300 leading-relaxed italic">"{selectedScheme.eligibility_criteria}"</p>
                </div>
              </div>
              <div className="space-y-4">
                <div className="p-5 rounded-3xl bg-accent-cyan/10 border border-accent-cyan/20">
                  <p className="text-[10px] text-accent-cyan font-bold uppercase mb-1">Required Documentation</p>
                  <ul className="text-xs text-gray-300 space-y-2">
                    {selectedScheme.documents_required?.map((doc, i) => <li key={i} className="flex gap-2"><span>   </span> {doc}</li>)}
                  </ul>
                </div>
              </div>
            </div>

            <button className="btn-primary w-full py-5 rounded-[2rem] text-lg font-black uppercase tracking-widest shadow-accent-green/20">
              Initialize Application Protocol
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Finance;
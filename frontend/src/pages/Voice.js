import React, { useState, useRef, useEffect } from 'react';
import { MicrophoneIcon, SpeakerWaveIcon, LanguageIcon, StopIcon, SparklesIcon, TrashIcon } from '@heroicons/react/24/outline';
import { useSpeechToText, useTextToSpeech, useDetectLanguage, useLanguages } from '../hooks/useAPI';
import toast from 'react-hot-toast';
import gsap from 'gsap';

const Voice = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en-IN');
  const [transcribedText, setTranscribedText] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  const audioRef = useRef(null);
  const waveRef = useRef(null);
  const cardsRef = useRef([]);

  // API hooks
  const speechToTextMutation = useSpeechToText();
  const textToSpeechMutation = useTextToSpeech();
  const detectLanguageMutation = useDetectLanguage();
  const { data: languagesData } = useLanguages();

  const languages = languagesData?.data?.languages || [
    { code: 'hi-IN', name: 'Hindi' }, { code: 'ta-IN', name: 'Tamil' },
    { code: 'te-IN', name: 'Telugu' }, { code: 'bn-IN', name: 'Bengali' },
    { code: 'en-IN', name: 'English' }
  ];

  // --- SONIC WAVE ANIMATION ---
  useEffect(() => {
    if (isRecording) {
      gsap.to(waveRef.current, {
        scaleY: 1.5,
        duration: 0.4,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
        stagger: 0.1
      });
    } else {
      gsap.to(waveRef.current, { scaleY: 1, duration: 0.5 });
    }
  }, [isRecording]);

  useEffect(() => {
    gsap.fromTo(cardsRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.8, stagger: 0.1, ease: "power3.out" }
    );
  }, []);

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];
      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        setIsProcessing(true);
        const response = await speechToTextMutation.mutateAsync({ audioFile: blob, language: selectedLanguage });
        setTranscribedText(response.data.text || response.data.transcription);
        setIsProcessing(false);
      };
      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
      toast.success('Listening to your fields...');
    } catch (error) { toast.error('Mic access denied.'); }
  };

  const handleStopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  return (
    <div className="page-container min-h-screen pb-20">
      <div className="page-overlay opacity-20" />

      <div className="content-wrapper relative z-10">
        <header className="mb-12 text-center lg:text-left">
          <h1 className="text-5xl lg:text-6xl font-bold tracking-tighter text-white">
            Voice <span className="text-gradient">Activation</span>
          </h1>
          <p className="text-gray-400 mt-2 font-light italic">Multilingual neural-link for accessible farming.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">

          {/* LEFT: The Sonic Core (Recording & Waveform) */}
          <div ref={el => cardsRef.current[0] = el} className="lg:col-span-5 flex flex-col gap-8">
            <div className="glass-card flex flex-col items-center justify-center py-16 relative overflow-hidden bg-accent-green/[0.02]">

              {/* Animated Waveform */}
              <div className="flex items-end gap-1 mb-10 h-16">
                {[...Array(8)].map((_, i) => (
                  <div key={i} ref={el => i === 0 ? waveRef.current = el : null}
                    className={`w-1.5 rounded-full ${isRecording ? 'bg-accent-green' : 'bg-gray-700'}`}
                    style={{ height: `${20 + Math.random() * 40}px` }}
                  />
                ))}
              </div>

              <button
                onClick={isRecording ? handleStopRecording : handleStartRecording}
                className={`w-32 h-32 rounded-full flex items-center justify-center transition-all duration-500 shadow-2xl
                  ${isRecording ? 'bg-red-500 shadow-red-500/40 scale-110' : 'bg-accent-green shadow-accent-green/40 hover:scale-105'}`}
              >
                {isRecording ? <StopIcon className="h-12 w-12 text-white" /> : <MicrophoneIcon className="h-12 w-12 text-nature-900" />}
              </button>

              <p className="mt-8 text-xs font-bold uppercase tracking-[0.3em] text-gray-500 animate-pulse">
                {isRecording ? 'Processing Frequency...' : 'Ready to Receive'}
              </p>

              {isProcessing && (
                <div className="absolute inset-0 bg-nature-900/60 backdrop-blur-sm flex items-center justify-center z-20">
                  <div className="w-10 h-10 border-2 border-accent-green border-t-transparent rounded-full animate-spin" />
                </div>
              )}
            </div>

            {/* Language Orbit */}
            <div className="glass-card">
              <h3 className="text-[10px] font-bold text-accent-cyan uppercase tracking-widest mb-4">Neural Translation</h3>
              <div className="grid grid-cols-2 gap-3">
                {languages.map((lang, i) => (
                  <button
                    key={lang.code}
                    onClick={() => setSelectedLanguage(lang.code)}
                    className={`px-4 py-3 rounded-2xl text-xs font-medium transition-all border
                      ${selectedLanguage === lang.code ? 'bg-accent-cyan/10 border-accent-cyan text-accent-cyan' : 'bg-white/5 border-white/5 text-gray-400 hover:bg-white/10'}`}
                  >
                    {lang.name}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* RIGHT: Transcriptions & AI Response */}
          <div ref={el => cardsRef.current[1] = el} className="lg:col-span-7 flex flex-col gap-6">

            {/* User Transcription Node */}
            <div className={`glass-card transition-all duration-500 ${transcribedText ? 'opacity-100' : 'opacity-30'}`}>
              <div className="flex items-center gap-2 mb-4 text-gray-500 uppercase font-bold text-[10px]">
                <LanguageIcon className="h-4 w-4" /> Captured Audio
              </div>
              <p className="text-xl text-white font-light italic leading-relaxed">
                {transcribedText || "Your spoken queries will appear here..."}
              </p>
            </div>

            {/* AI Response Node */}
            <div className={`glass-card border-accent-green/20 bg-accent-green/5 transition-all duration-500 ${aiResponse ? 'opacity-100 scale-100' : 'opacity-20 scale-95'}`}>
              <div className="flex items-center gap-2 mb-4 text-accent-green uppercase font-bold text-[10px]">
                <SparklesIcon className="h-4 w-4" /> Neural Response
              </div>
              <p className="text-lg text-gray-200 leading-relaxed mb-8">
                {aiResponse || "Awaiting frequency analysis..."}
              </p>

              <div className="flex gap-4">
                <button className="btn-primary flex-1 py-4 flex items-center justify-center gap-2">
                  <SpeakerWaveIcon className="h-5 w-5" /> Synthesis Audio
                </button>
                <button onClick={() => setAiResponse('')} className="btn-secondary p-4">
                  <TrashIcon className="h-5 w-5 text-gray-500" />
                </button>
              </div>
            </div>

            {/* Quick Commands Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {['                                                ?', 'Tell me about Weather', 'Crop for Maharashtra?'].map((cmd, i) => (
                <div key={i} className="animate-float glass-card py-4 px-6 flex items-center justify-between group cursor-pointer hover:border-accent-cyan/40" style={{ animationDelay: `${i * 0.2}s` }}>
                  <span className="text-xs text-gray-400 group-hover:text-white transition-colors">{cmd}</span>
                  <MicrophoneIcon className="h-4 w-4 text-gray-600 group-hover:text-accent-cyan" />
                </div>
              ))}
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default Voice;
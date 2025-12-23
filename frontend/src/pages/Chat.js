import React, { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon, MicrophoneIcon, PhotoIcon, SparklesIcon, BeakerIcon } from '@heroicons/react/24/outline';
import { useProcessQuery, useProcessVoiceQuery, useProcessImageQuery, useQueryHistory, useQueryTypes } from '../hooks/useAPI';
import toast from 'react-hot-toast';
import gsap from 'gsap';

// ✅ IMPORT MARKDOWN RENDERER
import ReactMarkdown from 'react-markdown';

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      text: "Hello! I'm AgriAI, your synchronized agricultural advisor. My sensors are calibrated. How can I assist your field today?",
      timestamp: new Date(),
      queryType: 'init'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // API hooks
  const processQueryMutation = useProcessQuery();
  const { data: queryHistory } = useQueryHistory(10, 0);

  // --- ANTIGRAVITY ANIMATION ---
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    const lastMsg = chatContainerRef.current?.lastElementChild;
    if (lastMsg) {
      gsap.fromTo(lastMsg, { opacity: 0, y: 20, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.4)" });
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMessage = { id: Date.now(), type: 'user', text: inputText, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputText;
    setInputText('');

    try {
      const response = await processQueryMutation.mutateAsync({ query_text: currentInput, language: 'en' });
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        text: response.data.response,
        timestamp: new Date(),
        queryType: response.data.query_type,
        confidence: response.data.confidence_score,
        recommendations: response.data.recommendations,
        dataSources: response.data.data_sources
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      toast.error("Telemetry error. Connection lost.");
    }
  };

  return (
    <div className="page-container h-[calc(100vh-6rem)]">
      <div className="page-overlay opacity-20" />

      <div className="content-wrapper h-full flex flex-col max-w-5xl mx-auto pb-6">

        {/* CHAT HUB HEADER */}
        <div className="flex items-center justify-between mb-6 px-4">
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tighter">AI <span className="text-gradient">Advisor Stream</span></h2>
            <div className="flex items-center gap-2 text-[10px] text-accent-cyan font-bold uppercase tracking-widest mt-1">
              <span className="w-1.5 h-1.5 rounded-full bg-accent-cyan animate-pulse" />
              Neural Link Encrypted
            </div>
          </div>
          <div className="flex gap-2">
            <div className="glass-card py-2 px-4 rounded-full text-[10px] text-gray-400 border-white/5 uppercase">History: {queryHistory?.queries?.length || 0} Nodes</div>
          </div>
        </div>

        {/* MESSAGES AREA */}
        <div ref={chatContainerRef} className="flex-1 overflow-y-auto px-4 space-y-6 no-scrollbar pb-10">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`relative max-w-[85%] lg:max-w-2xl px-6 py-4 rounded-[2rem] transition-all
                ${message.type === 'user'
                  ? 'bg-accent-green/10 border border-accent-green/20 text-white rounded-tr-none'
                  : 'bg-white/[0.03] backdrop-blur-xl border border-white/10 text-gray-100 rounded-tl-none'}`}>

                {message.type === 'ai' && (
                  <div className="flex items-center gap-2 mb-3">
                    <SparklesIcon className="h-4 w-4 text-accent-cyan" />
                    <span className="text-[10px] font-bold text-accent-cyan uppercase tracking-widest">AgriAI Insight</span>
                  </div>
                )}

                {/* ✅ REPLACED PLAIN TEXT WITH MARKDOWN RENDERER */}
                <div className="text-sm leading-relaxed mb-3 markdown-content">
                  <ReactMarkdown
                    components={{
                      // Custom styling for bold text to match your theme
                      strong: ({node, ...props}) => <span className="font-bold text-accent-cyan" {...props} />,
                      // Custom styling for lists
                      ul: ({node, ...props}) => <ul className="list-disc pl-5 my-2 space-y-1" {...props} />,
                      li: ({node, ...props}) => <li className="text-gray-200" {...props} />,
                      p: ({node, ...props}) => <p className="mb-2" {...props} />
                    }}
                  >
                    {message.text}
                  </ReactMarkdown>
                </div>

                {/* AI Metadata Tags */}
                {message.type === 'ai' && message.queryType !== 'init' && (
                  <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-white/5">
                    <span className="text-[9px] px-2 py-0.5 rounded-md bg-white/5 text-gray-500 uppercase">Type: {message.queryType}</span>
                    <span className="text-[9px] px-2 py-0.5 rounded-md bg-accent-cyan/10 text-accent-cyan uppercase font-bold">Confidence: {message.confidence}</span>
                    {message.dataSources?.map(src => (
                      <span key={src} className="text-[9px] px-2 py-0.5 rounded-md bg-white/5 text-gray-400">{src}</span>
                    ))}
                  </div>
                )}
                
                <span className="absolute -bottom-5 left-2 text-[9px] text-gray-600 uppercase tracking-widest">
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* INPUT AREA */}
        <div className="mt-auto px-4">
          <div className="glass-card p-2 rounded-[2.5rem] bg-white/[0.02] border-white/10 shadow-2xl">
            <form onSubmit={handleSubmit} className="flex items-center gap-2">
              <button type="button" className="p-3 text-gray-500 hover:text-accent-cyan transition-colors">
                <PhotoIcon className="h-6 w-6" />
              </button>
              <button type="button" className="p-3 text-gray-400 hover:text-accent-green transition-colors">
                <MicrophoneIcon className="h-6 w-6" />
              </button>

              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Ask the Advisor..."
                className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder-gray-600 text-sm py-3"
              />

              <button
                type="submit"
                disabled={!inputText.trim()}
                className="bg-accent-green text-nature-900 p-3 rounded-full hover:scale-110 active:scale-95 transition-all disabled:opacity-20 disabled:grayscale"
              >
                <PaperAirplaneIcon className="h-5 w-5 -rotate-45" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
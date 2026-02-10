
import React, { useState, useEffect } from 'react';
import { Lock, Unlock, ArrowRight, Sparkles } from 'lucide-react';

const AuthGate = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [passkey, setPasskey] = useState('');
    const [error, setError] = useState(false);
    const [shake, setShake] = useState(false);

    useEffect(() => {
        const sessionAuth = sessionStorage.getItem('curriculum_auth');
        if (sessionAuth === 'true') {
            setIsAuthenticated(true);
        }
    }, []);

    const handleLogin = (e) => {
        e.preventDefault();
        if (passkey === '1234') {
            setIsAuthenticated(true);
            sessionStorage.setItem('curriculum_auth', 'true');
            setError(false);
        } else {
            setError(true);
            setShake(true);
            setPasskey('');
            setTimeout(() => setShake(false), 600);
        }
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
        sessionStorage.removeItem('curriculum_auth');
    }

    if (isAuthenticated) {
        return (
            <>
                <div className="fixed top-4 right-4 z-[60]">
                    <button
                        onClick={handleLogout}
                        className="p-2.5 glass rounded-full text-gray-400 hover:text-red-400 transition-all duration-200 hover:scale-110 shadow-lg"
                        title="Lock App"
                    >
                        <Lock size={18} />
                    </button>
                </div>
                {children}
            </>
        );
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 px-4 relative overflow-hidden">
            {/* Animated background orbs */}
            <div className="absolute top-20 left-20 w-72 h-72 bg-indigo-500/20 rounded-full blur-3xl animate-float"></div>
            <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/15 rounded-full blur-3xl animate-float" style={{ animationDelay: '1.5s' }}></div>
            <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '3s' }}></div>

            <div className={`w-full max-w-lg animate-scale-in ${shake ? 'animate-[shake_0.5s_ease-in-out]' : ''}`}>
                <div className="glass rounded-3xl shadow-2xl overflow-hidden border border-white/10">
                    <div className="p-10 text-center">
                        {/* Icon */}
                        <div className="mx-auto w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mb-8 shadow-lg shadow-indigo-500/30 animate-float">
                            <Lock size={36} className="text-white" />
                        </div>

                        <h2 className="text-4xl font-extrabold text-white mb-3 tracking-tight">
                            Private Learning Station
                        </h2>
                        <p className="text-xl text-slate-400 mb-10">
                            Enter your passkey to unlock the curriculum
                        </p>

                        <form onSubmit={handleLogin} className="space-y-5">
                            <div>
                                <input
                                    type="password"
                                    value={passkey}
                                    onChange={(e) => { setPasskey(e.target.value); setError(false); }}
                                    placeholder="● ● ● ●"
                                    className={`w-full px-6 py-5 rounded-2xl border-2 text-xl tracking-[0.3em] text-center font-bold transition-all duration-300 bg-white/5 text-white placeholder-slate-500 focus:outline-none focus:ring-4 ${error
                                        ? 'border-red-400/60 focus:ring-red-400/20 bg-red-500/5'
                                        : 'border-white/10 focus:ring-indigo-400/30 focus:border-indigo-400/50'
                                        }`}
                                    autoFocus
                                />
                            </div>

                            <button
                                type="submit"
                                className="w-full py-5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xl font-bold rounded-2xl transition-all duration-300 transform active:scale-95 hover:shadow-lg hover:shadow-indigo-500/30 flex items-center justify-center gap-3"
                            >
                                <Sparkles size={22} />
                                Unlock Academy
                                <ArrowRight size={22} />
                            </button>
                        </form>

                        {error && (
                            <p className="mt-5 text-red-400 text-lg font-medium animate-fade-in">
                                ❌ Incorrect passkey. Try again.
                            </p>
                        )}
                    </div>
                    <div className="bg-white/5 p-4 text-center text-sm text-slate-500 border-t border-white/5">
                        Default Passkey: <span className="font-mono font-bold text-slate-400">1234</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AuthGate;

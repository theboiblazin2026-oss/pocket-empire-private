
import React, { useState, useEffect } from 'react';
import { Lock, ArrowRight, Fingerprint } from 'lucide-react';

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
                        className="p-2 rounded-full text-gray-400 hover:text-red-400 transition-all duration-200 hover:scale-110 hover:bg-red-400/10"
                        title="Lock App"
                    >
                        <Lock size={16} />
                    </button>
                </div>
                {children}
            </>
        );
    }

    return (
        <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden"
            style={{
                background: 'linear-gradient(135deg, #0f0c29 0%, #1a1145 30%, #24243e 60%, #0f0c29 100%)'
            }}>

            {/* Ambient glow orbs — soft and dreamy */}
            <div className="absolute top-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full blur-[120px] opacity-30"
                style={{ background: 'radial-gradient(circle, #7c3aed, transparent 70%)' }}></div>
            <div className="absolute bottom-[-15%] right-[-10%] w-[600px] h-[600px] rounded-full blur-[140px] opacity-25"
                style={{ background: 'radial-gradient(circle, #6366f1, transparent 70%)' }}></div>
            <div className="absolute top-[40%] left-[60%] w-[300px] h-[300px] rounded-full blur-[100px] opacity-15"
                style={{ background: 'radial-gradient(circle, #a78bfa, transparent 70%)' }}></div>

            {/* Floating particles */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                {[...Array(6)].map((_, i) => (
                    <div
                        key={i}
                        className="absolute w-1 h-1 bg-white/20 rounded-full animate-float"
                        style={{
                            left: `${15 + i * 15}%`,
                            top: `${20 + (i % 3) * 25}%`,
                            animationDelay: `${i * 0.7}s`,
                            animationDuration: `${4 + i * 0.5}s`
                        }}
                    />
                ))}
            </div>

            <div className={`w-full max-w-md animate-scale-in ${shake ? 'animate-[shake_0.5s_ease-in-out]' : ''}`}>
                {/* Main card */}
                <div className="text-center mb-10">
                    {/* Avatar/Logo */}
                    <div className="mx-auto w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center mb-6 shadow-lg shadow-violet-500/25 animate-float"
                        style={{ animationDuration: '5s' }}>
                        <Fingerprint size={28} className="text-white/90" />
                    </div>

                    <h2 className="text-3xl font-bold text-white tracking-tight mb-2">
                        Welcome back 👋
                    </h2>
                    <p className="text-base font-light text-white/40 leading-relaxed">
                        Your learning space is ready. Enter your code to jump in.
                    </p>
                </div>

                <form onSubmit={handleLogin} className="space-y-4">
                    <div className="relative">
                        <input
                            type="password"
                            value={passkey}
                            onChange={(e) => { setPasskey(e.target.value); setError(false); }}
                            placeholder="Enter passkey"
                            className={`w-full px-5 py-4 rounded-2xl text-base tracking-widest text-center font-medium transition-all duration-300 bg-white/[0.06] text-white placeholder-white/20 focus:outline-none focus:bg-white/[0.09] backdrop-blur-sm ${error
                                ? 'ring-2 ring-red-400/40 bg-red-500/5'
                                : 'ring-1 ring-white/[0.08] focus:ring-violet-400/30'
                                }`}
                            autoFocus
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full py-4 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white text-sm font-semibold rounded-2xl transition-all duration-300 active:scale-[0.98] hover:shadow-lg hover:shadow-violet-500/20 flex items-center justify-center gap-2"
                    >
                        Let's Go
                        <ArrowRight size={16} />
                    </button>
                </form>

                {error && (
                    <p className="mt-4 text-red-400/80 text-sm font-medium text-center animate-fade-in">
                        Hmm, that doesn't match. Try again!
                    </p>
                )}

                <p className="mt-8 text-center text-xs text-white/15 font-light">
                    Hint: <span className="font-mono text-white/25">1234</span>
                </p>
            </div>
        </div>
    );
};

export default AuthGate;

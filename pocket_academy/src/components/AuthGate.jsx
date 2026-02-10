
import React, { useState, useEffect } from 'react';
import { Lock, Unlock, ArrowRight } from 'lucide-react';

const AuthGate = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [passkey, setPasskey] = useState('');
    const [error, setError] = useState(false);

    // Check session storage on load
    useEffect(() => {
        const sessionAuth = sessionStorage.getItem('curriculum_auth');
        if (sessionAuth === 'true') {
            setIsAuthenticated(true);
        }
    }, []);

    const handleLogin = (e) => {
        e.preventDefault();
        // Simple client-side check. 
        // CHANGE THIS '1234' TO YOUR OWN SECRET CODE!
        if (passkey === '1234') {
            setIsAuthenticated(true);
            sessionStorage.setItem('curriculum_auth', 'true');
            setError(false);
        } else {
            setError(true);
            setPasskey('');
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
                        className="p-2 bg-white/20 hover:bg-white/40 backdrop-blur-md rounded-full text-gray-500 hover:text-red-500 transition shadow-sm"
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
        <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
            <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl overflow-hidden">
                <div className="p-8 text-center">
                    <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-6 text-blue-600">
                        <Lock size={32} />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">Private Learning Station</h2>
                    <p className="text-gray-500 mb-8">Enter your passkey to access your curriculum.</p>

                    <form onSubmit={handleLogin} className="space-y-4">
                        <div>
                            <input
                                type="password"
                                value={passkey}
                                onChange={(e) => { setPasskey(e.target.value); setError(false); }}
                                placeholder="Enter Passkey"
                                className={`w-full px-4 py-3 rounded-xl border ${error ? 'border-red-300 bg-red-50 focus:ring-red-200' : 'border-gray-200 focus:ring-blue-200 focus:border-blue-400'} focus:outline-none focus:ring-4 transition text-center text-lg tracking-widest`}
                                autoFocus
                            />
                        </div>

                        <button
                            type="submit"
                            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition transform active:scale-95 flex items-center justify-center gap-2"
                        >
                            Unlock <ArrowRight size={20} />
                        </button>
                    </form>

                    {error && (
                        <p className="mt-4 text-red-500 text-sm font-medium animate-pulse">
                            Incorrect passkey. Please try again.
                        </p>
                    )}
                </div>
                <div className="bg-gray-50 p-4 text-center text-xs text-gray-400 border-t border-gray-100">
                    Default Passkey: 1234
                </div>
            </div>
        </div>
    );
};

export default AuthGate;

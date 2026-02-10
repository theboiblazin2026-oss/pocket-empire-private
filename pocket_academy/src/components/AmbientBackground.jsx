import React from 'react';
import { useTheme } from '../context/ThemeContext';

const AmbientBackground = () => {
    const { darkMode } = useTheme();

    return (
        <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
            {/* Top Right Orb - Violet/Purple */}
            <div className={`absolute top-[-10%] right-[-5%] w-[600px] h-[600px] rounded-full blur-[120px] transition-opacity duration-700 ${darkMode ? 'opacity-20' : 'opacity-15'}`}
                style={{ background: 'radial-gradient(circle, #8b5cf6, transparent 70%)' }}></div>

            {/* Bottom Left Orb - Indigo/Blue */}
            <div className={`absolute bottom-[-10%] left-[-10%] w-[700px] h-[700px] rounded-full blur-[140px] transition-opacity duration-700 ${darkMode ? 'opacity-15' : 'opacity-10'}`}
                style={{ background: 'radial-gradient(circle, #6366f1, transparent 70%)' }}></div>

            {/* Center Floating Orb - Subtle */}
            <div className={`absolute top-[40%] left-[30%] w-[400px] h-[400px] rounded-full blur-[100px] transition-opacity duration-1000 animate-pulse ${darkMode ? 'opacity-10' : 'opacity-5'}`}
                style={{ background: 'radial-gradient(circle, #a78bfa, transparent 70%)', animationDuration: '8s' }}></div>
        </div>
    );
};

export default AmbientBackground;


import React from 'react';
import { useTheme } from '../context/ThemeContext';

const ProgressBar = ({ progress }) => {
    const { darkMode } = useTheme();

    return (
        <div className={`fixed top-0 left-0 w-full z-50 glass border-b px-4 py-3.5 shadow-sm ${darkMode ? 'border-white/10' : 'border-gray-200/80'}`}>
            <div className="max-w-3xl mx-auto flex items-center justify-between gap-4">
                <h1 className={`text-lg font-bold hidden sm:block ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                    Zero to Hero Curriculum
                </h1>
                <div className="flex-1 flex flex-col gap-1.5">
                    <div className={`flex justify-between text-xs font-bold uppercase tracking-wider ${darkMode ? 'text-slate-400' : 'text-gray-500'}`}>
                        <span>Progress</span>
                        <span className={progress >= 100 ? 'text-green-400' : ''}>
                            {Math.round(progress)}%
                        </span>
                    </div>
                    <div className={`w-full rounded-full h-3 overflow-hidden ${darkMode ? 'bg-slate-700' : 'bg-gray-200'}`}>
                        <div
                            className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 h-3 rounded-full transition-all duration-700 ease-out relative"
                            style={{ width: `${progress}%` }}
                        >
                            {progress > 5 && (
                                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProgressBar;

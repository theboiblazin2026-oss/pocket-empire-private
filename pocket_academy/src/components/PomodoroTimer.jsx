
import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Timer } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const PomodoroTimer = () => {
    const [timeLeft, setTimeLeft] = useState(25 * 60);
    const [isActive, setIsActive] = useState(false);
    const [isWorkMode, setIsWorkMode] = useState(true);
    const [isOpen, setIsOpen] = useState(false);
    const { darkMode } = useTheme();

    useEffect(() => {
        let interval = null;

        if (isActive && timeLeft > 0) {
            interval = setInterval(() => {
                setTimeLeft((time) => time - 1);
            }, 1000);
        } else if (timeLeft === 0) {
            clearInterval(interval);
            setIsActive(false);
            const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
            audio.play();

            if (isWorkMode) {
                setTimeLeft(5 * 60);
                setIsWorkMode(false);
            } else {
                setTimeLeft(25 * 60);
                setIsWorkMode(true);
            }
        }

        return () => clearInterval(interval);
    }, [isActive, timeLeft, isWorkMode]);

    const toggleTimer = () => setIsActive(!isActive);

    const resetTimer = () => {
        setIsActive(false);
        setTimeLeft(isWorkMode ? 25 * 60 : 5 * 60);
    };

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-4 right-4 z-50 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white p-4 rounded-2xl shadow-lg shadow-indigo-500/30 transition-all duration-300 hover:scale-110 flex items-center justify-center"
                title="Open Study Timer"
            >
                <Timer size={24} />
            </button>
        )
    }

    return (
        <div className={`fixed bottom-4 right-4 z-50 p-6 rounded-3xl shadow-2xl w-80 animate-scale-in border-2 ${darkMode
                ? 'bg-slate-800 border-slate-700 shadow-black/40'
                : 'bg-white border-gray-100 shadow-indigo-500/10'
            }`}>
            <div className="flex justify-between items-center mb-5">
                <h3 className={`font-extrabold text-lg flex items-center gap-2 ${darkMode ? 'text-white' : 'text-gray-700'}`}>
                    <Timer size={20} className="text-indigo-500" />
                    {isWorkMode ? 'Focus Time' : 'Break Time'}
                </h3>
                <button onClick={() => setIsOpen(false)} className={`text-lg transition-colors ${darkMode ? 'text-slate-500 hover:text-slate-300' : 'text-gray-400 hover:text-gray-600'}`}>✕</button>
            </div>

            <div className={`text-6xl font-mono font-black text-center mb-6 tracking-wider ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                {formatTime(timeLeft)}
            </div>

            <div className="flex justify-center gap-3">
                <button
                    onClick={toggleTimer}
                    className={`flex items-center gap-2 px-8 py-3 rounded-2xl font-bold text-white text-lg transition-all duration-200 ${isActive
                        ? 'bg-amber-500 hover:bg-amber-600 shadow-amber-500/30 shadow-lg'
                        : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 shadow-indigo-500/30 shadow-lg'
                        }`}
                >
                    {isActive ? <Pause size={20} /> : <Play size={20} />}
                    {isActive ? 'Pause' : 'Start'}
                </button>

                <button
                    onClick={resetTimer}
                    className={`p-3 rounded-2xl transition-all duration-200 ${darkMode ? 'text-slate-400 hover:text-white hover:bg-slate-700' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                        }`}
                    title="Reset"
                >
                    <RotateCcw size={22} />
                </button>
            </div>

            <div className="mt-5 flex justify-between text-sm font-bold">
                <button
                    onClick={() => { setIsWorkMode(true); setTimeLeft(25 * 60); setIsActive(false); }}
                    className={`px-4 py-2 rounded-xl transition-all ${isWorkMode
                        ? 'bg-indigo-500/20 text-indigo-400'
                        : darkMode ? 'text-slate-500 hover:text-indigo-400' : 'text-gray-400 hover:text-indigo-500'
                        }`}
                >
                    25m Work
                </button>
                <button
                    onClick={() => { setIsWorkMode(false); setTimeLeft(5 * 60); setIsActive(false); }}
                    className={`px-4 py-2 rounded-xl transition-all ${!isWorkMode
                        ? 'bg-indigo-500/20 text-indigo-400'
                        : darkMode ? 'text-slate-500 hover:text-indigo-400' : 'text-gray-400 hover:text-indigo-500'
                        }`}
                >
                    5m Break
                </button>
            </div>
        </div>
    );
};

export default PomodoroTimer;

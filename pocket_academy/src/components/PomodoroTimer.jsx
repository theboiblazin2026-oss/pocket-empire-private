
import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Timer } from 'lucide-react';

const PomodoroTimer = () => {
    const [timeLeft, setTimeLeft] = useState(25 * 60); // 25 minutes in seconds
    const [isActive, setIsActive] = useState(false);
    const [isWorkMode, setIsWorkMode] = useState(true); // true = work, false = break
    const [isOpen, setIsOpen] = useState(false); // Widget open/close state

    useEffect(() => {
        let interval = null;

        if (isActive && timeLeft > 0) {
            interval = setInterval(() => {
                setTimeLeft((time) => time - 1);
            }, 1000);
        } else if (timeLeft === 0) {
            // Time is up!
            clearInterval(interval);
            setIsActive(false);
            // Play a sound
            const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
            audio.play();

            // Auto-switch modes (optional, or just stop)
            if (isWorkMode) {
                setTimeLeft(5 * 60); // 5 min break
                setIsWorkMode(false);
            } else {
                setTimeLeft(25 * 60); // 25 min work
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
                className="fixed bottom-4 right-4 z-50 bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full shadow-lg transition-transform hover:scale-105 flex items-center justify-center"
                title="Open Study Timer"
            >
                <Timer size={24} />
            </button>
        )
    }

    return (
        <div className="fixed bottom-4 right-4 z-50 bg-white border border-gray-200 p-6 rounded-2xl shadow-xl w-72 animate-in slide-in-from-bottom-4 duration-300">
            <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold text-gray-700 flex items-center gap-2">
                    <Timer size={18} className="text-indigo-500" />
                    {isWorkMode ? 'Focus Time' : 'Break Time'}
                </h3>
                <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-gray-600">✕</button>
            </div>

            <div className="text-5xl font-mono font-bold text-center text-gray-800 mb-6 tracking-wider">
                {formatTime(timeLeft)}
            </div>

            <div className="flex justify-center gap-3">
                <button
                    onClick={toggleTimer}
                    className={`flex items-center gap-2 px-6 py-2 rounded-full font-medium text-white transition-colors ${isActive ? 'bg-amber-500 hover:bg-amber-600' : 'bg-indigo-600 hover:bg-indigo-700'
                        }`}
                >
                    {isActive ? <Pause size={18} /> : <Play size={18} />}
                    {isActive ? 'Pause' : 'Start'}
                </button>

                <button
                    onClick={resetTimer}
                    className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
                    title="Reset"
                >
                    <RotateCcw size={20} />
                </button>
            </div>

            <div className="mt-4 flex justify-between text-xs text-gray-400">
                <button onClick={() => { setIsWorkMode(true); setTimeLeft(25 * 60); setIsActive(false); }} className={`hover:text-indigo-500 ${isWorkMode ? 'text-indigo-600 font-bold' : ''}`}>25m Work</button>
                <button onClick={() => { setIsWorkMode(false); setTimeLeft(5 * 60); setIsActive(false); }} className={`hover:text-indigo-500 ${!isWorkMode ? 'text-indigo-600 font-bold' : ''}`}>5m Break</button>
            </div>
        </div>
    );
};

export default PomodoroTimer;

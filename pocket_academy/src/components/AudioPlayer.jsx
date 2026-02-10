
import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX, Play, RotateCcw } from 'lucide-react';

const AudioPlayer = ({ text, title }) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const [utterance, setUtterance] = useState(null);

    useEffect(() => {
        // Cleanup on unmount
        return () => {
            window.speechSynthesis.cancel();
        };
    }, []);

    const handlePlay = () => {
        window.speechSynthesis.cancel(); // effective reset

        const newUtterance = new SpeechSynthesisUtterance(`${title}. ${text}`);
        newUtterance.rate = 1.0;

        newUtterance.onend = () => {
            setIsPlaying(false);
            setIsPaused(false);
        };

        setUtterance(newUtterance);
        window.speechSynthesis.speak(newUtterance);
        setIsPlaying(true);
        setIsPaused(false);
    };

    const handleStop = () => {
        window.speechSynthesis.cancel();
        setIsPlaying(false);
        setIsPaused(false);
    };

    return (
        <div className="flex items-center gap-2 mt-4">
            {!isPlaying ? (
                <button
                    onClick={handlePlay}
                    className="flex items-center gap-2 px-3 py-1.5 bg-blue-100 text-blue-700 rounded-lg text-sm font-medium hover:bg-blue-200 transition"
                >
                    <Volume2 size={16} />
                    Listen to Lesson
                </button>
            ) : (
                <button
                    onClick={handleStop}
                    className="flex items-center gap-2 px-3 py-1.5 bg-red-100 text-red-700 rounded-lg text-sm font-medium hover:bg-red-200 transition"
                >
                    <VolumeX size={16} />
                    Stop Audio
                </button>
            )}
        </div>
    );
};

export default AudioPlayer;

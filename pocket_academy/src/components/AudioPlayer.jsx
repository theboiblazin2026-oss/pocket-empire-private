
import React, { useState, useEffect } from 'react';
import { Volume2, VolumeX } from 'lucide-react';

const AudioPlayer = ({ text, title }) => {
    const [isPlaying, setIsPlaying] = useState(false);

    useEffect(() => {
        return () => {
            window.speechSynthesis.cancel();
        };
    }, []);

    const handlePlay = () => {
        window.speechSynthesis.cancel();

        const newUtterance = new SpeechSynthesisUtterance(`${title}. ${text}`);
        newUtterance.rate = 1.0;

        newUtterance.onend = () => {
            setIsPlaying(false);
        };

        window.speechSynthesis.speak(newUtterance);
        setIsPlaying(true);
    };

    const handleStop = () => {
        window.speechSynthesis.cancel();
        setIsPlaying(false);
    };

    return (
        <div className="flex items-center gap-2">
            {!isPlaying ? (
                <button
                    onClick={(e) => { e.stopPropagation(); handlePlay(); }}
                    className="flex items-center gap-2 px-4 py-2 bg-white/20 text-white rounded-xl text-sm font-bold hover:bg-white/30 transition-all duration-200"
                >
                    <Volume2 size={16} />
                    Listen
                </button>
            ) : (
                <button
                    onClick={(e) => { e.stopPropagation(); handleStop(); }}
                    className="flex items-center gap-2 px-4 py-2 bg-red-500/80 text-white rounded-xl text-sm font-bold hover:bg-red-600 transition-all duration-200 animate-pulse"
                >
                    <VolumeX size={16} />
                    Stop
                </button>
            )}
        </div>
    );
};

export default AudioPlayer;


import React from 'react';

const ProgressBar = ({ progress }) => {
    return (
        <div className="fixed top-0 left-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-200 px-4 py-3 shadow-sm">
            <div className="max-w-3xl mx-auto flex items-center justify-between gap-4">
                <h1 className="text-lg font-bold text-gray-800 hidden sm:block">Zero to Hero Curriculum</h1>
                <div className="flex-1 flex flex-col gap-1">
                    <div className="flex justify-between text-xs font-semibold uppercase tracking-wider text-gray-500">
                        <span>Progress</span>
                        <span>{Math.round(progress)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                        <div
                            className="bg-gradient-to-r from-blue-500 to-purple-600 h-2.5 rounded-full transition-all duration-500 ease-out"
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProgressBar;

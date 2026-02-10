import React, { useRef } from 'react';
import { ReactSketchCanvas } from 'react-sketch-canvas';
import { Trash2, Undo, PenTool } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const ScratchPad = () => {
    const canvasRef = useRef(null);
    const { darkMode } = useTheme();

    const styles = {
        border: 'none',
        borderRadius: '0',
    };

    return (
        <div className={`w-full h-80 rounded-2xl overflow-hidden mt-4 transition-all duration-300 ${darkMode ? 'bg-slate-950 border-2 border-indigo-500/20 shadow-lg shadow-indigo-900/20' : 'bg-white border-2 border-indigo-100 shadow-md'
            }`}>
            <div className={`p-3 flex justify-between items-center border-b ${darkMode ? 'bg-slate-900 border-indigo-500/20' : 'bg-gray-50 border-indigo-100'
                }`}>
                <span className={`text-xs font-semibold tracking-wide flex items-center gap-2 ${darkMode ? 'text-slate-500' : 'text-gray-400'
                    }`}>
                    <PenTool size={12} /> Scratchpad · Apple Pencil Ready
                </span>
                <div className="flex gap-1.5">
                    <button
                        onClick={() => canvasRef.current.undo()}
                        className={`p-1.5 rounded-lg transition-colors ${darkMode ? 'text-slate-500 hover:text-indigo-400 hover:bg-indigo-900/30' : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'
                            }`}
                        title="Undo"
                    >
                        <Undo size={15} />
                    </button>
                    <button
                        onClick={() => canvasRef.current.clearCanvas()}
                        className={`p-1.5 rounded-lg transition-colors ${darkMode ? 'text-slate-500 hover:text-red-400 hover:bg-red-900/30' : 'text-gray-400 hover:text-red-500 hover:bg-red-50'
                            }`}
                        title="Clear"
                    >
                        <Trash2 size={15} />
                    </button>
                </div>
            </div>
            <ReactSketchCanvas
                ref={canvasRef}
                style={styles}
                strokeWidth={3}
                strokeColor={darkMode ? '#818cf8' : '#1e293b'}
                canvasColor={darkMode ? '#0a0f1e' : 'transparent'}
            />
        </div>
    );
};

export default ScratchPad;

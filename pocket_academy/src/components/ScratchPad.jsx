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
        <div className={`w-full h-80 rounded-2xl overflow-hidden border-2 shadow-sm mt-4 ${darkMode ? 'bg-slate-900 border-slate-700' : 'bg-white border-gray-200'
            }`}>
            <div className={`border-b p-3 flex justify-between items-center ${darkMode ? 'bg-slate-800 border-slate-700' : 'bg-gray-50 border-gray-200'
                }`}>
                <span className={`text-sm font-bold uppercase flex items-center gap-2 ${darkMode ? 'text-slate-400' : 'text-gray-500'}`}>
                    <PenTool size={14} /> Scratchpad (Apple Pencil Ready)
                </span>
                <div className="flex gap-2">
                    <button
                        onClick={() => canvasRef.current.undo()}
                        className={`p-2 rounded-xl transition-colors ${darkMode ? 'text-slate-400 hover:text-indigo-400 hover:bg-indigo-900/30' : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'}`}
                        title="Undo"
                    >
                        <Undo size={18} />
                    </button>
                    <button
                        onClick={() => canvasRef.current.clearCanvas()}
                        className={`p-2 rounded-xl transition-colors ${darkMode ? 'text-slate-400 hover:text-red-400 hover:bg-red-900/30' : 'text-gray-600 hover:text-red-600 hover:bg-red-50'}`}
                        title="Clear"
                    >
                        <Trash2 size={18} />
                    </button>
                </div>
            </div>
            <ReactSketchCanvas
                ref={canvasRef}
                style={styles}
                strokeWidth={3}
                strokeColor={darkMode ? '#818cf8' : 'black'}
                canvasColor={darkMode ? '#0f172a' : 'transparent'}
            />
        </div>
    );
};

export default ScratchPad;

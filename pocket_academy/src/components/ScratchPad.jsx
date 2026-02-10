import React, { useRef } from 'react';
import { ReactSketchCanvas } from 'react-sketch-canvas';
import { Trash2, Undo, PenTool } from 'lucide-react';

const ScratchPad = () => {
    const canvasRef = useRef(null);

    const styles = {
        border: '1px solid #e5e7eb',
        borderRadius: '0.5rem',
    };

    return (
        <div className="w-full h-80 bg-white rounded-lg overflow-hidden border border-gray-200 shadow-sm mt-4">
            <div className="bg-gray-50 border-b border-gray-200 p-2 flex justify-between items-center">
                <span className="text-xs font-bold text-gray-500 uppercase flex items-center gap-1">
                    <PenTool size={14} /> Scratchpad (Apple Pencil Ready)
                </span>
                <div className="flex gap-2">
                    <button
                        onClick={() => canvasRef.current.undo()}
                        className="p-1.5 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded"
                        title="Undo"
                    >
                        <Undo size={16} />
                    </button>
                    <button
                        onClick={() => canvasRef.current.clearCanvas()}
                        className="p-1.5 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded"
                        title="Clear"
                    >
                        <Trash2 size={16} />
                    </button>
                </div>
            </div>
            <ReactSketchCanvas
                ref={canvasRef}
                style={styles}
                strokeWidth={3}
                strokeColor="black"
                canvasColor="transparent"
            />
        </div>
    );
};

export default ScratchPad;

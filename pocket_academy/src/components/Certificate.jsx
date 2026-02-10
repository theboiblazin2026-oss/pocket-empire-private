
import React from 'react';
import { Award, Download, Share2 } from 'lucide-react';
import confetti from 'canvas-confetti';

const Certificate = ({ track, userName = "Future Mogul", onClose }) => {
    const isTrucking = track === 'trucking';
    const title = isTrucking ? "FLEET MOGUL CERTIFICATION" : "TECH MOGUL CERTIFICATION";
    const color = isTrucking ? "border-green-600 text-green-800" : "border-blue-600 text-blue-800";
    const bg = isTrucking ? "bg-green-50" : "bg-blue-50";
    const date = new Date().toLocaleDateString();

    const handleDownload = () => {
        window.print();
    }

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
            <div className={`relative w-full max-w-4xl ${bg} border-8 ${color} p-1 md:p-4 shadow-2xl rounded-lg`}>
                {/* Inner Border */}
                <div className={`border-4 border-dashed ${color} h-full p-8 md:p-16 text-center relative flex flex-col items-center justify-center`}>

                    {/* Badge */}
                    <div className="absolute top-4 right-8 opacity-20 md:opacity-100">
                        <Award size={100} strokeWidth={1} className={isTrucking ? "text-green-700" : "text-blue-700"} />
                    </div>

                    <h1 className={`text-4xl md:text-6xl font-black mb-4 tracking-widest ${isTrucking ? "text-green-900" : "text-blue-900"}`}>
                        CERTIFICATE
                    </h1>
                    <h2 className="text-xl md:text-2xl font-serif text-gray-600 mb-12">
                        OF MASTERY
                    </h2>

                    <p className="text-lg text-gray-500 mb-4">This hereby certifies that</p>

                    <div className="text-3xl md:text-5xl font-script font-bold text-gray-800 border-b-2 border-gray-400 pb-2 mb-8 px-12 min-w-[300px]">
                        {userName}
                    </div>

                    <p className="text-lg text-gray-500 mb-4">Has successfully completed the comprehensive curriculum for</p>

                    <h3 className={`text-2xl md:text-4xl font-bold mb-12 uppercase ${isTrucking ? "text-green-700" : "text-blue-700"}`}>
                        {isTrucking ? "Commercial Fleet Operations" : "Full Stack Web Engineering"}
                    </h3>

                    <div className="flex w-full justify-between items-end mt-8 px-12">
                        <div className="text-center">
                            <p className="font-bold text-gray-800 mb-2">{date}</p>
                            <div className="w-40 border-t border-gray-400 pt-2 text-xs text-gray-500 uppercase tracking-wider">Date</div>
                        </div>
                        <div className="hidden md:block">
                            <Award size={64} className="text-yellow-500" />
                        </div>
                        <div className="text-center">
                            <p className="font-script text-2xl text-gray-800 mb-1">The Interactive App</p>
                            <div className="w-40 border-t border-gray-400 pt-2 text-xs text-gray-500 uppercase tracking-wider">Instructor</div>
                        </div>
                    </div>

                </div>

                {/* Action Buttons (Hide when printing) */}
                <div className="absolute -bottom-16 left-0 right-0 flex justify-center gap-4 print:hidden">
                    <button onClick={handleDownload} className="flex items-center gap-2 px-6 py-3 bg-white text-gray-900 rounded-full font-bold shadow-lg hover:bg-gray-100 transition">
                        <Download size={20} /> Convert to PDF (Print)
                    </button>
                    <button onClick={() => onClose()} className="px-6 py-3 bg-gray-800 text-white rounded-full font-bold shadow-lg hover:bg-gray-700 transition">
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Certificate;

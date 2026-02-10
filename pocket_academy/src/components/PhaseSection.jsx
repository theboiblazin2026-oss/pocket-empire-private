import React, { useState } from 'react';
import TaskItem from './TaskItem';
import AudioPlayer from './AudioPlayer';
import QuizSection from './QuizSection';
import ScratchPad from './ScratchPad';
import { PenTool, ChevronDown, ChevronUp } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const PhaseSection = ({ phase, completedTasks, onToggleTask }) => {
    const [showScratchPad, setShowScratchPad] = useState(false);
    const [isExpanded, setIsExpanded] = useState(true);
    const { darkMode } = useTheme();

    const phaseTasks = phase.tasks;
    const completedCount = phaseTasks.filter(t => completedTasks.includes(t.id)).length;
    const isPhaseComplete = completedCount === phaseTasks.length && phaseTasks.length > 0;

    const audioText = `${phase.description} . Tasks include: ${phaseTasks.map(t => t.text).join('. ')}`;

    return (
        <div className={`rounded-3xl overflow-hidden border-2 transition-all duration-300 card-hover ${isPhaseComplete
                ? darkMode ? 'border-green-500/30 bg-green-900/10' : 'border-green-200 bg-green-50/30'
                : darkMode ? 'border-slate-700/80 bg-slate-800/50' : 'border-gray-100 bg-white shadow-sm'
            }`}>
            {/* Header */}
            <div
                className={`p-6 ${phase.color} text-white cursor-pointer`}
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="flex justify-between items-start">
                    <div className="flex-1">
                        <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight">{phase.title}</h2>
                        <p className="opacity-90 mt-2 text-lg leading-relaxed">{phase.description}</p>
                    </div>
                    <div className="flex items-center gap-3 ml-4">
                        <div className="bg-white/20 backdrop-blur-sm px-4 py-1.5 rounded-full text-base font-bold">
                            {completedCount} / {phaseTasks.length}
                        </div>
                        {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                    </div>
                </div>

                {isExpanded && (
                    <div className="flex flex-wrap gap-3 mt-5">
                        <AudioPlayer title={phase.title} text={audioText} />

                        <button
                            onClick={(e) => { e.stopPropagation(); setShowScratchPad(!showScratchPad); }}
                            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold transition-all duration-200 ${showScratchPad ? 'bg-white text-gray-900 shadow-lg' : 'bg-white/20 text-white hover:bg-white/30'}`}
                        >
                            <PenTool size={16} />
                            {showScratchPad ? 'Hide Scratchpad' : 'Open Scratchpad'}
                        </button>
                    </div>
                )}
            </div>

            {/* Content */}
            {isExpanded && (
                <div className="p-5 flex flex-col gap-3">
                    {/* Lingo Section */}
                    {phase.lingo && phase.lingo.length > 0 && (
                        <div className={`rounded-2xl p-5 mb-3 ${darkMode ? 'bg-indigo-900/20 border border-indigo-500/20' : 'bg-indigo-50/70 border border-indigo-100'}`}>
                            <h3 className={`text-lg font-bold mb-3 flex items-center gap-2 ${darkMode ? 'text-indigo-300' : 'text-indigo-800'}`}>
                                📖 Insider Lingo
                            </h3>
                            <div className="grid gap-2">
                                {phase.lingo.map((item, i) => (
                                    <div key={i} className={`rounded-xl p-3 ${darkMode ? 'bg-slate-800/50' : 'bg-white/70'}`}>
                                        <span className={`font-bold text-base ${darkMode ? 'text-indigo-300' : 'text-indigo-700'}`}>{item.term}:</span>
                                        <span className={`ml-2 text-base ${darkMode ? 'text-slate-300' : 'text-gray-600'}`}>{item.def}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {phaseTasks.map(task => (
                        <TaskItem
                            key={task.id}
                            task={task}
                            isCompleted={completedTasks.includes(task.id)}
                            onToggle={onToggleTask}
                        />
                    ))}

                    <button
                        onClick={() => setShowScratchPad(!showScratchPad)}
                        className={`flex items-center gap-2 text-base font-medium transition-colors mb-4 ${darkMode ? 'text-slate-400 hover:text-indigo-400' : 'text-gray-500 hover:text-indigo-600'
                            }`}
                    >
                        <PenTool size={16} />
                        {showScratchPad ? 'Hide Sketchpad' : (phase.sketchChallenge ? 'Start Drawing Challenge 🎨' : 'Open Sketchpad')}
                    </button>

                    {showScratchPad && (
                        <div className="my-4 animate-slide-up">
                            {phase.sketchChallenge && (
                                <div className={`p-4 rounded-t-2xl text-base font-bold border-b flex items-center gap-2 ${darkMode ? 'bg-indigo-900/30 text-indigo-300 border-indigo-500/20' : 'bg-indigo-50 text-indigo-800 border-indigo-100'
                                    }`}>
                                    <PenTool size={16} />
                                    Challenge: {phase.sketchChallenge}
                                </div>
                            )}
                            <ScratchPad />
                        </div>
                    )}

                    {phase.quiz && (
                        <QuizSection quiz={phase.quiz} />
                    )}
                </div>
            )}
        </div>
    );
};

export default PhaseSection;

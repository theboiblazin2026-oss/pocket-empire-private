import React, { useState } from 'react';
import { ChevronDown, Lock, Award, CheckCircle } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import TaskItem from './TaskItem';
import AudioPlayer from './AudioPlayer';
import ScratchPad from './ScratchPad';
import ExamSection from './ExamSection';

const PhaseSection = ({
    phase,
    completedTasks,
    onToggle,
    index,
    locked,
    examScore,
    onExamPass
}) => {
    const { darkMode } = useTheme();
    const [isOpen, setIsOpen] = useState(!locked && index === 0);
    const [showExam, setShowExam] = useState(false);

    const completedCount = phase.tasks.filter(t =>
        completedTasks.includes(t.id)
    ).length;
    const allTasksDone = completedCount === phase.tasks.length;
    const hasPassed = examScore !== undefined && examScore >= 80;

    // Gradient colors for phase headers
    const gradients = [
        'from-slate-600 to-slate-800',
        'from-blue-600 to-indigo-700',
        'from-rose-500 to-pink-700',
        'from-amber-500 to-orange-700',
        'from-cyan-500 to-blue-700',
        'from-emerald-500 to-green-700',
        'from-violet-500 to-indigo-700',
        'from-fuchsia-500 to-purple-700',
        'from-teal-500 to-cyan-700',
        'from-orange-500 to-red-700'
    ];

    return (
        <div
            className={`rounded-3xl overflow-hidden transition-all duration-300 ${locked
                    ? darkMode ? 'opacity-40' : 'opacity-50'
                    : ''
                }`}
            style={{ animationDelay: `${index * 0.1}s` }}
        >
            {/* Header */}
            <button
                onClick={() => !locked && setIsOpen(!isOpen)}
                disabled={locked}
                className={`w-full text-left p-6 bg-gradient-to-r ${gradients[index % gradients.length]} text-white rounded-3xl transition-all duration-200 ${locked ? 'cursor-not-allowed' : 'cursor-pointer hover:shadow-lg'
                    } ${isOpen ? 'rounded-b-none' : ''}`}
            >
                <div className="flex items-center justify-between">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                            {locked && <Lock size={20} className="text-white/60" />}
                            {hasPassed && <Award size={20} className="text-yellow-300" />}
                            <h3 className="text-2xl font-extrabold tracking-tight">
                                {phase.title}
                            </h3>
                        </div>
                        <p className="text-white/70 text-base">
                            {phase.description}
                        </p>
                    </div>
                    <div className="flex items-center gap-4 ml-4">
                        {hasPassed && (
                            <span className="bg-green-400/20 text-green-300 px-3 py-1 rounded-full text-sm font-bold">
                                {examScore}%
                            </span>
                        )}
                        <span className="bg-white/20 text-white/90 px-3 py-1 rounded-full text-sm font-bold">
                            {completedCount} / {phase.tasks.length}
                        </span>
                        {!locked && (
                            <ChevronDown
                                size={24}
                                className={`text-white/70 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''
                                    }`}
                            />
                        )}
                    </div>
                </div>
            </button>

            {/* Body */}
            {isOpen && !locked && (
                <div className={`p-6 space-y-6 rounded-b-3xl ${darkMode ? 'bg-slate-800/30' : 'bg-white/80'
                    }`}>
                    {/* Audio + Scratchpad toolbar */}
                    <div className="flex gap-2">
                        <AudioPlayer text={`${phase.title}. ${phase.description}`} />
                        <ScratchPad challenge={phase.sketchChallenge} />
                    </div>

                    {/* Insider Lingo */}
                    {phase.lingo && phase.lingo.length > 0 && (
                        <div>
                            <h4 className={`text-lg font-bold mb-3 flex items-center gap-2 ${darkMode ? 'text-indigo-400' : 'text-indigo-600'
                                }`}>
                                🗣️ Insider Lingo
                            </h4>
                            <div className="grid gap-2">
                                {phase.lingo.map((item, i) => (
                                    <div
                                        key={i}
                                        className={`p-4 rounded-2xl ${darkMode ? 'bg-indigo-900/15' : 'bg-indigo-50/50'
                                            }`}
                                    >
                                        <span className={`font-bold ${darkMode ? 'text-indigo-300' : 'text-indigo-700'
                                            }`}>{item.term}</span>
                                        <span className={`${darkMode ? 'text-slate-400' : 'text-gray-600'
                                            }`}> — {item.def}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Tasks */}
                    <div className="space-y-1">
                        {phase.tasks.map((task) => (
                            <TaskItem
                                key={task.id}
                                task={task}
                                isCompleted={completedTasks.includes(task.id)}
                                onToggle={() => onToggle(task.id)}
                                locked={false}
                            />
                        ))}
                    </div>

                    {/* Exam Section */}
                    {allTasksDone && !hasPassed && (
                        <div className="pt-4">
                            {!showExam ? (
                                <button
                                    onClick={() => setShowExam(true)}
                                    className="w-full py-5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-lg font-bold rounded-2xl transition-all duration-200 flex items-center justify-center gap-3 shadow-lg shadow-indigo-500/30 animate-fade-in"
                                >
                                    📝 Take Section Exam
                                    <span className="bg-white/20 px-3 py-0.5 rounded-full text-sm">
                                        Need 80% to pass
                                    </span>
                                </button>
                            ) : (
                                <ExamSection
                                    exam={phase.exam}
                                    phaseId={phase.id}
                                    onPass={onExamPass}
                                />
                            )}
                        </div>
                    )}

                    {hasPassed && (
                        <div className={`flex items-center gap-3 p-5 rounded-2xl ${darkMode ? 'bg-green-900/15' : 'bg-green-50'
                            }`}>
                            <CheckCircle size={24} className="text-green-500" />
                            <div>
                                <p className={`font-bold text-lg ${darkMode ? 'text-green-400' : 'text-green-700'}`}>
                                    Section Passed! Score: {examScore}%
                                </p>
                                <p className={`text-sm ${darkMode ? 'text-green-400/60' : 'text-green-600/60'}`}>
                                    Next section unlocked
                                </p>
                            </div>
                        </div>
                    )}

                    {!allTasksDone && (
                        <p className={`text-center text-sm py-3 ${darkMode ? 'text-slate-500' : 'text-gray-400'
                            }`}>
                            Complete all tasks above to unlock the section exam
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default PhaseSection;

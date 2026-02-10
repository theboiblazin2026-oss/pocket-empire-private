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
            className={`rounded-3xl overflow-hidden transition-all duration-300 ${locked ? 'opacity-35 saturate-50' : ''
                }`}
            style={{ animationDelay: `${index * 0.1}s` }}
        >
            {/* Header */}
            <button
                onClick={() => !locked && setIsOpen(!isOpen)}
                disabled={locked}
                className={`w-full text-left p-6 bg-gradient-to-r ${gradients[index % gradients.length]} text-white rounded-3xl transition-all duration-200 ${locked ? 'cursor-not-allowed' : 'cursor-pointer hover:shadow-lg hover:shadow-black/20'
                    } ${isOpen ? 'rounded-b-none' : ''}`}
            >
                <div className="flex items-center justify-between">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-1.5">
                            {locked && <Lock size={18} className="text-white/40" />}
                            {hasPassed && <Award size={18} className="text-yellow-300" />}
                            <h3 className="text-xl font-bold tracking-tight">
                                {phase.title}
                            </h3>
                        </div>
                        <p className="text-white/60 text-sm font-light leading-relaxed">
                            {phase.description}
                        </p>
                    </div>
                    <div className="flex items-center gap-3 ml-4">
                        {hasPassed && (
                            <span className="bg-green-400/20 text-green-300 px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide">
                                {examScore}%
                            </span>
                        )}
                        <span className="bg-white/15 text-white/80 px-2.5 py-0.5 rounded-full text-xs font-semibold tabular-nums">
                            {completedCount}/{phase.tasks.length}
                        </span>
                        {!locked && (
                            <ChevronDown
                                size={20}
                                className={`text-white/50 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''
                                    }`}
                            />
                        )}
                    </div>
                </div>
            </button>

            {/* Body */}
            {isOpen && !locked && (
                <div className={`p-6 space-y-6 rounded-b-3xl animate-reveal backdrop-blur-md border px-6 py-6 ${darkMode ? 'bg-slate-900/40 border-white/5 border-t-0' : 'bg-white/60 border-white/40 border-t-0'
                    }`}>
                    {/* Audio + Scratchpad toolbar */}
                    <div className="flex flex-col gap-4">
                        <div className="flex justify-start">
                            <AudioPlayer text={`${phase.title}. ${phase.description}`} />
                        </div>
                        <ScratchPad challenge={phase.sketchChallenge} />
                    </div>

                    {/* Insider Lingo */}
                    {phase.lingo && phase.lingo.length > 0 && (
                        <div>
                            <h4 className={`text-sm font-semibold uppercase tracking-widest mb-4 flex items-center gap-2 ${darkMode ? 'text-indigo-400/70' : 'text-indigo-500/80'
                                }`}>
                                <span className="w-5 h-px bg-current opacity-40"></span>
                                Insider Lingo
                            </h4>
                            <div className="grid gap-2.5 stagger-children">
                                {phase.lingo.map((item, i) => (
                                    <div
                                        key={i}
                                        className={`p-4 rounded-xl hover-lift transition-colors duration-200 ${darkMode ? 'bg-white/[0.03] hover:bg-white/[0.05]' : 'bg-slate-50 hover:bg-slate-100/60'
                                            }`}
                                    >
                                        <span className={`font-semibold text-sm ${darkMode ? 'text-indigo-300' : 'text-indigo-700'
                                            }`}>{item.term}</span>
                                        <span className={`text-sm font-light ml-1.5 ${darkMode ? 'text-slate-400' : 'text-slate-500'
                                            }`}>— {item.def}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Tasks */}
                    <div className="space-y-0.5 stagger-children">
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
                                    className="w-full py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-base font-semibold rounded-2xl transition-all duration-200 flex items-center justify-center gap-3 shadow-lg shadow-indigo-500/20 animate-fade-in"
                                >
                                    📝 Take Section Exam
                                    <span className="bg-white/15 px-2.5 py-0.5 rounded-full text-xs font-medium">
                                        80% to pass
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
                        <div className={`flex items-center gap-3 p-4 rounded-xl ${darkMode ? 'bg-green-900/10' : 'bg-green-50/80'
                            }`}>
                            <CheckCircle size={20} className="text-green-500" />
                            <div>
                                <p className={`font-semibold text-sm ${darkMode ? 'text-green-400' : 'text-green-700'}`}>
                                    Section passed · {examScore}%
                                </p>
                                <p className={`text-xs font-light ${darkMode ? 'text-green-400/50' : 'text-green-600/50'}`}>
                                    Next section unlocked
                                </p>
                            </div>
                        </div>
                    )}

                    {!allTasksDone && (
                        <p className={`text-center text-xs font-light tracking-wide py-3 ${darkMode ? 'text-slate-600' : 'text-gray-300'
                            }`}>
                            Complete all tasks to unlock the section exam
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default PhaseSection;

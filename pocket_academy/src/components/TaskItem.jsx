import React from 'react';
import { ExternalLink } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const TaskItem = ({ task, isCompleted, onToggle, locked }) => {
    const { darkMode } = useTheme();

    return (
        <div
            className={`group flex items-start gap-4 py-4 px-4 rounded-xl transition-all duration-200 ${locked
                    ? 'opacity-40 pointer-events-none'
                    : isCompleted
                        ? darkMode ? 'bg-green-900/5' : 'bg-green-50/30'
                        : darkMode ? 'hover:bg-white/[0.03]' : 'hover:bg-slate-50/60'
                }`}
        >
            {/* Custom Checkbox */}
            <button
                onClick={onToggle}
                disabled={locked}
                className={`mt-0.5 shrink-0 w-6 h-6 rounded-lg flex items-center justify-center transition-all duration-300 ${isCompleted
                        ? 'bg-gradient-to-br from-green-400 to-emerald-500 text-white shadow-sm shadow-green-500/25 scale-105'
                        : darkMode
                            ? 'bg-white/[0.06] group-hover:bg-white/10'
                            : 'bg-slate-100 group-hover:bg-slate-200/80'
                    }`}
            >
                {isCompleted && (
                    <svg className="w-3.5 h-3.5 animate-scale-in" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                )}
            </button>

            {/* Text */}
            <div className="flex-1 min-w-0">
                <p className={`text-[15px] leading-relaxed transition-all duration-200 ${isCompleted
                        ? darkMode ? 'text-green-400/50 line-through decoration-green-400/20' : 'text-green-700/50 line-through decoration-green-700/20'
                        : darkMode ? 'text-slate-300 font-light' : 'text-slate-600'
                    }`}>
                    {task.text}
                </p>
                {task.link && (
                    <a
                        href={task.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`inline-flex items-center gap-1 mt-1.5 text-xs font-medium tracking-wide transition-colors ${darkMode
                                ? 'text-indigo-400/70 hover:text-indigo-300'
                                : 'text-indigo-500 hover:text-indigo-700'
                            }`}
                        onClick={(e) => e.stopPropagation()}
                    >
                        Open Resource <ExternalLink size={11} />
                    </a>
                )}
            </div>
        </div>
    );
};

export default TaskItem;

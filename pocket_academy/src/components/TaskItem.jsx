import React from 'react';
import { ExternalLink, ChevronDown } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const TaskItem = ({ task, isCompleted, onToggle, locked }) => {
    const { darkMode } = useTheme();
    const [isOpen, setIsOpen] = React.useState(false);
    const hasDetails = task.detail || task.tool;

    return (
        <div
            onClick={() => hasDetails && setIsOpen(!isOpen)}
            className={`group flex flex-col py-4 px-4 rounded-xl transition-all duration-200 border border-transparent ${locked
                ? 'opacity-40 pointer-events-none'
                : isCompleted
                    ? darkMode ? 'bg-green-900/10 border-green-900/20' : 'bg-green-50/50 border-green-100'
                    : darkMode
                        ? `hover:bg-white/[0.03] ${isOpen ? 'bg-white/[0.03] border-white/5' : ''}`
                        : `hover:bg-slate-50/60 ${isOpen ? 'bg-slate-50/60 border-gray-200/50' : ''}`
                } ${hasDetails ? 'cursor-pointer' : ''}`}
        >
            <div className="flex items-start gap-4">
                {/* Custom Checkbox */}
                <button
                    onClick={(e) => {
                        e.stopPropagation();
                        onToggle();
                    }}
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

                {/* Header Text */}
                <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                        <p className={`text-[15px] font-medium leading-relaxed transition-all duration-200 ${isCompleted
                            ? darkMode ? 'text-green-400/50 line-through decoration-green-400/20' : 'text-green-700/50 line-through decoration-green-700/20'
                            : darkMode ? 'text-slate-200' : 'text-slate-700'
                            }`}>
                            {task.text}
                        </p>
                        {hasDetails && (
                            <div className={`transition-transform duration-300 ${isOpen ? 'rotate-180' : ''} ${darkMode ? 'text-slate-500' : 'text-slate-400'}`}>
                                <ChevronDown size={18} />
                            </div>
                        )}
                    </div>

                    {/* Meta info (like links) in the header if not expanded */}
                    {!isOpen && task.link && (
                        <div className={`mt-1 text-xs ${darkMode ? 'text-indigo-400/60' : 'text-indigo-500/60'}`}>
                            Contains Link ↗
                        </div>
                    )}
                </div>
            </div>

            {/* Expandable Details */}
            {hasDetails && isOpen && (
                <div className="pl-10 mt-4 animate-fade-in space-y-4">
                    {/* Tool Badge */}
                    {task.tool && (
                        <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold tracking-wide uppercase ${darkMode
                            ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/20'
                            : 'bg-indigo-50 text-indigo-600 border border-indigo-100'
                            }`}>
                            Using: {task.tool}
                        </span>
                    )}

                    {/* Detailed Instructions */}
                    {task.detail && (
                        <div className={`text-sm leading-7 whitespace-pre-line ${darkMode ? 'text-slate-400' : 'text-slate-600'}`}>
                            {task.detail}
                        </div>
                    )}

                    {/* Bottom Link */}
                    {task.link && (
                        <a
                            href={task.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`inline-flex items-center gap-1.5 text-sm font-medium transition-colors ${darkMode
                                ? 'text-indigo-400 hover:text-indigo-300'
                                : 'text-indigo-600 hover:text-indigo-700'
                                }`}
                            onClick={(e) => e.stopPropagation()}
                        >
                            Open Resource <ExternalLink size={14} />
                        </a>
                    )}
                </div>
            )}
        </div>
    );
};

export default TaskItem;

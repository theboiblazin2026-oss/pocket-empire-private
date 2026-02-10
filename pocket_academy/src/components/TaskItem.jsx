import React from 'react';
import { ExternalLink } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const TaskItem = ({ task, isCompleted, onToggle, locked }) => {
    const { darkMode } = useTheme();

    return (
        <div
            className={`group flex items-start gap-4 p-5 rounded-2xl transition-all duration-200 ${locked
                    ? 'opacity-40 pointer-events-none'
                    : isCompleted
                        ? darkMode ? 'bg-green-900/10' : 'bg-green-50/50'
                        : darkMode ? 'hover:bg-white/5' : 'hover:bg-gray-50'
                }`}
        >
            {/* Custom Checkbox */}
            <button
                onClick={onToggle}
                disabled={locked}
                className={`mt-0.5 shrink-0 w-7 h-7 rounded-lg flex items-center justify-center transition-all duration-300 ${isCompleted
                        ? 'bg-gradient-to-br from-green-400 to-emerald-500 text-white shadow-md shadow-green-500/30 scale-110'
                        : darkMode
                            ? 'bg-slate-700/50 group-hover:bg-slate-600/50'
                            : 'bg-gray-200/70 group-hover:bg-gray-300/70'
                    }`}
            >
                {isCompleted && (
                    <svg className="w-4 h-4 animate-scale-in" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                )}
            </button>

            {/* Text */}
            <div className="flex-1 min-w-0">
                <p className={`text-base leading-relaxed font-medium transition-all duration-200 ${isCompleted
                        ? darkMode ? 'text-green-400/70 line-through' : 'text-green-700/70 line-through'
                        : darkMode ? 'text-slate-200' : 'text-gray-700'
                    }`}>
                    {task.text}
                </p>
                {task.link && (
                    <a
                        href={task.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className={`inline-flex items-center gap-1.5 mt-2 text-sm font-semibold transition-colors ${darkMode
                                ? 'text-indigo-400 hover:text-indigo-300'
                                : 'text-indigo-600 hover:text-indigo-700'
                            }`}
                        onClick={(e) => e.stopPropagation()}
                    >
                        Open Resource <ExternalLink size={14} />
                    </a>
                )}
            </div>
        </div>
    );
};

export default TaskItem;

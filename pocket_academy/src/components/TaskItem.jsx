import React from 'react';
import { CheckCircle2, Circle, ExternalLink } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const TaskItem = ({ task, isCompleted, onToggle }) => {
    const { darkMode } = useTheme();

    return (
        <div
            onClick={() => onToggle(task.id)}
            className={`
                group flex items-start gap-4 p-4 rounded-2xl cursor-pointer transition-all duration-200 border-2
                ${isCompleted
                    ? darkMode
                        ? 'bg-green-900/20 border-green-500/20'
                        : 'bg-green-50/50 border-green-100'
                    : darkMode
                        ? 'bg-slate-800/30 border-slate-700/50 hover:border-indigo-500/40 hover:bg-slate-800/60'
                        : 'bg-white border-gray-100 hover:border-blue-200 hover:shadow-md'
                }
            `}
        >
            <div className={`mt-0.5 transition-all duration-200 ${isCompleted ? 'text-green-500 scale-110' : darkMode ? 'text-slate-600 group-hover:text-indigo-400' : 'text-gray-300 group-hover:text-blue-400'}`}>
                {isCompleted ? <CheckCircle2 size={24} fill="currentColor" className="text-white" /> : <Circle size={24} />}
            </div>

            <div className="flex-1">
                <p className={`text-base md:text-lg leading-relaxed transition-all duration-200 ${isCompleted
                        ? darkMode ? 'text-slate-500 line-through' : 'text-gray-400 line-through'
                        : darkMode ? 'text-slate-200' : 'text-gray-700'
                    }`}>
                    {task.text}
                </p>

                {task.link && (
                    <a
                        href={task.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="inline-flex items-center gap-1.5 text-sm text-indigo-500 hover:text-indigo-400 mt-2 font-bold transition-colors"
                    >
                        Open Resource <ExternalLink size={14} />
                    </a>
                )}
            </div>
        </div>
    );
};

export default TaskItem;

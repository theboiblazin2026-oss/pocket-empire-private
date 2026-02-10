import React from 'react';
import { CheckCircle2, Circle, ExternalLink } from 'lucide-react';

const TaskItem = ({ task, isCompleted, onToggle }) => {
    return (
        <div
            onClick={() => onToggle(task.id)}
            className={`
        group flex items-start gap-3 p-3 rounded-lg cursor-pointer transition-all duration-200 border
        ${isCompleted
                    ? 'bg-green-50/50 border-green-100'
                    : 'bg-white border-gray-100 hover:border-blue-200 hover:shadow-md'
                }
      `}
        >
            <div className={`mt-0.5 transition-colors duration-200 ${isCompleted ? 'text-green-500' : 'text-gray-300 group-hover:text-blue-400'}`}>
                {isCompleted ? <CheckCircle2 size={20} fill="currentColor" className="text-white" /> : <Circle size={20} />}
            </div>

            <div className="flex-1">
                <p className={`text-sm sm:text-base transition-all duration-200 ${isCompleted ? 'text-gray-400 line-through' : 'text-gray-700'}`}>
                    {task.text}
                </p>

                {task.link && (
                    <a
                        href={task.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="inline-flex items-center gap-1 text-xs text-blue-500 hover:text-blue-700 mt-1 font-medium"
                    >
                        Resource <ExternalLink size={12} />
                    </a>
                )}
            </div>
        </div>
    );
};

export default TaskItem;

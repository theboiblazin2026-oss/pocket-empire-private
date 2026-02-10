import React, { useState } from 'react';
import TaskItem from './TaskItem';
import AudioPlayer from './AudioPlayer';
import QuizSection from './QuizSection';
import ScratchPad from './ScratchPad';
import { PenTool } from 'lucide-react';

const PhaseSection = ({ phase, completedTasks, onToggleTask }) => {
    const [showScratchPad, setShowScratchPad] = useState(false);

    const phaseTasks = phase.tasks;
    const completedCount = phaseTasks.filter(t => completedTasks.includes(t.id)).length;
    const isPhaseComplete = completedCount === phaseTasks.length && phaseTasks.length > 0;

    // Generate text for audio reader
    const audioText = `${phase.description} . Tasks include: ${phaseTasks.map(t => t.text).join('. ')}`;

    return (
        <div className={`mb-8 rounded-2xl overflow-hidden border transition-all duration-300 ${isPhaseComplete ? 'border-green-200 bg-green-50/30' : 'border-gray-200 bg-white shadow-sm'}`}>
            <div className={`p-6 ${phase.color} text-white`}>
                <div className="flex justify-between items-start">
                    <div>
                        <h2 className="text-2xl font-bold">{phase.title}</h2>
                        <p className="opacity-90 mt-1">{phase.description}</p>
                    </div>
                    <div className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium">
                        {completedCount} / {phaseTasks.length}
                    </div>
                </div>

                <div className="flex flex-wrap gap-3 mt-4">
                    <AudioPlayer title={phase.title} text={audioText} />

                    <button
                        onClick={() => setShowScratchPad(!showScratchPad)}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition ${showScratchPad ? 'bg-white text-gray-900' : 'bg-white/20 text-white hover:bg-white/30'}`}
                    >
                        <PenTool size={16} />
                        {showScratchPad ? 'Hide Scratchpad' : 'Open Scratchpad'}
                    </button>
                </div>
            </div>

            <div className="p-4 flex flex-col gap-2">
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
                    className="flex items-center gap-2 text-sm text-gray-500 hover:text-indigo-600 transition-colors mb-4"
                >
                    <PenTool size={16} />
                    {showScratchPad ? 'Hide Sketchpad' : (phase.sketchChallenge ? 'Start Drawing Challenge 🎨' : 'Open Sketchpad')}
                </button>

                {showScratchPad && (
                    <div className="my-4 animate-in fade-in slide-in-from-top-4 duration-300">
                        {phase.sketchChallenge && (
                            <div className="bg-indigo-50 text-indigo-800 p-3 rounded-t-lg text-sm font-medium border-b border-indigo-100 flex items-center gap-2">
                                <PenTool size={14} />
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
        </div>
    );
};

export default PhaseSection;

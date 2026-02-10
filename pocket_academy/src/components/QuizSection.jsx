
import React, { useState } from 'react';
import confetti from 'canvas-confetti';
import { CheckCircle, XCircle, HelpCircle, Sparkles } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const QuizSection = ({ quiz }) => {
    const [selectedOption, setSelectedOption] = useState(null);
    const [isCorrect, setIsCorrect] = useState(null);
    const { darkMode } = useTheme();

    const handleSelect = (index) => {
        setSelectedOption(index);
        const correct = index === quiz.correctAnswer;
        setIsCorrect(correct);

        if (correct) {
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });
        }
    };

    if (!quiz) return null;

    return (
        <div className={`mt-8 rounded-2xl p-6 border-2 ${darkMode
                ? 'bg-indigo-900/20 border-indigo-500/20'
                : 'bg-indigo-50/50 border-indigo-100'
            }`}>
            <div className="flex items-start gap-3 mb-5">
                <div className={`p-2.5 rounded-xl ${darkMode ? 'bg-indigo-500/20 text-indigo-400' : 'bg-indigo-100 text-indigo-600'}`}>
                    <HelpCircle size={26} />
                </div>
                <div>
                    <h3 className={`text-xl font-extrabold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                        Knowledge Check
                    </h3>
                    <p className={`text-lg font-medium mt-1 ${darkMode ? 'text-slate-300' : 'text-gray-600'}`}>
                        {quiz.question}
                    </p>
                </div>
            </div>

            <div className="grid gap-3">
                {quiz.options.map((option, index) => {
                    let buttonClass = `w-full text-left p-5 rounded-2xl border-2 transition-all duration-200 text-lg font-medium `;

                    if (selectedOption === null) {
                        buttonClass += darkMode
                            ? 'bg-slate-800/50 border-slate-600/50 hover:border-indigo-500/50 hover:bg-indigo-900/20 text-slate-200'
                            : 'bg-white border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 text-gray-700';
                    } else if (index === quiz.correctAnswer) {
                        buttonClass += darkMode
                            ? 'bg-green-900/30 border-green-500/40 text-green-300'
                            : 'bg-green-100 border-green-300 text-green-800';
                    } else if (selectedOption === index && !isCorrect) {
                        buttonClass += darkMode
                            ? 'bg-red-900/30 border-red-500/40 text-red-300'
                            : 'bg-red-100 border-red-300 text-red-800';
                    } else {
                        buttonClass += darkMode
                            ? 'bg-slate-800/30 border-slate-700/30 text-slate-600 opacity-50'
                            : 'bg-white border-gray-100 text-gray-400 opacity-50';
                    }

                    return (
                        <button
                            key={index}
                            disabled={selectedOption !== null}
                            onClick={() => handleSelect(index)}
                            className={buttonClass}
                        >
                            <div className="flex items-center justify-between">
                                <span>{option}</span>
                                {selectedOption === index && (
                                    <span className="animate-scale-in">
                                        {index === quiz.correctAnswer ? <CheckCircle size={24} /> : <XCircle size={24} />}
                                    </span>
                                )}
                            </div>
                        </button>
                    );
                })}
            </div>

            {isCorrect === true && (
                <div className={`mt-5 p-4 rounded-2xl text-lg text-center font-bold flex items-center justify-center gap-2 animate-slide-up ${darkMode ? 'bg-green-900/30 text-green-300' : 'bg-green-100 text-green-700'
                    }`}>
                    <Sparkles size={20} /> Correct! Great Job! 🎉
                </div>
            )}
            {isCorrect === false && (
                <div className={`mt-5 p-4 rounded-2xl text-lg text-center font-bold animate-fade-in ${darkMode ? 'bg-red-900/30 text-red-300' : 'bg-red-100 text-red-700'
                    }`}>
                    ❌ Not quite. Try refreshing to guess again!
                </div>
            )}
        </div>
    );
};

export default QuizSection;

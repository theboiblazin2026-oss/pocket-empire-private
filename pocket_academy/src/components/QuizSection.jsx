
import React, { useState } from 'react';
import confetti from 'canvas-confetti';
import { CheckCircle, XCircle, HelpCircle } from 'lucide-react';

const QuizSection = ({ quiz }) => {
    const [selectedOption, setSelectedOption] = useState(null);
    const [isCorrect, setIsCorrect] = useState(null);

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
        <div className="mt-8 bg-indigo-50/50 border border-indigo-100 rounded-xl p-6">
            <div className="flex items-start gap-3 mb-4">
                <div className="p-2 bg-indigo-100 text-indigo-600 rounded-lg">
                    <HelpCircle size={24} />
                </div>
                <div>
                    <h3 className="text-lg font-bold text-gray-800">Knowledge Check</h3>
                    <p className="text-gray-600 font-medium">{quiz.question}</p>
                </div>
            </div>

            <div className="grid gap-2">
                {quiz.options.map((option, index) => {
                    let buttonClass = "w-full text-left p-4 rounded-lg border transition-all duration-200 font-medium ";

                    if (selectedOption === null) {
                        buttonClass += "bg-white border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 text-gray-700";
                    } else if (index === quiz.correctAnswer) {
                        // Creating a 'revealed correct' state even if they clicked wrong is good for learning
                        // But for now let's just show status of clicked
                        buttonClass += "bg-green-100 border-green-300 text-green-800";
                    } else if (selectedOption === index && !isCorrect) {
                        buttonClass += "bg-red-100 border-red-300 text-red-800";
                    } else {
                        buttonClass += "bg-white border-gray-100 text-gray-400 opacity-50";
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
                                    <span>
                                        {index === quiz.correctAnswer ? <CheckCircle size={20} /> : <XCircle size={20} />}
                                    </span>
                                )}
                            </div>
                        </button>
                    );
                })}
            </div>

            {isCorrect === true && (
                <div className="mt-4 p-3 bg-green-100 text-green-700 rounded-lg text-sm text-center font-bold animate-bounce">
                    Correct! Great Job! 🎉
                </div>
            )}
            {isCorrect === false && (
                <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm text-center font-bold">
                    Not quite. Try refreshing to guess again!
                </div>
            )}
        </div>
    );
};

export default QuizSection;

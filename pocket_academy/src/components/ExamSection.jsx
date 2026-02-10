import React, { useState } from 'react';
import { CheckCircle, XCircle, Award, RotateCcw, Lock, ChevronRight } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import confetti from 'canvas-confetti';

const PASS_THRESHOLD = 80;

const ExamSection = ({ exam, phaseId, onPass }) => {
    const { darkMode } = useTheme();

    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [answers, setAnswers] = useState({});
    const [showResults, setShowResults] = useState(false);
    const [selectedOption, setSelectedOption] = useState(null);
    const [showFeedback, setShowFeedback] = useState(false);

    if (!exam || exam.length === 0) return null;

    const totalQuestions = exam.length;
    const currentQ = exam[currentQuestion];
    const correctCount = Object.keys(answers).filter(
        (idx) => answers[idx] === exam[idx].correctAnswer
    ).length;
    const score = Math.round((correctCount / totalQuestions) * 100);
    const passed = score >= PASS_THRESHOLD;

    const handleSelect = (optionIdx) => {
        if (showFeedback) return;
        setSelectedOption(optionIdx);
        setShowFeedback(true);

        const isCorrect = optionIdx === currentQ.correctAnswer;
        setAnswers(prev => ({ ...prev, [currentQuestion]: optionIdx }));

        if (isCorrect) {
            confetti({ particleCount: 40, spread: 50, origin: { y: 0.7 } });
        }
    };

    const handleNext = () => {
        if (currentQuestion < totalQuestions - 1) {
            setCurrentQuestion(prev => prev + 1);
            setSelectedOption(null);
            setShowFeedback(false);
        } else {
            setShowResults(true);
            const finalScore = Math.round(
                (Object.keys({ ...answers }).filter(
                    (idx) => ({ ...answers })[idx] === exam[idx].correctAnswer
                ).length / totalQuestions) * 100
            );
            if (finalScore >= PASS_THRESHOLD) {
                confetti({ particleCount: 200, spread: 120, origin: { y: 0.5 } });
                onPass(phaseId, finalScore);
            }
        }
    };

    const handleRetake = () => {
        setCurrentQuestion(0);
        setAnswers({});
        setShowResults(false);
        setSelectedOption(null);
        setShowFeedback(false);
    };

    // RESULTS SCREEN
    if (showResults) {
        return (
            <div className={`mt-8 rounded-3xl p-8 text-center animate-scale-in ${darkMode ? 'bg-slate-800/40' : 'bg-white shadow-lg'
                }`}>
                <div className={`mx-auto w-20 h-20 rounded-full flex items-center justify-center mb-6 ${passed
                    ? 'bg-gradient-to-br from-green-400 to-emerald-600 text-white'
                    : 'bg-gradient-to-br from-red-400 to-rose-600 text-white'
                    }`}>
                    {passed ? <Award size={40} /> : <XCircle size={40} />}
                </div>

                <h3 className={`text-2xl font-bold tracking-tight mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    {passed ? '🎉 You Passed!' : '📚 Keep Studying!'}
                </h3>

                <div className={`text-5xl font-bold tracking-tight my-6 tabular-nums ${passed
                    ? 'bg-gradient-to-r from-green-400 to-emerald-500 gradient-text'
                    : 'bg-gradient-to-r from-red-400 to-rose-500 gradient-text'
                    }`}>
                    {score}%
                </div>

                <p className={`text-sm font-medium mb-1.5 ${darkMode ? 'text-slate-400' : 'text-gray-500'}`}>
                    {correctCount} of {totalQuestions} correct
                </p>

                <p className={`text-sm font-light mb-8 ${darkMode ? 'text-slate-500' : 'text-gray-400'}`}>
                    {passed
                        ? 'Great work! The next section is now unlocked.'
                        : `You need ${PASS_THRESHOLD}% to pass. Review the material and try again!`
                    }
                </p>

                {/* Answer Review */}
                <div className="text-left space-y-3 mb-8">
                    {exam.map((q, idx) => {
                        const userAnswer = answers[idx];
                        const isCorrect = userAnswer === q.correctAnswer;
                        return (
                            <div key={idx} className={`p-3.5 rounded-xl ${isCorrect
                                ? darkMode ? 'bg-green-900/10' : 'bg-green-50/80'
                                : darkMode ? 'bg-red-900/10' : 'bg-red-50/80'
                                }`}>
                                <div className="flex items-start gap-2.5">
                                    {isCorrect
                                        ? <CheckCircle size={16} className="text-green-500 mt-0.5 shrink-0" />
                                        : <XCircle size={16} className="text-red-500 mt-0.5 shrink-0" />
                                    }
                                    <div>
                                        <p className={`text-sm font-medium ${darkMode ? 'text-slate-300' : 'text-gray-700'}`}>
                                            {q.question}
                                        </p>
                                        {!isCorrect && (
                                            <p className={`text-xs font-light mt-1 ${darkMode ? 'text-green-400/80' : 'text-green-600'}`}>
                                                ✓ Correct: {q.options[q.correctAnswer]}
                                            </p>
                                        )}
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {!passed && (
                    <button
                        onClick={handleRetake}
                        className="inline-flex items-center gap-2 px-7 py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-sm font-semibold rounded-xl transition-all duration-200 shadow-lg shadow-indigo-500/20"
                    >
                        <RotateCcw size={16} /> Retake Exam
                    </button>
                )}
            </div>
        );
    }

    // QUESTION SCREEN
    return (
        <div className={`mt-8 rounded-2xl overflow-hidden animate-fade-in ${darkMode ? 'bg-slate-800/40' : 'bg-white shadow-lg'
            }`}>
            {/* Header */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-5 text-white">
                <div className="flex items-center justify-between mb-3">
                    <h3 className="text-base font-semibold flex items-center gap-2 tracking-tight">
                        📝 Section Exam
                    </h3>
                    <span className="bg-white/15 px-2.5 py-0.5 rounded-full text-xs font-semibold tabular-nums">
                        {currentQuestion + 1} / {totalQuestions}
                    </span>
                </div>
                {/* Progress dots */}
                <div className="flex gap-1.5">
                    {exam.map((_, idx) => (
                        <div
                            key={idx}
                            className={`h-1 flex-1 rounded-full transition-all duration-300 ${idx < currentQuestion
                                ? answers[idx] === exam[idx].correctAnswer ? 'bg-green-400' : 'bg-red-400'
                                : idx === currentQuestion ? 'bg-white' : 'bg-white/20'
                                }`}
                        />
                    ))}
                </div>
            </div>

            {/* Question */}
            <div className="p-6">
                <p className={`text-lg font-medium tracking-tight mb-6 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                    {currentQ.question}
                </p>

                <div className="space-y-2.5">
                    {currentQ.options.map((option, idx) => {
                        let classes = `w-full text-left p-4 rounded-xl transition-all duration-200 text-[15px] cursor-pointer `;

                        if (!showFeedback) {
                            classes += darkMode
                                ? 'bg-slate-700/50 hover:bg-indigo-900/30 text-slate-200 hover:text-indigo-300'
                                : 'bg-gray-50 hover:bg-indigo-50 text-gray-700 hover:text-indigo-700';
                        } else if (idx === currentQ.correctAnswer) {
                            classes += darkMode
                                ? 'bg-green-900/30 text-green-300 ring-2 ring-green-500/50'
                                : 'bg-green-50 text-green-800 ring-2 ring-green-300';
                        } else if (idx === selectedOption && idx !== currentQ.correctAnswer) {
                            classes += darkMode
                                ? 'bg-red-900/30 text-red-300 ring-2 ring-red-500/50'
                                : 'bg-red-50 text-red-800 ring-2 ring-red-300';
                        } else {
                            classes += darkMode
                                ? 'bg-slate-800/30 text-slate-600 opacity-50'
                                : 'bg-gray-50 text-gray-400 opacity-50';
                        }

                        return (
                            <button
                                key={idx}
                                disabled={showFeedback}
                                onClick={() => handleSelect(idx)}
                                className={classes}
                            >
                                <div className="flex items-center justify-between">
                                    <span>{option}</span>
                                    {showFeedback && idx === currentQ.correctAnswer && (
                                        <CheckCircle size={22} className="text-green-500 animate-scale-in" />
                                    )}
                                    {showFeedback && idx === selectedOption && idx !== currentQ.correctAnswer && (
                                        <XCircle size={22} className="text-red-500 animate-scale-in" />
                                    )}
                                </div>
                            </button>
                        );
                    })}
                </div>

                {showFeedback && (
                    <button
                        onClick={handleNext}
                        className="mt-5 w-full py-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-sm font-semibold rounded-xl transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/20 animate-fade-in"
                    >
                        {currentQuestion < totalQuestions - 1 ? (
                            <>Next Question <ChevronRight size={16} /></>
                        ) : (
                            <>See Results <Award size={16} /></>
                        )}
                    </button>
                )}
            </div>
        </div>
    );
};

export default ExamSection;


import { useState, useEffect } from 'react'
import confetti from 'canvas-confetti';
import { curriculumData } from './data/curriculum';
import { truckingCurriculumData } from './data/truckingCurriculum';
import PhaseSection from './components/PhaseSection';
import ProgressBar from './components/ProgressBar';
import AuthGate from './components/AuthGate';
import PomodoroTimer from './components/PomodoroTimer';
import Certificate from './components/Certificate';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import { BookOpen, FileText, Truck, Code, ArrowLeft, Award, Sun, Moon } from 'lucide-react';

function ThemeToggle() {
  const { darkMode, toggleTheme } = useTheme();
  return (
    <button
      onClick={toggleTheme}
      className={`p-2 rounded-full transition-all duration-300 hover:scale-110 shrink-0 ${darkMode ? 'text-yellow-400 hover:text-yellow-300 hover:bg-yellow-400/10' : 'text-indigo-600 hover:text-indigo-500 hover:bg-indigo-50'
        }`}
      title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
    >
      {darkMode ? <Sun size={16} /> : <Moon size={16} />}
    </button>
  );
}

function AppContent() {
  const { darkMode } = useTheme();

  const [completedTasks, setCompletedTasks] = useState(() => {
    const saved = localStorage.getItem('curriculumProgress');
    return saved ? JSON.parse(saved) : [];
  });

  const [activeTrack, setActiveTrack] = useState(() => {
    return localStorage.getItem('activeTrack') || null;
  });

  const [examScores, setExamScores] = useState(() => {
    const saved = localStorage.getItem('examScores');
    return saved ? JSON.parse(saved) : {};
  });

  const [showCertificate, setShowCertificate] = useState(false);

  const currentData = activeTrack === 'trucking' ? truckingCurriculumData : curriculumData;
  const totalTasks = currentData.reduce((acc, phase) => acc + phase.tasks.length, 0);

  const relevantCompleted = completedTasks.filter(id => {
    if (activeTrack === 'trucking') return id.startsWith('t');
    return !id.startsWith('t');
  });

  const progressPercentage = totalTasks === 0 ? 0 : (relevantCompleted.length / totalTasks) * 100;

  // Get exam scores for current track
  const trackScoreKey = activeTrack === 'trucking' ? 'trucking' : 'web';
  const trackScores = examScores[trackScoreKey] || {};

  useEffect(() => {
    localStorage.setItem('curriculumProgress', JSON.stringify(completedTasks));
  }, [completedTasks]);

  useEffect(() => {
    localStorage.setItem('examScores', JSON.stringify(examScores));
  }, [examScores]);

  useEffect(() => {
    if (activeTrack) {
      localStorage.setItem('activeTrack', activeTrack);
    }
    setShowCertificate(false);
  }, [activeTrack]);

  const toggleTask = (taskId) => {
    setCompletedTasks(prev => {
      const isCompleted = prev.includes(taskId);
      let newCompleted;

      if (isCompleted) {
        newCompleted = prev.filter(id => id !== taskId);
      } else {
        newCompleted = [...prev, taskId];
        const currentTrackCompleted = newCompleted.filter(id => {
          if (activeTrack === 'trucking') return id.startsWith('t');
          return !id.startsWith('t');
        });

        if (currentTrackCompleted.length === totalTasks) {
          confetti({ particleCount: 500, spread: 180, zIndex: 999 });
          setTimeout(() => setShowCertificate(true), 1500);
        } else {
          if (Math.random() > 0.85) {
            confetti({ particleCount: 60, spread: 50, origin: { y: 0.7 }, zIndex: 999 });
          }
        }
      }
      return newCompleted;
    });
  };

  const handleExamPass = (phaseId, score) => {
    setExamScores(prev => ({
      ...prev,
      [trackScoreKey]: {
        ...prev[trackScoreKey],
        [phaseId]: score
      }
    }));
  };

  // Check if a section is locked (needs previous section's exam at 80%+)
  const isSectionLocked = (index) => {
    if (index === 0) return false; // First section always open
    const prevPhaseId = currentData[index - 1].id;
    const prevScore = trackScores[prevPhaseId];
    return prevScore === undefined || prevScore < 80;
  };

  // -- TRACK SELECTION SCREEN --
  if (!activeTrack) {
    return (
      <AuthGate>
        <ThemeToggle />
        <div className={`min-h-screen flex flex-col items-center justify-center px-4 transition-colors duration-300 ${darkMode ? 'bg-slate-900' : 'bg-gradient-to-br from-slate-50 to-indigo-50/30'}`}>
          {/* Background decorations */}
          <div className="absolute top-20 right-20 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 left-20 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl"></div>

          <h1 className={`text-4xl md:text-5xl font-bold tracking-tight mb-3 animate-fade-in ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Choose Your Path
          </h1>
          <p className={`text-lg font-light mb-14 text-center max-w-md animate-fade-in ${darkMode ? 'text-slate-500' : 'text-gray-400'}`}>
            What empire do you want to build today?
          </p>

          <div className="grid md:grid-cols-2 gap-8 w-full max-w-4xl">
            <button
              onClick={() => setActiveTrack('web')}
              className={`group relative p-10 rounded-3xl shadow-lg transition-all duration-300 text-left card-hover animate-slide-up ${darkMode
                ? 'bg-slate-800/80 hover:bg-slate-800'
                : 'bg-white hover:shadow-xl'
                }`}
            >
              <div className="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 rounded-t-3xl opacity-80 group-hover:opacity-100 transition-opacity"></div>
              <div className={`mb-6 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-all duration-300 shadow-lg ${darkMode ? 'bg-indigo-500/20 text-indigo-400 shadow-indigo-500/10' : 'bg-blue-50 text-blue-600 shadow-blue-500/10'
                }`} style={{ width: '72px', height: '72px' }}>
                <Code size={36} />
              </div>
              <h2 className={`text-2xl font-bold tracking-tight mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Tech Mogul</h2>
              <p className={`text-base font-light leading-relaxed ${darkMode ? 'text-slate-400' : 'text-gray-500'}`}>
                Master Web Development. Build apps, SaaS businesses, and digital empires. From HTML to React.
              </p>
            </button>

            <button
              onClick={() => setActiveTrack('trucking')}
              className={`group relative p-10 rounded-3xl shadow-lg transition-all duration-300 text-left card-hover animate-slide-up ${darkMode
                ? 'bg-slate-800/80 hover:bg-slate-800'
                : 'bg-white hover:shadow-xl'
                }`}
              style={{ animationDelay: '0.1s' }}
            >
              <div className="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 rounded-t-3xl opacity-80 group-hover:opacity-100 transition-opacity"></div>
              <div className={`mb-6 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-all duration-300 shadow-lg ${darkMode ? 'bg-emerald-500/20 text-emerald-400 shadow-emerald-500/10' : 'bg-green-50 text-green-600 shadow-green-500/10'
                }`} style={{ width: '72px', height: '72px' }}>
                <Truck size={36} />
              </div>
              <h2 className={`text-2xl font-bold tracking-tight mb-2 ${darkMode ? 'text-white' : 'text-gray-900'}`}>Fleet Mogul</h2>
              <p className={`text-base font-light leading-relaxed ${darkMode ? 'text-slate-400' : 'text-gray-500'}`}>
                Master Compliance & Safety. Build a trucking company, manage drivers, and conquer the road.
              </p>
            </button>
          </div>
        </div>
        <PomodoroTimer />
      </AuthGate>
    )
  }

  return (
    <AuthGate>
      <div className={`min-h-screen pb-20 pt-20 font-sans transition-colors duration-300 ${darkMode ? 'bg-slate-900 text-slate-200' : 'bg-gradient-to-br from-slate-50 to-indigo-50/20 text-gray-900'}`}>
        <ProgressBar progress={progressPercentage}>
          <ThemeToggle />
        </ProgressBar>

        {/* Back Button */}
        <button
          onClick={() => setActiveTrack(null)}
          className={`fixed top-4 left-4 z-40 glass p-2.5 rounded-full shadow-lg transition-all duration-200 hover:scale-110 ${darkMode ? 'text-slate-400 hover:text-white' : 'text-gray-500 hover:text-gray-900'
            }`}
          title="Switch Track"
        >
          <ArrowLeft size={20} />
        </button>

        <main className="max-w-3xl mx-auto px-4">
          <header className="mb-14 text-center animate-fade-in">
            <div className={`inline-flex items-center gap-2 mb-5 px-3.5 py-1.5 rounded-full text-xs font-semibold tracking-wider uppercase ${darkMode ? 'bg-white/[0.05] text-slate-500' : 'bg-gray-100 text-gray-500'
              }`}>
              {activeTrack === 'trucking' ? <Truck size={13} /> : <Code size={13} />}
              {activeTrack === 'trucking' ? 'Fleet Empire Track' : 'Tech Empire Track'}
            </div>
            <h1 className={`text-4xl md:text-5xl font-bold tracking-tight mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              Zero to{' '}
              <span className={`gradient-text bg-gradient-to-r ${activeTrack === 'trucking' ? 'from-green-400 to-emerald-600' : 'from-indigo-400 to-purple-500'}`}>
                {activeTrack === 'trucking' ? 'Fleet Mogul' : 'Tech Mogul'}
              </span>
            </h1>
            <p className={`text-base font-light max-w-lg mx-auto leading-relaxed ${darkMode ? 'text-slate-500' : 'text-gray-500'}`}>
              {activeTrack === 'trucking'
                ? "Setup your authority, ace your audits, and build a safety-first logistics back office."
                : "From your first line of code to your first million. Interactive lessons to build real apps."}
            </p>

            {/* Passing info */}
            <div className={`mt-5 inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium ${darkMode ? 'bg-indigo-900/15 text-indigo-400/80' : 'bg-indigo-50/80 text-indigo-600'
              }`}>
              🎯 Score 80% or higher on each exam to unlock the next level
            </div>
          </header>

          <div className="space-y-6">
            {currentData.map((phase, index) => (
              <div key={phase.id} className="animate-slide-up" style={{ animationDelay: `${index * 0.05}s` }}>
                <PhaseSection
                  phase={phase}
                  completedTasks={completedTasks}
                  onToggle={toggleTask}
                  index={index}
                  locked={isSectionLocked(index)}
                  examScore={trackScores[phase.id]}
                  onExamPass={handleExamPass}
                />
              </div>
            ))}
          </div>
        </main>

        <footer className={`mt-20 text-center text-sm pb-10 ${darkMode ? 'text-slate-600' : 'text-gray-400'}`}>
          <p>Built with React & Tailwind CSS</p>
        </footer>

        <PomodoroTimer />

        {showCertificate && (
          <Certificate track={activeTrack} onClose={() => setShowCertificate(false)} />
        )}
      </div>
    </AuthGate>
  )
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App

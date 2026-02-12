
import { useState, useEffect } from 'react'
import confetti from 'canvas-confetti';
import { curriculumData } from './data/curriculum';
import { truckingCurriculumData } from './data/truckingCurriculum';
import PhaseSection from './components/PhaseSection';
import ProgressBar from './components/ProgressBar';
import AuthGate from './components/AuthGate';
import PomodoroTimer from './components/PomodoroTimer';
import Certificate from './components/Certificate';
import AmbientBackground from './components/AmbientBackground';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import { BookOpen, FileText, Truck, Code, ArrowLeft, ArrowRight, Award, Sun, Moon, Lock } from 'lucide-react';

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
    const hour = new Date().getHours();
    const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
    const emoji = hour < 12 ? '☀️' : hour < 17 ? '🌤️' : '🌙';

    return (
      <AuthGate>
        <div className={`min-h-screen flex flex-col items-center justify-center px-4 transition-colors duration-300 relative overflow-hidden ${darkMode ? 'bg-slate-900' : 'bg-gradient-to-br from-slate-50 via-indigo-50/20 to-violet-50/10'}`}>

          {/* Ambient background */}
          <div className={`absolute top-[-10%] right-[-5%] w-[400px] h-[400px] rounded-full blur-[120px] ${darkMode ? 'opacity-15' : 'opacity-10'}`}
            style={{ background: 'radial-gradient(circle, #8b5cf6, transparent 70%)' }}></div>
          <div className={`absolute bottom-[-10%] left-[-5%] w-[500px] h-[500px] rounded-full blur-[140px] ${darkMode ? 'opacity-10' : 'opacity-8'}`}
            style={{ background: 'radial-gradient(circle, #6366f1, transparent 70%)' }}></div>

          {/* Greeting */}
          <div className="animate-fade-in text-center mb-12">
            <p className={`text-sm font-medium tracking-wide mb-3 ${darkMode ? 'text-white/30' : 'text-gray-400'}`}>
              {emoji} {greeting}
            </p>
            <h1 className={`text-4xl md:text-5xl font-bold tracking-tight mb-3 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
              What are we building?
            </h1>
            <p className={`text-base font-light max-w-sm mx-auto leading-relaxed ${darkMode ? 'text-white/30' : 'text-gray-400'}`}>
              Pick your vibe. Learn at your pace. No pressure.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6 w-full max-w-3xl animate-fade-in" style={{ animationDelay: '0.15s' }}>
            {/* Tech Mogul Card */}
            <button
              onClick={() => setActiveTrack('web')}
              className={`group relative p-8 rounded-3xl transition-all duration-300 text-left overflow-hidden ${darkMode
                ? 'bg-white/[0.03] hover:bg-white/[0.06] ring-1 ring-white/[0.06] hover:ring-white/[0.1]'
                : 'bg-white hover:shadow-xl hover:shadow-indigo-500/5 ring-1 ring-gray-200/50 hover:ring-indigo-200'
                }`}
            >
              {/* Glow on hover */}
              <div className={`absolute top-0 right-0 w-32 h-32 rounded-full blur-[60px] transition-opacity duration-500 opacity-0 group-hover:opacity-100 ${darkMode ? 'bg-indigo-500/10' : 'bg-indigo-100/60'}`}></div>

              <div className="relative">
                <div className="text-4xl mb-5">💻</div>
                <h2 className={`text-xl font-bold tracking-tight mb-1.5 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  Tech Mogul
                </h2>
                <p className={`text-sm font-light leading-relaxed mb-5 ${darkMode ? 'text-white/35' : 'text-gray-400'}`}>
                  Build apps, launch SaaS products, and code your way to the top. From HTML to React.
                </p>
                <div className={`inline-flex items-center gap-1.5 text-xs font-medium tracking-wide ${darkMode ? 'text-indigo-400/60' : 'text-indigo-500/70'}`}>
                  Start learning <ArrowRight size={12} className="group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </button>

            {/* Fleet Mogul Card */}
            <button
              onClick={() => setActiveTrack('trucking')}
              className={`group relative p-8 rounded-3xl transition-all duration-300 text-left overflow-hidden ${darkMode
                ? 'bg-white/[0.03] hover:bg-white/[0.06] ring-1 ring-white/[0.06] hover:ring-white/[0.1]'
                : 'bg-white hover:shadow-xl hover:shadow-emerald-500/5 ring-1 ring-gray-200/50 hover:ring-emerald-200'
                }`}
            >
              {/* Glow on hover */}
              <div className={`absolute top-0 right-0 w-32 h-32 rounded-full blur-[60px] transition-opacity duration-500 opacity-0 group-hover:opacity-100 ${darkMode ? 'bg-emerald-500/10' : 'bg-emerald-100/60'}`}></div>

              <div className="relative">
                <div className="text-4xl mb-5">🚛</div>
                <h2 className={`text-xl font-bold tracking-tight mb-1.5 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  Fleet Mogul
                </h2>
                <p className={`text-sm font-light leading-relaxed mb-5 ${darkMode ? 'text-white/35' : 'text-gray-400'}`}>
                  Master compliance, manage drivers, and build a trucking empire from the ground up.
                </p>
                <div className={`inline-flex items-center gap-1.5 text-xs font-medium tracking-wide ${darkMode ? 'text-emerald-400/60' : 'text-emerald-500/70'}`}>
                  Start learning <ArrowRight size={12} className="group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </button>
          </div>

          {/* Subtle footer */}
          <p className={`mt-12 text-xs font-light animate-fade-in ${darkMode ? 'text-white/10' : 'text-gray-300'}`} style={{ animationDelay: '0.3s' }}>
            Pocket Academy · Learn by doing
          </p>
        </div>
      </AuthGate>
          {/* Return Home Button */ }
    <button
      onClick={() => {
        if (window.history.length > 1) {
          window.history.back();
        } else {
          window.location.href = 'http://localhost:8501'; // Fallback to standard Streamlit port
        }
      }}
      className={`fixed top-4 left-4 z-50 glass p-2.5 rounded-full shadow-lg transition-all duration-200 hover:scale-110 ${darkMode ? 'text-slate-400 hover:text-white bg-slate-800/50' : 'text-gray-500 hover:text-gray-900 bg-white/50'
        }`}
      title="Return to Pocket Empire"
    >
      <ArrowLeft size={20} />
      <span className="sr-only">Return Home</span>
    </button>
    );
  }

  return (
    <AuthGate>
      <div className={`min-h-screen pb-20 pt-20 font-sans transition-colors duration-300 relative overflow-hidden ${darkMode ? 'bg-slate-950 text-slate-200' : 'bg-slate-50 text-gray-900'}`}>
        <AmbientBackground />

        <div className="relative z-10">
          <ProgressBar progress={progressPercentage} onGoHome={() => setActiveTrack(null)}>
            <div className="flex items-center gap-2">
              <ThemeToggle />
              <button
                onClick={() => {
                  sessionStorage.removeItem('curriculum_auth');
                  window.location.reload();
                }}
                className={`p-2 rounded-full transition-all duration-300 hover:scale-110 shrink-0 ${darkMode ? 'text-slate-400 hover:text-red-400 hover:bg-red-400/10' : 'text-gray-400 hover:text-red-500 hover:bg-red-50'
                  }`}
                title="Lock App"
              >
                <Lock size={16} />
              </button>
            </div>
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

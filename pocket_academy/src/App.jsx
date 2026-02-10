
import { useState, useEffect } from 'react'
import confetti from 'canvas-confetti';
import { curriculumData } from './data/curriculum';
import { truckingCurriculumData } from './data/truckingCurriculum';
import PhaseSection from './components/PhaseSection';
import ProgressBar from './components/ProgressBar';
import AuthGate from './components/AuthGate';
import PomodoroTimer from './components/PomodoroTimer';
import Certificate from './components/Certificate';
import { BookOpen, FileText, Truck, Code, ArrowLeft, Award } from 'lucide-react';

function App() {
  // Load initial state from local storage or start empty
  const [completedTasks, setCompletedTasks] = useState(() => {
    const saved = localStorage.getItem('curriculumProgress');
    return saved ? JSON.parse(saved) : [];
  });

  const [activeTrack, setActiveTrack] = useState(() => {
    // Remember the last track user was on
    return localStorage.getItem('activeTrack') || null;
  });

  const [showCertificate, setShowCertificate] = useState(false);

  // Decide which data to show based on track
  const currentData = activeTrack === 'trucking' ? truckingCurriculumData : curriculumData;

  // Calculate total progress
  const totalTasks = currentData.reduce((acc, phase) => acc + phase.tasks.length, 0);

  // Filter completed tasks to only count ones relevant to current track (simple approximation)
  // Ideally, we'd enable separate progress storage, but this works if IDs are unique
  const relevantCompleted = completedTasks.filter(id => {
    if (activeTrack === 'trucking') return id.startsWith('t');
    return !id.startsWith('t');
  });

  const progressPercentage = totalTasks === 0 ? 0 : (relevantCompleted.length / totalTasks) * 100;

  // Save to local storage whenever state changes
  useEffect(() => {
    localStorage.setItem('curriculumProgress', JSON.stringify(completedTasks));
  }, [completedTasks]);

  useEffect(() => {
    if (activeTrack) {
      localStorage.setItem('activeTrack', activeTrack);
    }
    setShowCertificate(false);
  }, [activeTrack]);

  // Handle task toggling
  const toggleTask = (taskId) => {
    setCompletedTasks(prev => {
      const isCompleted = prev.includes(taskId);
      let newCompleted;

      if (isCompleted) {
        newCompleted = prev.filter(id => id !== taskId);
      } else {
        newCompleted = [...prev, taskId];
        // We check completion based on the NEW state, which is this `newCompleted` array
        // But we need to filter it again for the current track to be accurate
        const currentTrackCompleted = newCompleted.filter(id => {
          if (activeTrack === 'trucking') return id.startsWith('t');
          return !id.startsWith('t');
        });

        if (currentTrackCompleted.length === totalTasks) {
          triggerConfetti({ particleCount: 500, spread: 180 });
          setTimeout(() => setShowCertificate(true), 1500); // Show cert after confetti
        } else {
          // Random celebration for normal tasks
          if (Math.random() > 0.8) {
            triggerConfetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
          }
        }
      }
      return newCompleted;
    });
  };

  const triggerConfetti = (opts) => {
    confetti({ ...opts, zIndex: 999 });
  }

  // -- TRACK SELECTION SCREEN --
  if (!activeTrack) {
    return (
      <AuthGate>
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
          <h1 className="text-4xl font-extrabold text-gray-900 mb-2">Choose Your Path</h1>
          <p className="text-gray-500 mb-12 text-center max-w-md">What empire do you want to build today?</p>

          <div className="grid md:grid-cols-2 gap-6 w-full max-w-4xl">
            <button
              onClick={() => setActiveTrack('web')}
              className="group relative bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:border-blue-500 hover:shadow-2xl transition-all text-left"
            >
              <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-t-2xl"></div>
              <div className="mb-4 bg-blue-50 w-16 h-16 rounded-xl flex items-center justify-center text-blue-600 group-hover:scale-110 transition-transform">
                <Code size={32} />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Tech Mogul</h2>
              <p className="text-gray-500">Master Web Development. Build apps, SaaS businesses, and digital empires. From HTML to React.</p>
            </button>

            <button
              onClick={() => setActiveTrack('trucking')}
              className="group relative bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:border-green-500 hover:shadow-2xl transition-all text-left"
            >
              <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-green-500 to-emerald-700 rounded-t-2xl"></div>
              <div className="mb-4 bg-green-50 w-16 h-16 rounded-xl flex items-center justify-center text-green-600 group-hover:scale-110 transition-transform">
                <Truck size={32} />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Fleet Mogul</h2>
              <p className="text-gray-500">Master Compliance & Safety. Build a trucking company, manage drivers, and conquer the road.</p>
            </button>
          </div>
        </div>
        <PomodoroTimer />
      </AuthGate>
    )
  }

  return (
    <AuthGate>
      <div className="min-h-screen pb-20 pt-24 font-sans text-gray-900 bg-gray-50">
        <ProgressBar progress={progressPercentage} />

        {/* Back to Home Button */}
        <button
          onClick={() => setActiveTrack(null)}
          className="fixed top-4 left-4 z-40 bg-white/80 backdrop-blur p-2 rounded-full shadow hover:bg-white text-gray-500 hover:text-gray-900 transition"
          title="Switch Track"
        >
          <ArrowLeft size={20} />
        </button>

        <main className="max-w-3xl mx-auto px-4">
          <header className="mb-12 text-center">
            <div className="inline-flex items-center gap-2 mb-4 px-3 py-1 rounded-full bg-gray-100 text-gray-600 text-xs font-bold tracking-wide uppercase">
              {activeTrack === 'trucking' ? <Truck size={14} /> : <Code size={14} />}
              {activeTrack === 'trucking' ? 'Fleet Empire Track' : 'Tech Empire Track'}
            </div>
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-gray-900 mb-4">
              {activeTrack === 'trucking' ? 'Zero to ' : 'Zero to '}
              <span className={`text-transparent bg-clip-text bg-gradient-to-r ${activeTrack === 'trucking' ? 'from-green-600 to-emerald-800' : 'from-blue-600 to-purple-600'}`}>
                {activeTrack === 'trucking' ? 'Fleet Mogul' : 'Tech Mogul'}
              </span>
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
              {activeTrack === 'trucking'
                ? "Setup your authority, ace your audits, and build a safety-first logistics back office."
                : "From your first line of code to your first million. Interactive lessons to build real apps."}
            </p>

            <div className="flex justify-center gap-4">
              {/* Context aware links could go here */}
            </div>
          </header>

          <div className="space-y-6">
            {currentData.map(phase => (
              <PhaseSection
                key={phase.id}
                phase={phase}
                completedTasks={completedTasks}
                onToggleTask={toggleTask}
              />
            ))}
          </div>
        </main>

        <footer className="mt-20 text-center text-gray-400 text-sm pb-10">
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

export default App

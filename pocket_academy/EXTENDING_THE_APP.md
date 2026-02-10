# 🛠️ Extending Your App

This app is designed to grow with you. Here is how you can add new features.

## 1. Adding More Lessons
Open `src/data/curriculum.js`. This file holds all the content.
To add a new Phase:
```javascript
{
  id: 6, // Make sure this is unique
  title: "Phase 6: Your New Phase",
  description: "Description here...",
  color: "bg-pink-500", // Tailwind color class
  tasks: [
    { id: "6-1", text: "New Task 1" },
    { id: "6-2", text: "New Task 2" }
  ],
  quiz: {
      question: "Your Question?",
      options: ["A", "B", "C", "D"],
      correctAnswer: 0
  }
}
```

## 2. Changing the Passkey
Open `src/components/AuthGate.jsx`.
Find this line:
```javascript
if (passkey === '1234') { 
```
Change `'1234'` to whatever secret password you want!

## 3. Adding a New Tool (e.g., Calculator)
1.  Create a new file: `src/components/Calculator.jsx`.
2.  Write your React component code (inputs, buttons, logic).
3.  Import it into `src/App.jsx`.
4.  Place it where you want it to appear (e.g., inside the `<main>` tag).

## 4. Customizing the Design
*   **Colors/Fonts**: Edit `src/index.css` or use Tailwind classes in the components.
*   **Layout**: Edit `src/App.jsx` to move the header/footer around.

# Phase 0: The Pro Workbench Setup

Welcome to the start of your journey! We are going to set up **Visual Studio Code (VS Code)** exactly how professional developers at Google, Facebook, and Netflix use it.

## 1. The Editor
You should already have VS Code installed. Open it up!

## 2. Essential Extensions
Extensions give VS Code "superpowers".
1.  Click the **Extensions Icon** on the left sidebar (looks like tetris blocks).
2.  Search for and install these **Top 5**:
    *   **Prettier - Code formatter**: Automatically cleans up your messy code every time you save.
    *   **ESLint**: Finds errors in your code (like spellcheck for JavaScript).
    *   **Live Server**: Lets you right-click an HTML file and see it instantly in your browser (auto-refreshes when you save!).
    *   **VS Code Icons**: Makes your file explorer look beautiful with distinct icons for every file type.
    *   **Auto Rename Tag**: If you change `<h1>` to `<h2>`, it automatically changes the closing tag `</h2>` for you.

## 3. Settings Tuning
1.  Press `Cmd + ,` (Command + Comma) to open Settings.
2.  Search for "Format On Save".
3.  **Check the box**. (Now Prettier works automatically!)
4.  Search for "Word Wrap".
5.  Set it to "on". (So long lines don't run off the screen).

## 4. The Terminal
You don't need a separate terminal app.
1.  Press `Ctrl + ~` (Control + Tilde, key under Esc).
2.  Boom! Your terminal is right inside VS Code. This is where you'll run commands like `npm run dev`.

## 5. Your First "Hello World"
1.  Click **File -> Open Folder**.
2.  Create a new folder on your Desktop called `web-learning`.
3.  Inside, create a file called `index.html`.
4.  Type `!` and press **Tab**.
5.  VS Code will generate a full HTML skeleton for you!
6.  Inside the `<body>` tag, type `<h1>Hello World!</h1>`.
7.  Right-click `index.html` and choose **"Open with Live Server"**.

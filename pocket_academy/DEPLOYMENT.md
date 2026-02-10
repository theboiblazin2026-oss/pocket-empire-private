# 🚀 Deployment Guide: Go Live!

To access your app from **anywhere** (phone, iPad, library computer), you need to "Deploy" it to the internet. We will use **Vercel** because it's free, fast, and works perfectly with the tools we used.

## Step 1: Push to GitHub
You need your code on GitHub first.
1.  Open Terminal in your project folder.
2.  `git add .`
3.  `git commit -m "Ready for deploy"`
4.  Create a new repo on GitHub.com.
5.  Follow the instructions on GitHub to `git remote add origin ...` and `git push`.

## Step 2: Deploy on Vercel
1.  Go to [Vercel.com](https://vercel.com) and Sign Up (you can use your GitHub account).
2.  Click **"Add New..."** -> **"Project"**.
3.  You will see your GitHub repository listed (e.g., `interactive-curriculum-app`). Click **Import**.
4.  **Framework Preset**: It should auto-detect "Vite". If not, select it.
5.  Click **Deploy**.

## Step 3: Use It!
*   Wait about 1 minute.
*   Vercel will give you a domain like: `https://interactive-curriculum-app-yourname.vercel.app`
*   **Share it (or don't)!** You have the passkey protection, so even if someone guesses the URL, they can't see your progress.

## Step 4: Add to Home Screen (iPad/iPhone)
1.  Open that new URL in Safari on your iPad.
2.  Tap the **Share** button (box with arrow up).
3.  Scroll down and tap **"Add to Home Screen"**.
4.  Now it looks and feels like a real app icon on your iPad!

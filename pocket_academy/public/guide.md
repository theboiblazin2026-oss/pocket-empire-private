# Website and App Builder Terminology Guide

This guide breaks down the common terms and languages used in building websites and applications, from traditional coding to modern visual builders.

## 1. Core Building Blocks (The "Code" Layer)
These are the fundamental languages that power the web. Even if you use a visual builder, these are what's happening under the hood.

*   **HTML (HyperText Markup Language)**: The structure of a webpage. Think of it as the skeleton—headings, paragraphs, images, buttons.
*   **CSS (Cascading Style Sheets)**: The valid style and layout. This controls colors, fonts, spacing, and positioning. It's the "skin" and "clothing" of the website.
*   **JavaScript (JS)**: The logic and interactivity. This makes things happen—popups, animations, form submissions, data fetching. It's the "muscle" and "brain."

## 2. Development Approaches

### A. Traditional Coding (Full-Code)
*   **Frontend**: The part of the app users see and interact with (Client-side).
    *   **Frameworks**: React, Vue, Angular, Svelte to build complex UIs efficiently.
*   **Backend**: The server side that handles data, logic, and security (Server-side).
    *   **Languages**: Node.js (JavaScript), Python, Ruby, PHP, Java, Go.
*   **Full Stack**: Developing both frontend and backend.
*   **API (Application Programming Interface)**: The bridge allowing the frontend to talk to the backend (e.g., fetching a list of users).
*   **Database**: Where data is stored (e.g., SQL [MySQL, PostgreSQL] or NoSQL [MongoDB, Firebase]).

### B. Low-Code / No-Code (LCNC) Platforms
Allows building apps with graphical interfaces instead of writing raw code.

*   **No-Code**: Designed for non-developers. Purely visual, drag-and-drop.
    *   **Examples**: Bubble, Glide, Adalo, Webflow (for websites).
    *   **Best for**: MVP (Minimum Viable Product), internal tools, simple apps.
*   **Low-Code**: Designed for developers to speed up work. Visual tools but allows custom code injection.
    *   **Examples**: OutSystems, Mendix, Retool, Appsmith.
    *   **Best for**: Enterprise apps, rapid prototyping, admin panels.

### C. CMS (Content Management Systems)
Focuses on managing content (blogs, stores) rather than complex app logic.
*   **Examples**: WordPress, Shopify, Squarespace, Wix.
*   **Theme/Template**: Pre-designed layouts you can customize.
*   **Plugin/Extension**: Add-ons to extend functionality (e.g., SEO tools, contact forms).

## 3. App Types & Terminology

### Web Apps
*   **SPA (Single Page Application)**: An app that loads a single HTML page and dynamically updates content as the user interacts (feels like a native app). Examples: Gmail, Trello.
*   **PWA (Progressive Web App)**: A website that can be "installed" on a phone, works offline, and sends push notifications.
*   **Responsive Design**: Ensuring the site looks good on all screen sizes (Desktop, Tablet, Mobile).

### Mobile Apps
*   **Native App**: Built specifically for one platform using its native language.
    *   **iOS**: Swift / Objective-C
    *   **Android**: Kotlin / Java
    *   **Pros**: Best performance, access to all device features.
*   **Cross-Platform / Hybrid**: One codebase that runs on both iOS and Android.
    *   **Examples**: React Native, Flutter, Ionic.
    *   **Pros**: Cheaper and faster to build than two native apps.

## 4. Design & UX/UI Terms
*   **UI (User Interface)**: The visual look (buttons, colors, typography).
*   **UX (User Experience)**: How the user feels and navigates through the app (flow, ease of use).
*   **Wireframe**: A low-fidelity sketch of the layout (blueprint).
*   **Prototype**: A clickable, interactive mockup that looks like the real app but has no code behind it (often done in Figma).
*   **Breakpoint**: The screen width at which the layout changes (e.g., switching from 3 columns to 1 column on mobile).

## 5. Deployment & Infrastructure
*   **Hosting**: The service that stores your website files and makes them accessible on the internet (e.g., Vercel, Netlify, AWS, Heroku).
*   **Domain**: The web address (e.g., `google.com`).
*   **DNS (Domain Name System)**: Translates the domain name into the server's IP address.
*   **SSL (Secure Sockets Layer)**: Encrypts the connection (makes your site `https://` with the padlock icon).
*   **CI/CD (Continuous Integration/Continuous Deployment)**: Automating the process of testing and deploying code changes.

## 6. How SEO Fits In (Search Engine Optimization)
SEO isn't just about keywords; it relies heavily on how the site is built.

*   **HTML & Semantics**: Search engines (like Google) read the HTML code to understand what the page is about. Using proper tags (like `<h1>` for the main title, `<p>` for paragraphs, `alt` text for images) makes it easier for them to "crawl" and index your site.
*   **Performance (Core Web Vitals)**: Before showing your site in search results, Google checks how fast it loads.
    *   **Bloated CSS/JS**: Too much unused code slows down the site, hurting your ranking.
    *   **Image Optimization**: Large images take longer to load.
*   **Rendering Matters (SSR vs. CSR)**:
    *   **SSR (Server-Side Rendering)**: Best for SEO. The server sends a fully-formed HTML page. Google's bots see the content immediately. (e.g., WordPress, Next.js).
    *   **CSR (Client-Side Rendering)**: Harder for SEO. The browser gets an empty shell and JavaScript fills it in later. Sometimes bots miss the content before it loads. (e.g., basic React apps).
*   **Mobile-First Indexing**: Google primarily looks at the *mobile version* of your site to decide where to rank it. If your **Responsive Design** is broken on phones, your desktop ranking will suffer too.

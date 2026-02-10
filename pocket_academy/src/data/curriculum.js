export const curriculumData = [
    {
        id: 0,
        title: "Level 0: The Secret HQ 🕵️‍♂️",
        description: "Every superhero needs a base. Let's set up your computer to build million-dollar ideas.",
        color: "bg-slate-600",
        sketchChallenge: "Draw your ideal desk setup (Monitors, Keyboard, Coffee).",
        lingo: [
            { term: "IDE", def: "Integrated Development Environment. A fancy name for 'Text Editor for Code'." },
            { term: "Terminal", def: "The text-only screen where you type commands to the computer." },
            { term: "Browser", def: "Chrome, Safari, Firefox. The program that reads your HTML code." }
        ],
        tasks: [
            {
                id: "0-1",
                text: "Computer: Get your laptop ready (Your command center)",
                tool: "Hardware",
                detail: "Find a quiet spot with good Wi-Fi.\nPlugin your charger.\nClear off your desktop (digital and physical).\nThis is your workspace now. Treat it like a cockpit."
            },
            {
                id: "0-2",
                text: "Install VS Code: This is where we write the magic spells (code)",
                link: "https://code.visualstudio.com/",
                tool: "VS Code",
                detail: "1. Go to code.visualstudio.com.\n2. Download the version for your OS (Mac or Windows).\n3. Install and Open it.\n4. This software is the industry standard. 99% of pros use it."
            },
            {
                id: "0-3",
                text: "Extensions: Add 'Superpowers' to VS Code (Prettier, Live Server)",
                tool: "VS Code",
                detail: "1. Open VS Code.\n2. Click the 'Squares' icon on the left sidebar (Extensions).\n3. Search for 'Prettier' and click Install (It makes your code look neat).\n4. Search for 'Live Server' and click Install (It lets you see your website instantly)."
            },
            {
                id: "0-4",
                text: "Browser: Install Chrome (Your window to the world)",
                link: "https://www.google.com/chrome/",
                tool: "Chrome",
                detail: "1. If you don't have Google Chrome, download it.\n2. Developers love Chrome because of its 'DevTools'.\n3. Press F12 (or Right Click -> Inspect) on any webpage to see under the hood."
            },
            {
                id: "0-5",
                text: "Terminal: The black box hackers use (Don't worry, it's easy!)",
                tool: "Terminal",
                detail: "1. On Mac: Press Cmd+Space, type 'Terminal', and hit Enter.\n2. On Windows: Search for 'PowerShell' and open it.\n3. Type 'echo hello' and press Enter.\n4. The computer should reply 'hello'. You just talked to the machine."
            },
            {
                id: "0-6",
                text: "Git: The 'Save Game' button for your code",
                link: "https://git-scm.com/",
                tool: "Git",
                detail: "1. Download Git from git-scm.com.\n2. Install it (click Next, Next, Next).\n3. Open your Terminal and type 'git --version'.\n4. If it shows a number (like 2.30.0), you are ready."
            },
            {
                id: "0-7",
                text: "Node.js: The engine that runs your robots",
                link: "https://nodejs.org/",
                tool: "Node.js",
                detail: "1. Go to nodejs.org.\n2. Download the 'LTS' (Long Term Support) version.\n3. Install it.\n4. In Terminal, type 'node -v'. You should see a version number."
            }
        ],
        exam: [
            { question: "What is VS Code used for?", options: ["Watching movies", "Writing code", "Playing games", "Shopping"], correctAnswer: 1 },
            { question: "What does 'Terminal' refer to?", options: ["A bus station", "A text-based command interface", "A type of font", "A video player"], correctAnswer: 1 },
            { question: "What is Git used for?", options: ["Chatting online", "Version control (saving code history)", "Browsing the web", "Editing photos"], correctAnswer: 1 },
            { question: "What does an IDE help you do?", options: ["Cook food", "Write and edit code efficiently", "Play music", "Install hardware"], correctAnswer: 1 },
            { question: "What does Node.js allow you to do?", options: ["Run JavaScript outside the browser", "Edit images", "Browse social media", "Design logos"], correctAnswer: 0 }
        ]
    },
    {
        id: 1,
        title: "Level 1: The Lemonade Stand 🍋 (HTML)",
        description: "Build your first digital product. We'll make a website that can actually sell things.",
        color: "bg-orange-500",
        sketchChallenge: "Sketch the layout of your Lemonade Stand website (Title, Image, Price).",
        lingo: [
            { term: "Tag", def: "The < > things in HTML. Like <p> for paragraph or <img> for image." },
            { term: "Element", def: "One whole piece of a website, from the start tag to the end tag." },
            { term: "Attribute", def: "Extra info inside a tag. Like src='image.jpg'." }
        ],
        tasks: [
            {
                id: "1-1",
                text: "HTML Tags: The bricks of the web (<p>, <h1>, <button>)",
                tool: "VS Code",
                detail: "1. Create a folder named 'website'.\n2. Open it in VS Code.\n3. Create a file 'index.html'.\n4. Type '!' and hit Tab.\n5. Press Cmd+S (Mac) or Ctrl+S (Windows) to save."
            },
            {
                id: "1-2",
                text: "Project: Build a 'Business Card' website for yourself",
                tool: "VS Code",
                detail: "1. Use <h1> for your name.\n2. Use <p> for your job title.\n3. Use <p> for your bio.\n4. Right-click the file and select 'Open with Live Server' to see it."
            },
            {
                id: "1-3",
                text: "Images & Links: connecting your site to the world",
                tool: "Web / Code",
                detail: "1. Find a picture of yourself (or a cool avatar).\n2. Drag it into your folder.\n3. Add <img src='my-photo.jpg' width='200' />.\n4. Add a link: <a href='https://google.com'>My Google</a>."
            },
            {
                id: "1-4",
                text: "Forms: How to let customers talk to you",
                tool: "VS Code",
                detail: "1. Add a <form> tag.\n2. Inside it, add <input type='text' placeholder='Your Email' />.\n3. Add <button>Subscribe</button>.\n4. Now people can type (even if it doesn't send yet)."
            },
            {
                id: "1-5",
                text: "Publishing: putting your site on the internet for FREE",
                tool: "Vercel / Netlify",
                detail: "1. Go to netlify.com and sign up.\n2. Drag your 'website' folder onto their page.\n3. BOOM. You have a live URL.\n4. Send it to a friend."
            }
        ],
        exam: [
            { question: "Which tag creates a big heading?", options: ["<p>", "<button>", "<h1>", "<img>"], correctAnswer: 2 },
            { question: "What does the <a> tag do?", options: ["Adds an image", "Creates a link", "Makes text bold", "Plays a video"], correctAnswer: 1 },
            { question: "What is an HTML attribute?", options: ["A type of website", "Extra info inside a tag", "A programming language", "A CSS style"], correctAnswer: 1 },
            { question: "Which tag adds an image?", options: ["<p>", "<img>", "<h1>", "<div>"], correctAnswer: 1 },
            { question: "What does HTML stand for?", options: ["Hyper Tool Markup Listing", "HyperText Markup Language", "High Tech Modern Language", "Home Text Making Layout"], correctAnswer: 1 }
        ]
    },
    {
        id: 2,
        title: "Level 2: The Designer 🎨 (CSS)",
        description: "Nobody enters an ugly store. Let's make your site look professional and expensive.",
        color: "bg-pink-500",
        sketchChallenge: "Draw a Color Palette wheel. Pick 3 colors for your brand.",
        lingo: [
            { term: "Selector", def: "How you pick which element to style. e.g., 'h1 { color: red; }'" },
            { term: "Padding", def: "The space INSIDE the box, like bubble wrap." },
            { term: "Margin", def: "The space OUTSIDE the box, pushing other things away." }
        ],
        tasks: [
            {
                id: "2-1",
                text: "CSS Basics: Changing colors, fonts, and sizes",
                tool: "VS Code",
                detail: "1. Create a file 'style.css'.\n2. In html <head>, add <link rel='stylesheet' href='style.css'>.\n3. In css: body { background: black; color: white; }.\n4. Save and watch your site go dark mode."
            },
            {
                id: "2-2",
                text: "The Box Model: Margins and Padding (Space is luxury)",
                tool: "VS Code",
                detail: "1. Add a border to an element: border: 1px solid red;\n2. Add padding: 20px; (Text moves away from border).\n3. Add margin: 50px; (Element pushes away from neighbors).\n4. Learn this well. It is 90% of layout."
            },
            {
                id: "2-3",
                text: "Flexbox: Moving things around like Lego blocks",
                tool: "VS Code",
                detail: "1. Wrap your elements in a <div class='container'>.\n2. In CSS: .container { display: flex; }.\n3. Add justify-content: center; to center them.\n4. Add gap: 20px; for space between."
            },
            {
                id: "2-4",
                text: "Responsive: Making it look great on iPhones and iPads",
                tool: "Chrome DevTools",
                detail: "1. Implement @media (max-width: 600px) { ... }.\n2. Change flex-direction to 'column' for mobile.\n3. Open DevTools: Press F12 (Windows) or Cmd+Option+I (Mac).\n4. Click the 'Phone Icon' to test different screen sizes."
            },
            {
                id: "2-5",
                text: "Project: Style your Business Card to look like Apple/Nike",
                tool: "Design",
                detail: "1. Pick a nice font from fonts.google.com.\n2. Use a subtle background color (not neon).\n3. Add rounded-corners (border-radius: 10px).\n4. Add a shadow (box-shadow: 0 4px 10px rgba(0,0,0,0.1))."
            }
        ],
        exam: [
            { question: "What language controls colors and fonts?", options: ["HTML", "CSS", "Python", "English"], correctAnswer: 1 },
            { question: "What is Padding?", options: ["Space outside the element", "Space inside the element", "A type of font", "A border style"], correctAnswer: 1 },
            { question: "What does Flexbox help with?", options: ["Adding images", "Laying out elements in rows/columns", "Playing audio", "Writing JavaScript"], correctAnswer: 1 },
            { question: "What does 'Responsive Design' mean?", options: ["Fast loading speed", "Works on all screen sizes", "Dark mode only", "Has animations"], correctAnswer: 1 },
            { question: "What is a CSS Selector?", options: ["A tool to copy code", "How you target which element to style", "A color picker", "A font name"], correctAnswer: 1 }
        ]
    },
    {
        id: 3,
        title: "Level 3: The Magician 🪄 (JavaScript)",
        description: "Static sites are boring. Let's add magic: moving parts, calculators, and games.",
        color: "bg-yellow-500",
        sketchChallenge: "Draw a logic flow: 'IF button clicked -> THEN play sound'.",
        lingo: [
            { term: "Variable", def: "A container for storing data values. x = 5." },
            { term: "Function", def: "A block of code designed to perform a particular task." },
            { term: "Bug", def: "An error, flaw, or fault in a computer program." }
        ],
        tasks: [
            {
                id: "3-1",
                text: "Variables: Storing information (Like a backpack)",
                tool: "VS Code",
                detail: "1. Create 'script.js' and link it in HTML.\n2. Type: let score = 0;\n3. Type: const name = 'Your Name';\n4.  Press Cmd+Option+J (Mac) or Ctrl+Shift+J (Windows) to open Console."
            },
            {
                id: "3-2",
                text: "Functions: Creating your own magic spells",
                tool: "VS Code",
                detail: "1. Write: function sayHello() { alert('Hello!'); }\n2. Nothing happens yet.\n3. You have to call it: sayHello();\n4. Now a popup appears. You made magic."
            },
            {
                id: "3-3",
                text: "Events: Making things happen when you Click or Tap",
                tool: "VS Code",
                detail: "1. In HTML, add <button onclick='sayHello()'>Click Me</button>.\n2. Click the button.\n3. The alert pops up.\n4. You just connected HTML to JS."
            },
            {
                id: "3-4",
                text: "Logic: If This, Then That (Teaching the computer to think)",
                tool: "VS Code",
                detail: "1. Write: if (score > 10) { alert('You Win!'); }\n2. Change score to 11 and run it.\n3. Change score to 5 and run it.\n4. The computer is making decisions based on data."
            },
            {
                id: "3-5",
                text: "Project: Build a 'Tip Calculator' app for restaurants",
                tool: "Project",
                detail: "1. Input: Bill Amount.\n2. Input: Tip %.\n3. Button: Calculate.\n4. JS: Take amount * percent and show the result."
            }
        ],
        exam: [
            { question: "What is a Variable?", options: ["A container that holds data", "A type of car", "A computer virus", "A website"], correctAnswer: 0 },
            { question: "What is a Function?", options: ["A button", "A reusable block of code", "A style rule", "An image tag"], correctAnswer: 1 },
            { question: "What is an 'Event' in JavaScript?", options: ["A party", "Something that happens (click, type, scroll)", "An error", "A variable"], correctAnswer: 1 },
            { question: "What is a Bug?", options: ["An insect in your computer", "An error in your code", "A feature", "A type of variable"], correctAnswer: 1 },
            { question: "What does 'console.log()' do?", options: ["Deletes files", "Prints output to the developer console", "Creates a website", "Sends an email"], correctAnswer: 1 }
        ]
    },
    {
        id: 4,
        title: "Level 4: The Factory 🏭 (React)",
        description: "Stop building one by one. Build a factory that makes apps for you.",
        color: "bg-cyan-500",
        sketchChallenge: "Draw a 'Component' Tree (App -> Header, Main, Footer).",
        lingo: [
            { term: "Component", def: "A reusable piece of UI. Like a Lego brick." },
            { term: "State", def: "Data that changes over time (like a score or a user's name)." },
            { term: "Props", def: "Information passed from a parent component to a child." }
        ],
        tasks: [
            {
                id: "4-1",
                text: "Components: Building reusable parts (Like Lego bricks)",
                tool: "React",
                detail: "1. A component is just a function that returns HTML.\n2. Create function Button() { return <button>Click</button> }\n3. Use it like a tag: <Button />\n4. Use it 100 times easily."
            },
            {
                id: "4-2",
                text: "State: Giving your app a memory",
                tool: "React",
                detail: "1. import { useState } from 'react';\n2. const [count, setCount] = useState(0);\n3. setCount(count + 1) increases it.\n4. React automatically updates the screen when state changes."
            },
            {
                id: "4-3",
                text: "Vite: The super-fast engine for your apps",
                tool: "Terminal",
                detail: "1. Open Terminal (Mac) or PowerShell (Windows).\n2. Type: npm create vite@latest\n3. Follow prompts (Select React + JavaScript).\n4. cd into folder, npm install, npm run dev. You have a full app running."
            },
            {
                id: "4-4",
                text: "Polishing: Using Tailwind CSS for instant style",
                tool: "Tailwind",
                detail: "1. Install Tailwind via their guide.\n2. Add classes like 'bg-blue-500 text-white p-4'.\n3. No more separate CSS files.\n4. It's fast and looks professional instantly."
            },
            {
                id: "4-5",
                text: "Project: Build a 'Search Engine' for movies",
                tool: "React Project",
                detail: "1. Create an Input field.\n2. Store input in 'State'.\n3. Filter a list of movies based on that input.\n4. Display the results."
            }
        ],
        exam: [
            { question: "What is a React Component?", options: ["A reusable building block", "A virus", "A mistake", "A slow computer"], correctAnswer: 0 },
            { question: "What is 'State' in React?", options: ["A US state", "Data that changes and triggers re-renders", "A CSS property", "A type of tag"], correctAnswer: 1 },
            { question: "What are Props?", options: ["Stage decorations", "Data passed from parent to child", "Error messages", "CSS classes"], correctAnswer: 1 },
            { question: "What tool does Vite replace?", options: ["CSS", "A slower bundler like Webpack", "HTML", "The browser"], correctAnswer: 1 },
            { question: "What is JSX?", options: ["A new language", "HTML-like syntax inside JavaScript", "A type of database", "A server framework"], correctAnswer: 1 }
        ]
    },
    {
        id: 5,
        title: "Level 5: The CEO 💼 (Business & Data)",
        description: "Handle real customers, user accounts, and data. Build the next Facebook or Amazon.",
        color: "bg-green-600",
        sketchChallenge: "Draw a Database Schema (User -> Orders -> Items).",
        lingo: [
            { term: "Database", def: "An organized collection of structured information, or data." },
            { term: "API", def: "Application Programming Interface. How computers talk to each other." },
            { term: "Auth", def: "Authentication. Verifying who a user is (Login)." }
        ],
        tasks: [
            {
                id: "5-1",
                text: "Databases: Where to keep all your customer info",
                tool: "Supabase / Firebase",
                detail: "1. Use a service like Supabase or Firebase.\n2. Create a table called 'Users'.\n3. Add columns: id, email, created_at.\n4. This lives in the cloud, not on your laptop."
            },
            {
                id: "5-2",
                text: "API: Talking to other computers (like Stripe for money)",
                tool: "Code",
                detail: "1. APIs happen via 'fetch' in JS.\n2. fetch('https://api.stripe.com...')\n3. You send data, they send back a response.\n4. It's how apps talk to banks, maps, and AI."
            },
            {
                id: "5-3",
                text: "Authentication: Letting users Log In safely",
                tool: "Security",
                detail: "1. Never write your own password security (you will get hacked).\n2. Use Supabase Auth or Clerk.\n3. Users sign up with Email/Password or Google.\n4. You get a 'User ID' to track them."
            },
            {
                id: "5-4",
                text: "Project: E-Commerce Store (Sell real products!)",
                tool: "Full Stack",
                detail: "1. List products from Database.\n2. Add 'Buy' button.\n3. When clicked, call Stripe API.\n4. Build a checkout page."
            },
            {
                id: "5-5",
                text: "Mobile: Turn your web store into a phone app",
                tool: "Capacitor",
                detail: "1. Apps like CapacitorJS wrap your website in a native shell.\n2. Run a command.\n3. Get an Xcode project.\n4. Deploy to the App Store."
            }
        ],
        exam: [
            { question: "What do we use to store customer data?", options: ["RAM", "Database", "Notepad", "Sticky Notes"], correctAnswer: 1 },
            { question: "What does API stand for?", options: ["Apple Pie Interface", "Application Programming Interface", "Auto Program Install", "Advanced Phone Input"], correctAnswer: 1 },
            { question: "What is Authentication?", options: ["Making things fast", "Verifying a user's identity", "Adding animations", "Writing CSS"], correctAnswer: 1 },
            { question: "What does CRUD stand for?", options: ["Crash, Run, Update, Delete", "Create, Read, Update, Delete", "Code, Review, Upload, Deploy", "Clean, Restart, Undo, Debug"], correctAnswer: 1 },
            { question: "What is Stripe used for?", options: ["Painting", "Processing payments", "Hosting websites", "Writing code"], correctAnswer: 1 }
        ]
    },
    {
        id: 6,
        title: "Level 6: The Architect 🏛️ (System Design)",
        description: "Designing systems that can handle 1 million users. Clouds and Servers.",
        color: "bg-indigo-700",
        sketchChallenge: "Draw a Cloud Architecture (User -> Load Balancer -> Server Pool -> DB).",
        lingo: [
            { term: "Cloud", def: "Servers that are accessed over the Internet." },
            { term: "Scalability", def: "The ability of a system to handle growing amount of work." },
            { term: "Latency", def: "The delay before a transfer of data begins." }
        ],
        tasks: [
            {
                id: "6-1",
                text: "Cloud Providers: AWS, Google Cloud, Vercel",
                tool: "Cloud",
                detail: "1. AWS is the biggest (Amazon).\n2. Vercel is the easiest for frontend.\n3. You rent computers by the second.\n4. No need to buy physical servers anymore."
            },
            {
                id: "6-2",
                text: "Serverless: Running code without managing servers",
                tool: "Vercel Functions",
                detail: "1. Write a function named 'api/hello.js'.\n2. Vercel runs it only when someone visits that URL.\n3. You pay $0 when no one visits.\n4. Perfect for startups."
            },
            {
                id: "6-3",
                text: "Scalability: How to not crash when you go viral",
                tool: "Architecture",
                detail: "1. If one server handles 100 users, you need 1000 servers for 100k users.\n2. This is 'Horizontal Scaling'.\n3. Cloud providers do this automatically (Auto-scaling)."
            },
            {
                id: "6-4",
                text: "CI/CD: Robots that deploy your code automatically",
                tool: "GitHub Actions",
                detail: "1. You push code to GitHub.\n2. A robot runs your tests.\n3. If tests pass, it deploys to Vercel.\n4. You sleep while the robots work."
            }
        ],
        exam: [
            { question: "What does 'Serverless' mean?", options: ["No servers exist", "You don't manage the servers", "Broken internet", "Offline mode"], correctAnswer: 1 },
            { question: "What is a CDN?", options: ["Canadian Dollar Network", "Content Delivery Network", "Code Debug Node", "Central Data Number"], correctAnswer: 1 },
            { question: "What does CI/CD automate?", options: ["Coffee making", "Testing and deploying code", "Designing logos", "Writing emails"], correctAnswer: 1 },
            { question: "What is Latency?", options: ["Amount of data stored", "The delay before data transfer begins", "A programming language", "The speed of your keyboard"], correctAnswer: 1 },
            { question: "Which is a cloud provider?", options: ["Nike", "AWS", "Uber", "McDonald's"], correctAnswer: 1 }
        ]
    },
    {
        id: 7,
        title: "Level 7: The Founder 🦄 (Monetization)",
        description: "Turning code into cash. SaaS metrics, Marketing, and Exit Strategy.",
        color: "bg-fuchsia-700",
        sketchChallenge: "Draw a 'Funnel' (Traffic -> Signups -> Paid Users).",
        lingo: [
            { term: "SaaS", def: "Software as a Service. Paying a subscription for software." },
            { term: "Churn", def: "The percentage of subscribers who cancel their subscriptions." },
            { term: "MVP", def: "Minimum Viable Product. The simplest version of a product." }
        ],
        tasks: [
            {
                id: "7-1",
                text: "SaaS Metrics: MRR, Churn, and LTV (The holy numbers)",
                tool: "Business",
                detail: "1. MRR: Monthly Recurring Revenue (Rent money).\n2. Churn: How many people quit.\n3. LTV: How much one customer pays you in their lifetime.\n4. Knowing these allows you to spend money on ads."
            },
            {
                id: "7-2",
                text: "Payment Gateways: Stripe/PayPal Integration",
                tool: "Stripe",
                detail: "1. Create Stripe account.\n2. Get API Keys.\n3. Build 'Subscribe' button.\n4. Money lands in your bank account after 2 days."
            },
            {
                id: "7-3",
                text: "Marketing: SEO and getting your first 100 users",
                tool: "Growth",
                detail: "1. Build in public (Twitter/X).\n2. Write blog posts (SEO) so Google finds you.\n3. Cold email potential customers.\n4. The first 100 are the hardest."
            },
            {
                id: "7-4",
                text: "The Exit: Selling your app for millions",
                tool: "Acquire.com",
                detail: "1. If your app makes $10k/month, it's worth ~$300k.\n2. List it on Acquire.com.\n3. Buyers contact you.\n4. Sell, cash out, and buy your island (or next startup)."
            }
        ],
        exam: [
            { question: "What is MRR?", options: ["Monthly Recurring Revenue", "My Red Robot", "More Real Roads", "Money Run Rate"], correctAnswer: 0 },
            { question: "What is an MVP?", options: ["Most Valuable Player", "Minimum Viable Product", "Maximum Volume Processing", "Mobile Video Platform"], correctAnswer: 1 },
            { question: "What is 'Churn Rate'?", options: ["Speed of a butter churner", "Percentage of users who cancel", "The loading speed", "Amount of code written"], correctAnswer: 1 },
            { question: "What is SEO?", options: ["Super Easy Operation", "Search Engine Optimization", "Software Engineering Office", "Simple Email Output"], correctAnswer: 1 },
            { question: "What is LTV?", options: ["Live TV", "Lifetime Value of a customer", "Low Tech Version", "Large Text Volume"], correctAnswer: 1 }
        ]
    }
];

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
            { id: "0-1", text: "Computer: Get your laptop ready (Your command center)" },
            { id: "0-2", text: "Install VS Code: This is where we write the magic spells (code)", link: "https://code.visualstudio.com/" },
            { id: "0-3", text: "Extensions: Add 'Superpowers' to VS Code (Prettier, Live Server)" },
            { id: "0-4", text: "Browser: Install Chrome (Your window to the world)", link: "https://www.google.com/chrome/" },
            { id: "0-5", text: "Terminal: The black box hackers use (Don't worry, it's easy!)" },
            { id: "0-6", text: "Git: The 'Save Game' button for your code", link: "https://git-scm.com/" },
            { id: "0-7", text: "Node.js: The engine that runs your robots", link: "https://nodejs.org/" }
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
            { id: "1-1", text: "HTML Tags: The bricks of the web (<p>, <h1>, <button>)" },
            { id: "1-2", text: "Project: Build a 'Business Card' website for yourself" },
            { id: "1-3", text: "Images & Links: connecting your site to the world" },
            { id: "1-4", text: "Forms: How to let customers talk to you" },
            { id: "1-5", text: "Publishing: putting your site on the internet for FREE" }
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
            { id: "2-1", text: "CSS Basics: Changing colors, fonts, and sizes" },
            { id: "2-2", text: "The Box Model: Margins and Padding (Space is luxury)" },
            { id: "2-3", text: "Flexbox: Moving things around like Lego blocks" },
            { id: "2-4", text: "Responsive: Making it look great on iPhones and iPads" },
            { id: "2-5", text: "Project: Style your Business Card to look like Apple/Nike" }
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
            { id: "3-1", text: "Variables: Storing information (Like a backpack)" },
            { id: "3-2", text: "Functions: Creating your own magic spells" },
            { id: "3-3", text: "Events: Making things happen when you Click or Tap" },
            { id: "3-4", text: "Logic: If This, Then That (Teaching the computer to think)" },
            { id: "3-5", text: "Project: Build a 'Tip Calculator' app for restaurants" }
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
            { id: "4-1", text: "Components: Building reusable parts (Like Lego bricks)" },
            { id: "4-2", text: "State: Giving your app a memory" },
            { id: "4-3", text: "Vite: The super-fast engine for your apps" },
            { id: "4-4", text: "Polishing: Using Tailwind CSS for instant style" },
            { id: "4-5", text: "Project: Build a 'Search Engine' for movies" }
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
            { id: "5-1", text: "Databases: Where to keep all your customer info" },
            { id: "5-2", text: "API: Talking to other computers (like Stripe for money)" },
            { id: "5-3", text: "Authentication: Letting users Log In safely" },
            { id: "5-4", text: "Project: E-Commerce Store (Sell real products!)" },
            { id: "5-5", text: "Mobile: Turn your web store into a phone app" }
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
            { id: "6-1", text: "Cloud Providers: AWS, Google Cloud, Vercel" },
            { id: "6-2", text: "Serverless: Running code without managing servers" },
            { id: "6-3", text: "Scalability: How to not crash when you go viral" },
            { id: "6-4", text: "CI/CD: Robots that deploy your code automatically" }
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
            { id: "7-1", text: "SaaS Metrics: MRR, Churn, and LTV (The holy numbers)" },
            { id: "7-2", text: "Payment Gateways: Stripe/PayPal Integration" },
            { id: "7-3", text: "Marketing: SEO and getting your first 100 users" },
            { id: "7-4", text: "The Exit: Selling your app for millions" }
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

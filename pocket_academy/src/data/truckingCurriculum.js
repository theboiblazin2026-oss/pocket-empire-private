export const truckingCurriculumData = [
    {
        id: 0,
        title: "Level 0: The Blueprint 🏗️",
        description: "Before the wheels turn, the paperwork must align. Setting up your legal entity.",
        color: "bg-slate-600",
        sketchChallenge: "Draw your dream Company Logo! Keep it simple and strong.",
        lingo: [
            { term: "Authority", def: "The license from the government that says 'Yes, you can be a trucking company'." },
            { term: "Liability", def: "Who pays if you crash. (Spoiler: You want insurance to pay)." },
            { term: "Entity", def: "Your business as a 'person'. It can own things and get sued, protecting YOU." }
        ],
        tasks: [
            { id: "t0-1", text: "Business Name: Choose a name that sounds professional" },
            { id: "t0-2", text: "LLC Formation: Register with your Secretary of State" },
            { id: "t0-3", text: "EIN (Tax ID): Get your number from the IRS (Free)", link: "https://www.irs.gov/" },
            { id: "t0-4", text: "Business Bank Account: Keep money separate from personal" },
            { id: "t0-5", text: "DUNS Number: Build business credit profile", link: "https://www.dnb.com/duns-number/get-a-duns.html" }
        ],
        quiz: {
            question: "What is an EIN used for?",
            options: ["Driving License", "Tax Identification", "Ordering Pizza", "Radio Frequency"],
            correctAnswer: 1
        }
    },
    {
        id: 1,
        title: "Level 1: The Authority 👮",
        description: "Getting permission from the Feds to move freight.",
        color: "bg-blue-600",
        sketchChallenge: "Sketch the path of a truck crossing 3 state lines. Label the MC#.",
        lingo: [
            { term: "Interstate", def: "Driving between two or more states. Needs federal permission." },
            { term: "Intrastate", def: "Driving ONLY inside one state. simpler rules." },
            { term: "Process Agent", def: "A lawyer in every state who creates a 'mailbox' for you to get legal papers." }
        ],
        tasks: [
            { id: "t1-1", text: "USDOT Number: The main ID for your company", link: "https://www.fmcsa.dot.gov/registration" },
            { id: "t1-2", text: "MC Number (Operating Authority): Permission to cross state lines" },
            { id: "t1-3", text: "BOC-3 Filing: Process Agents (Legal requirement)" },
            { id: "t1-4", text: "UCR (Unified Carrier Registration): Pay your state fees", link: "https://plan.ucr.gov/" }
        ],
        quiz: {
            question: "What is an MC Number for?",
            options: ["Motorcycle Club", "Operating Authority (Interstate)", "McDonalds", "Music Cassette"],
            correctAnswer: 1
        }
    },
    {
        id: 2,
        title: "Level 2: The Shield 🛡️",
        description: "Protecting your business with Insurance and Compliance.",
        color: "bg-red-600",
        sketchChallenge: "Draw a 'Shield' protecting a truck from 'Liability' arrows.",
        lingo: [
            { term: "Premium", def: "The monthly bill you pay for insurance." },
            { term: "Deductible", def: "The money YOU pay before the insurance company pays a dime." },
            { term: "Cargo", def: "The stuff in the back of the truck. If you break it, you buy it (unless insured)." }
        ],
        tasks: [
            { id: "t2-1", text: "Liability Insurance: Required $750k minimum (Aim for $1M)" },
            { id: "t2-2", text: "Cargo Insurance: Protect what you haul ($100k standard)" },
            { id: "t2-3", text: "MCS-150 Update: Keep your DOT info current" },
            { id: "t2-4", text: "Drug & Alcohol Clearinghouse: Register your company", link: "https://clearinghouse.fmcsa.dot.gov/" }
        ],
        quiz: {
            question: "What is the standard minimum Liability Insurance?",
            options: ["$50,000", "$100,000", "$750,000", "$10,000,000"],
            correctAnswer: 2
        }
    },
    {
        id: 3,
        title: "Level 3: The Wheels 🚛",
        description: "Getting plates, stickers, and fuel taxes sorted.",
        color: "bg-yellow-600",
        sketchChallenge: "Draw the side of a truck cab and place the IFTA sticker where it belongs.",
        lingo: [
            { term: "Apportioned", def: "Splitting the cost of your license plate between all the states you drive in." },
            { term: "IFTA", def: "International Fuel Tax Agreement. A way to share gas tax money between states." },
            { term: "2290", def: "A special tax just for really heavy trucks (over 55,000 lbs)." }
        ],
        tasks: [
            { id: "t3-1", text: "IRP (Apportioned Plates): Run in multiple states" },
            { id: "t3-2", text: "IFTA (Fuel Tax): Setup your quarterly tax account" },
            { id: "t3-3", text: "Heavy Highway Tax (2290): Pay the IRS for heavy trucks" },
            { id: "t3-4", text: "State Permits: NY HUT, KY KYU, NM Weight Distance (if needed)" }
        ],
        quiz: {
            question: "What is IFTA related to?",
            options: ["Internet Access", "Fuel Taxes", "Food Safety", "Tire Pressure"],
            correctAnswer: 1
        }
    },
    {
        id: 4,
        title: "Level 4: The Hiring Gauntlet (Pre-Hire) 🕵️",
        description: "BEFORE they drive: The absolute must-haves for every driver applicant.",
        color: "bg-orange-600",
        sketchChallenge: "Draw a timeline of the last 10 years. Mark gaps in employment.",
        lingo: [
            { term: "MVR", def: "Motor Vehicle Record. The driver's report card." },
            { term: "Pre-Employment", def: "Anything that must happen BEFORE the driver touches the steering wheel." },
            { term: "Inquiry", def: "Asking a driver's old boss: 'Was he safe? Did he crash?'" }
        ],
        tasks: [
            { id: "t4-1", text: "Application for Employment: Must cover 10 years of work history" },
            { id: "t4-2", text: "CDL & Medical Card Copy: Verify they are valid and not expired" },
            { id: "t4-3", text: "MVR (Motor Vehicle Record): Pull from all states licensed in last 3 years" },
            { id: "t4-4", text: "Clearinghouse Full Query: Check for past drug/alcohol violations ($1.25 fee)" },
            { id: "t4-5", text: "Safety Performance History: Send inquiries to ALL DOT employers from last 3 years" },
            { id: "t4-6", text: "Pre-Employment Drug Test: Must have NEGATIVE result in hand before driving" }
        ],
        quiz: {
            question: "How many years of work history must the application cover?",
            options: ["1 year", "3 years", "5 years", "10 years"],
            correctAnswer: 3
        }
    },
    {
        id: 5,
        title: "Level 5: The DQ File (Onboarding) 📁",
        description: "The 'Holy Grail' of audit protection. This specific file must exist for every driver.",
        color: "bg-indigo-600",
        sketchChallenge: "Draw a file folder and label the 5 essential documents inside.",
        lingo: [
            { term: "DQ File", def: "Driver Qualification File. The master folder for one driver." },
            { term: "Medical Card", def: "A doctor's note saying the driver is healthy enough to drive a tank." },
            { term: "Onboarding", def: "The process of turning an 'Applicant' into an 'Employee'." }
        ],
        tasks: [
            { id: "t5-1", text: "Road Test Certificate: Must be signed by a qualified evaluator" },
            { id: "t5-2", text: "Medical Examiner's Certificate (MEC): Verify on the National Registry" },
            { id: "t5-3", text: "Annual List of Violations: Driver lists their tickets (or 'None') every year" },
            { id: "t5-4", text: "Annual MVR Review: You must review and sign off on their record yearly" },
            { id: "t5-5", text: "Policy Receipt: Driver signs they received Drug/Alcohol policy" }
        ],
        quiz: {
            question: "How often must you review a driver's MVR?",
            options: ["Every Week", "Every Month", "Once a Year (Annual)", "Never"],
            correctAnswer: 2
        }
    },
    {
        id: 6,
        title: "Level 6: Maintenance & Ops 🛠️",
        description: "Keeping the trucks running and the records straight.",
        color: "bg-teal-600",
        sketchChallenge: "Draw a dotted line connecting the Truck -> Mechanic -> Receipt -> File.",
        lingo: [
            { term: "DVIR", def: "Driver Vehicle Inspection Report. The daily 'Checklist' for the truck." },
            { term: "Preventative Maintenance", def: "Fixing things BEFORE they break (Oil changes, tire rotations)." },
            { term: "Consortium", def: "A random lottery for drug testing. You pay a company to manage it." }
        ],
        tasks: [
            { id: "t6-1", text: "DVIR (Inspection Reports): Keep for 3 months. Every day, every truck." },
            { id: "t6-2", text: "Maintenance Files: Keep records of all repairs/service for 12 months" },
            { id: "t6-3", text: "ELD Logs: Monitor Hours of Service daily. No cheating!" },
            { id: "t6-4", text: "Random Testing Pool: You MUST be enrolled in a consortium" }
        ],
        quiz: {
            question: "How long must you keep vehicle maintenance records?",
            options: ["1 month", "6 months", "12 months (1 year)", "Forever"],
            correctAnswer: 2
        }
    },
    {
        id: 7,
        title: "Level 7: The Empire (Growth) 💰",
        description: "Operations, funding, and scaling up.",
        color: "bg-purple-700",
        sketchChallenge: "Draw a map of the USA and circle your top 3 target lanes.",
        lingo: [
            { term: "Factoring", def: "Selling your invoice to get cash TODAY instead of waiting 30 days. You lose 3%." },
            { term: "Deadhead", def: "Driving with an EMPTY trailer. You are burning fuel and making $0." },
            { term: "Rate Con", def: "Rate Confirmation. The contract for one specific trip." }
        ],
        tasks: [
            { id: "t7-1", text: "Factoring Setup: Get paid next-day on your invoices" },
            { id: "t7-2", text: "Load Boards: DAT, Truckstop (Finding the money)" },
            { id: "t7-3", text: "Dispatcher Agreement: Clear terms if you hire help" },
            { id: "t7-4", text: "Rate Con Analysis: Read the fine print before signing!" }
        ],
        quiz: {
            question: "What document tells you how much a load pays?",
            options: ["The Bill of Lading", "The Rate Confirmation", "The Driver's License", "The Fuel Receipt"],
            correctAnswer: 1
        }
    },
    {
        id: 8,
        title: "Level 8: The Auditor (Survival) 🕵️‍♂️",
        description: "Surviving a New Entrant Safety Audit. Keep your license.",
        color: "bg-gray-800",
        sketchChallenge: "Draw a 'checkmark' for every Passed component (Driver, Vehicle, Accident).",
        lingo: [
            { term: "New Entrant", def: "A newbie trucking company (under 18 months old)." },
            { term: "Revocation", def: "The government cancelling your license. Game Over." },
            { term: "CAP", def: "Corrective Action Plan. Your apology letter if you fail an audit." }
        ],
        tasks: [
            { id: "t8-1", text: "Audit Invite: Respond immediately to the FMCSA letter" },
            { id: "t8-2", text: "Upload Portal: Learn how to upload PDFs to the safety portal" },
            { id: "t8-3", text: "CAP (Corrective Action Plan): How to fix mistakes if you fail" },
            { id: "t8-4", text: "Mock Audit: Audit yourself before they do" }
        ],
        quiz: {
            question: "What happens if you fail a Safety Audit?",
            options: ["You get a free lunch", "Your MC Authority is Revoked", "Nothing", "They give you a warning"],
            correctAnswer: 1
        }
    },
    {
        id: 9,
        title: "Level 9: The Fleet Mogul (Scaling) 🏢",
        description: "Moving from Owner-Op to CEO. Yards, Mechanics, and Dispatchers.",
        color: "bg-emerald-800",
        sketchChallenge: "Draw your future 10-acre Terminal Layout (Parking, Shop, Office).",
        lingo: [
            { term: "Terminal", def: "Your company HQ and parking yard." },
            { term: "Bobtail", def: "Driving a truck WITHOUT a trailer attached." },
            { term: "Lumper", def: "A person you hire just to unload the truck at the warehouse." }
        ],
        tasks: [
            { id: "t9-1", text: "Hiring a Dispatcher: Incentive-based pay structures" },
            { id: "t9-2", text: "Yard Lease: Legal parking for your growing fleet" },
            { id: "t9-3", text: "Fuel Cards: Saving 50 cents/gallon with fleet discounts" },
            { id: "t9-4", text: "IFTA Automation: Using GPS to calculate taxes instantly" }
        ],
        quiz: {
            question: "What is the biggest expense for a fleet?",
            options: ["Coffee", "Tires", "Fuel", "Office Paper"],
            correctAnswer: 2
        }
    }
];

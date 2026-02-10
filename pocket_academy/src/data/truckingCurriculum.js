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
            {
                id: "t0-1",
                text: "Business Name: Choose a name that sounds professional",
                tool: "Brainstorming",
                detail: "1. Google your name ideas to ensure they aren't taken.\n2. Check GoDaddy for the .com domain.\n3. Avoid names like 'Speedy' (implies unsafe) or 'Cheap' (implies low quality).\n4. Pick something solid: 'IronClad Logistics', 'Summit Freight'."
            },
            {
                id: "t0-2",
                text: "LLC Formation: Register with your Secretary of State",
                tool: "State Website",
                detail: "1. Go to your state's Secretary of State website.\n2. Look for 'Business Registration' or 'Articles of Organization'.\n3. File for an LLC (Limited Liability Company).\n4. Cost is usually $50-$200. This protects your personal house/car from lawsuits."
            },
            {
                id: "t0-3",
                text: "EIN (Tax ID): Get your number from the IRS (Free)",
                link: "https://www.irs.gov/",
                tool: "IRS.gov",
                detail: "1. Go to IRS.gov (ONLY .gov, never pay for this).\n2. Search 'Apply for EIN online'.\n3. Fill out the form as a 'Transportation' business.\n4. Download the PDF instantly. This is your business's Social Security Number."
            },
            {
                id: "t0-4",
                text: "Business Bank Account: Keep money separate from personal",
                tool: "Bank",
                detail: "1. Take your Articles of Organization and EIN to a bank (Chase, Wells Fargo, or online like Novo).\n2. Open a BUSINESS Checking account.\n3. Deposit $100.\n4. Never use this card for groceries. Business expenses only."
            },
            {
                id: "t0-5",
                text: "DUNS Number: Build business credit profile",
                link: "https://www.dnb.com/duns-number/get-a-duns.html",
                tool: "D&B",
                detail: "1. Go to dnb.com (Dun & Bradstreet).\n2. Apply for a free DUNS number.\n3. This is like a credit score for your business.\n4. It allows you to buy fuel and tires on credit later."
            }
        ],
        exam: [
            { question: "What is an EIN used for?", options: ["Driving License", "Tax Identification", "Ordering Pizza", "Radio Frequency"], correctAnswer: 1 },
            { question: "What type of entity protects your personal assets?", options: ["Sole Proprietorship", "LLC", "Nickname", "Social Club"], correctAnswer: 1 },
            { question: "Why do you need a separate bank account?", options: ["To look cool", "To separate business and personal finances", "To hide money", "It's optional"], correctAnswer: 1 },
            { question: "What is a DUNS number for?", options: ["Social media", "Building business credit", "Getting a CDL", "Fuel discounts"], correctAnswer: 1 },
            { question: "Where do you register an LLC?", options: ["The DMV", "Secretary of State", "The post office", "A truck stop"], correctAnswer: 1 }
        ]
    },
    {
        id: 1,
        title: "Level 1: The Authority 👮",
        description: "Getting permission from the Feds to move freight.",
        color: "bg-blue-600",
        sketchChallenge: "Sketch the path of a truck crossing 3 state lines. Label the MC#.",
        lingo: [
            { term: "Interstate", def: "Driving between two or more states. Needs federal permission." },
            { term: "Intrastate", def: "Driving ONLY inside one state. Simpler rules." },
            { term: "Process Agent", def: "A lawyer in every state who creates a 'mailbox' for you to get legal papers." }
        ],
        tasks: [
            {
                id: "t1-1",
                text: "USDOT Number: The main ID for your company",
                link: "https://www.fmcsa.dot.gov/registration",
                tool: "FMCSA Portal",
                detail: "1. Go to fmcsa.dot.gov.\n2. Click 'Register'.\n3. This number (USDOT #) tracks your safety score.\n4. It is free if obtained alone, but we need the MC number too."
            },
            {
                id: "t1-2",
                text: "MC Number (Operating Authority): Permission to cross state lines",
                tool: "FMCSA Portal",
                detail: "1. In the same application, select 'Interstate' and 'For-Hire'.\n2. Pay the $300 federal fee.\n3. You will get an MC# (Motor Carrier Number).\n4. NOTE: It will not be 'Active' yet. It sits in pending until you add insurance."
            },
            {
                id: "t1-3",
                text: "BOC-3 Filing: Process Agents (Legal requirement)",
                tool: "Service Provider",
                detail: "1. Google 'BOC-3 filing service'.\n2. Pay $25-$50 (one-time fee).\n3. They file a form designating a lawyer in every state to accept lawsuits for you.\n4. You cannot file this yourself; a provider must do it."
            },
            {
                id: "t1-4",
                text: "UCR (Unified Carrier Registration): Pay your state fees",
                link: "https://plan.ucr.gov/",
                tool: "UCR.gov",
                detail: "1. Go to plan.ucr.gov.\n2. Enter your DOT number.\n3. Pay the fee based on your fleet size (Usually ~$60 for 1-2 trucks).\n4. This money goes to the states to maintain roads."
            }
        ],
        exam: [
            { question: "What is an MC Number for?", options: ["Motorcycle Club", "Operating Authority (Interstate)", "McDonalds", "Music Cassette"], correctAnswer: 1 },
            { question: "What does USDOT stand for?", options: ["US Department of Travel", "US Department of Transportation", "United States Driving Office", "Universal System for Dispatching"], correctAnswer: 1 },
            { question: "What is a BOC-3?", options: ["A type of truck", "Process Agent filing", "A fuel type", "A trailer model"], correctAnswer: 1 },
            { question: "What is 'Interstate' driving?", options: ["Driving on one highway", "Driving between two or more states", "Driving in circles", "Driving at night only"], correctAnswer: 1 },
            { question: "What is UCR?", options: ["Universal Credit Report", "Unified Carrier Registration", "US Commercial Registry", "United Company Review"], correctAnswer: 1 }
        ]
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
            {
                id: "t2-1",
                text: "Liability Insurance: Required $750k minimum (Aim for $1M)",
                tool: "Insurance Broker",
                detail: "1. Call a commercial truck insurance broker.\n2. Ask for 'Auto Liability'.\n3. The law requires $750,000 coverage.\n4. Most brokers (loads) require $1,000,000. Get the million."
            },
            {
                id: "t2-2",
                text: "Cargo Insurance: Protect what you haul ($100k standard)",
                tool: "Insurance Broker",
                detail: "1. This covers the freight inside the trailer.\n2. Ask for $100,000 coverage (Standard).\n3. Ask for 'Reefer Breakdown' if you haul refrigerated goods.\n4. Without this, you cannot book decent loads."
            },
            {
                id: "t2-3",
                text: "MCS-150 Update: Keep your DOT info current",
                tool: "DOT Portal",
                detail: "1. Login to FMCSA portal.\n2. Update your 'MCS-150' form.\n3. Make sure your mileage and truck count are accurate.\n4. This must be done every 2 years (Biennial Update)."
            },
            {
                id: "t2-4",
                text: "Drug & Alcohol Clearinghouse: Register your company",
                link: "https://clearinghouse.fmcsa.dot.gov/",
                tool: "Clearinghouse",
                detail: "1. Go to clearinghouse.fmcsa.dot.gov.\n2. Register as an 'Employer'.\n3. Purchase a 'Query Plan' ($1.25 per query).\n4. You must check every driver here before hiring."
            }
        ],
        exam: [
            { question: "What is the minimum Liability Insurance?", options: ["$50,000", "$100,000", "$750,000", "$10,000,000"], correctAnswer: 2 },
            { question: "What is a 'Premium'?", options: ["A type of fuel", "Your monthly insurance payment", "A truck model", "A toll fee"], correctAnswer: 1 },
            { question: "What is a 'Deductible'?", options: ["Tax deduction", "Amount you pay before insurance kicks in", "A type of brake", "Discounted fuel"], correctAnswer: 1 },
            { question: "What does the MCS-150 form update?", options: ["Your fuel tax", "Your DOT registration info", "Your CDL", "Your insurance policy"], correctAnswer: 1 },
            { question: "What is the Drug & Alcohol Clearinghouse?", options: ["A pharmacy", "A federal database for drug/alcohol violations", "A gas station", "A medical clinic"], correctAnswer: 1 }
        ]
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
            {
                id: "t3-1",
                text: "IRP (Apportioned Plates): Run in multiple states",
                tool: "State DMV / IRP Office",
                detail: "1. Go to your state's IRP (International Registration Plan) office.\n2. Bring your Title, Insurance, and Lease.\n3. You will get an 'Apportioned' License Plate.\n4. This plate allows you to drive in all 48 lower states."
            },
            {
                id: "t3-2",
                text: "IFTA (Fuel Tax): Setup your quarterly tax account",
                tool: "State Comptroller",
                detail: "1. Applies if your truck is over 26,000 lbs.\n2. Register for IFTA with your state.\n3. You will get 2 ugly stickers for the side of your cab.\n4. You MUST file returns every quarter (Jan, Apr, Jul, Oct)."
            },
            {
                id: "t3-3",
                text: "Heavy Highway Tax (2290): Pay the IRS for heavy trucks",
                tool: "IRS / eFile",
                detail: "1. If your truck is 55,000+ lbs combined weight.\n2. File IRS Form 2290.\n3. Cost is ~$550 per year.\n4. You need the 'stamped Schedule 1' to get your plates."
            },
            {
                id: "t3-4",
                text: "State Permits: NY HUT, KY KYU, NM Weight Distance",
                tool: "State Portals",
                detail: "1. Some states want EXTRA money.\n2. New York: Get a HUT sticker.\n3. Kentucky: Get a KYU number.\n4. New Mexico: Register for Weight Distance tax.\n5. Oregon: Buy permits at the border or register monthly."
            }
        ],
        exam: [
            { question: "What is IFTA related to?", options: ["Internet Access", "Fuel Taxes", "Food Safety", "Tire Pressure"], correctAnswer: 1 },
            { question: "What is Form 2290 for?", options: ["Income tax", "Heavy Highway Vehicle Use Tax", "Sales tax", "Property tax"], correctAnswer: 1 },
            { question: "What does IRP stand for?", options: ["Interstate Road Pass", "International Registration Plan", "Instant Repair Permission", "Internal Revenue Processing"], correctAnswer: 1 },
            { question: "How often must IFTA taxes be filed?", options: ["Monthly", "Quarterly", "Annually", "Weekly"], correctAnswer: 1 },
            { question: "What does 'Apportioned' mean for plates?", options: ["One plate for all states", "Cost split across states you drive in", "Free plates", "Temporary plates"], correctAnswer: 1 }
        ]
    },
    {
        id: 4,
        title: "Level 4: The Hiring Gauntlet 🕵️",
        description: "BEFORE they drive: The absolute must-haves for every driver applicant.",
        color: "bg-orange-600",
        sketchChallenge: "Draw a timeline of the last 10 years. Mark gaps in employment.",
        lingo: [
            { term: "MVR", def: "Motor Vehicle Record. The driver's report card." },
            { term: "Pre-Employment", def: "Anything that must happen BEFORE the driver touches the steering wheel." },
            { term: "Inquiry", def: "Asking a driver's old boss: 'Was he safe? Did he crash?'" }
        ],
        tasks: [
            {
                id: "t4-1",
                text: "Application for Employment: Must cover 10 years of work history",
                tool: "Paper/PDF Form",
                detail: "1. The driver MUST fill out a detailed application.\n2. It must list 10 years of work history.\n3. Any gaps (unemployed periods) must be explained in writing."
            },
            {
                id: "t4-2",
                text: "CDL & Medical Card Copy: Verify they are valid and not expired",
                tool: "Camera/Scan",
                detail: "1. Take a picture of the front and back of their CDL.\n2. Take a picture of their Medical Examiner's Certificate (Med Card).\n3. Check the expiration dates. If expired, they cannot drive."
            },
            {
                id: "t4-3",
                text: "MVR (Motor Vehicle Record): Pull from all states licensed in last 3 years",
                tool: "Background Check Service",
                detail: "1. Order an MVR from the state DMV.\n2. Look for speeding tickets, reckless driving, or DUIs.\n3. You need MVRs from EVERY state they held a license in for the past 3 years."
            },
            {
                id: "t4-4",
                text: "Clearinghouse Full Query: Check for past drug/alcohol violations",
                tool: "Clearinghouse",
                detail: "1. Log in to Clearinghouse.\n2. Run a 'Pre-Employment Full Query'.\n3. The driver must login to their account to 'Consent'.\n4. If it shows a violation, DO NOT HIRE."
            },
            {
                id: "t4-5",
                text: "Safety Performance History: Send inquiries to ALL DOT employers from last 3 years",
                tool: "Fax / Email",
                detail: "1. Send a form to their previous trucking companies.\n2. Ask: 'Did he crash? Did he fail a drug test?'\n3. Keep the fax receipt or email proof that you tried to ask."
            },
            {
                id: "t4-6",
                text: "Pre-Employment Drug Test: Must have NEGATIVE result in hand before driving",
                tool: "LabCorp / Quest",
                detail: "1. Send the driver to a clinic for a urine test.\n2. Wait for the Medical Review Officer (MRO) to send results.\n3. Result must say 'NEGATIVE'.\n4. Only THEN can they drive."
            }
        ],
        exam: [
            { question: "How many years of work history must the application cover?", options: ["1 year", "3 years", "5 years", "10 years"], correctAnswer: 3 },
            { question: "What is an MVR?", options: ["Motor Vehicle Record", "Manual Vehicle Registration", "Monthly Vehicle Report", "Minimum Voltage Required"], correctAnswer: 0 },
            { question: "When must a drug test result be available?", options: ["After 30 days of driving", "Before the driver starts driving", "At the end of the year", "Only if there's an accident"], correctAnswer: 1 },
            { question: "How many years back must you check Safety Performance History?", options: ["1 year", "3 years", "5 years", "10 years"], correctAnswer: 1 },
            { question: "What is the Clearinghouse?", options: ["A bank", "A federal database for drug/alcohol violations", "A warehouse", "A dispatch service"], correctAnswer: 1 }
        ]
    },
    {
        id: 5,
        title: "Level 5: The DQ File 📁",
        description: "The 'Holy Grail' of audit protection. This file must exist for every driver.",
        color: "bg-indigo-600",
        sketchChallenge: "Draw a file folder and label the 5 essential documents inside.",
        lingo: [
            { term: "DQ File", def: "Driver Qualification File. The master folder for one driver." },
            { term: "Medical Card", def: "A doctor's note saying the driver is healthy enough to drive a tank." },
            { term: "Onboarding", def: "The process of turning an 'Applicant' into an 'Employee'." }
        ],
        tasks: [
            {
                id: "t5-1",
                text: "Road Test Certificate: Must be signed by a qualified evaluator",
                tool: "Truck / Form",
                detail: "1. Take the driver on a test drive.\n2. Fill out a Road Test form (Pre-trip, Braking, Turning).\n3. You (or a lead driver) signs it as the evaluator.\n4. File it."
            },
            {
                id: "t5-2",
                text: "Medical Examiner's Certificate (MEC): Verify on the National Registry",
                tool: "National Registry Website",
                detail: "1. Go to the National Registry of Certified Medical Examiners.\n2. Enter the doctor's ID from the med card.\n3. Verify the doctor is real.\n4. Print the verification and staple it to the med card."
            },
            {
                id: "t5-3",
                text: "Annual List of Violations: Driver lists their tickets (or 'None') every year",
                tool: "Form",
                detail: "1. Once a year, give the driver a form.\n2. They list all traffic tickets they got in the last 12 months.\n3. If none, they write 'NONE'.\n4. They sign it."
            },
            {
                id: "t5-4",
                text: "Annual MVR Review: You must review and sign off on their record yearly",
                tool: "MVR Report",
                detail: "1. Once a year, pull a new MVR.\n2. Compare it to their List of Violations.\n3. Fill out a 'Review of Driving Record' form.\n4. Decide if they are still safe to employ."
            },
            {
                id: "t5-5",
                text: "Policy Receipt: Driver signs they received Drug/Alcohol policy",
                tool: "Company Handbook",
                detail: "1. Give driver your Drug & Alcohol Policy handbook.\n2. Have them sign a receipt saying 'I received this'.\n3. Keep the receipt forever."
            }
        ],
        exam: [
            { question: "How often must you review a driver's MVR?", options: ["Every Week", "Every Month", "Once a Year", "Never"], correctAnswer: 2 },
            { question: "What is a DQ File?", options: ["Dairy Queen File", "Driver Qualification File", "Digital Query File", "Dispatch Queue File"], correctAnswer: 1 },
            { question: "Who must sign the Road Test Certificate?", options: ["The driver", "A qualified evaluator", "The DMV", "Anyone"], correctAnswer: 1 },
            { question: "What is the Annual List of Violations?", options: ["A list of company rules", "Driver's self-reported tickets/violations", "A maintenance log", "Insurance claims"], correctAnswer: 1 },
            { question: "What must a driver sign a receipt for?", options: ["Fuel cards", "Drug/Alcohol policy", "Company merchandise", "Vacation days"], correctAnswer: 1 }
        ]
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
            {
                id: "t6-1",
                text: "DVIR (Inspection Reports): Keep for 3 months.",
                tool: "ELD / Paper Log",
                detail: "1. Every day, driver inspects the truck.\n2. They mark 'No Defects' or list issues.\n3. If issues listed, mechanic must sign that it's fixed.\n4. Keep these reports for 3 months."
            },
            {
                id: "t6-2",
                text: "Maintenance Files: Keep records of all repairs/service for 12 months",
                tool: "File Cabinet",
                detail: "1. Every truck needs its own folder.\n2. Put every oil change, tire receipt, and repair invoice in it.\n3. Create a list of when next service is due.\n4. Keep records for 12 months."
            },
            {
                id: "t6-3",
                text: "ELD Logs: Monitor Hours of Service daily. No cheating!",
                tool: "KeepTruckin / Motive",
                detail: "1. Drivers use an ELD (Electronic Logging Device).\n2. They can drive 11 hours max.\n3. They must take a 30-min break.\n4. You must login as admin and check for 'Unassigned Driving' or violations."
            },
            {
                id: "t6-4",
                text: "Random Testing Pool: You MUST be enrolled in a consortium",
                tool: "Consortium Provider",
                detail: "1. Pay a 3rd party (Consortium) to manage random testing.\n2. They put your drivers in a big lottery pool.\n3. If selected, driver must go test immediately.\n4. This is mandatory by law."
            }
        ],
        exam: [
            { question: "How long must you keep maintenance records?", options: ["1 month", "6 months", "12 months", "Forever"], correctAnswer: 2 },
            { question: "What is a DVIR?", options: ["A type of truck", "Daily Vehicle Inspection Report", "Digital Video Recording", "Driver Vacation Request"], correctAnswer: 1 },
            { question: "How long must DVIRs be kept?", options: ["1 week", "3 months", "1 year", "5 years"], correctAnswer: 1 },
            { question: "What is an ELD?", options: ["Electric Light Display", "Electronic Logging Device", "Emergency Location Detector", "Engine Load Distributor"], correctAnswer: 1 },
            { question: "What is a Consortium for?", options: ["Fuel buying", "Random drug testing management", "Load booking", "Truck washing"], correctAnswer: 1 }
        ]
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
            {
                id: "t7-1",
                text: "Factoring Setup: Get paid next-day on your invoices",
                tool: "Factoring Company",
                detail: "1. Brokers take 30-60 days to pay you.\n2. Factoring companies pay you tomorrow, but take 3%.\n3. Send them your Rate Con and BOL (Bill of Lading).\n4. Essential for cash flow when starting."
            },
            {
                id: "t7-2",
                text: "Load Boards: DAT, Truckstop (Finding the money)",
                tool: "Website / App",
                detail: "1. Subscribe to DAT Power or Truckstop.com.\n2. Search for loads (e.g. Dallas to Atlanta).\n3. Call the broker. Negotiate the rate.\n4. This is the stock market of trucking."
            },
            {
                id: "t7-3",
                text: "Dispatcher Agreement: Clear terms if you hire help",
                tool: "Contract",
                detail: "1. If you hire a dispatcher, sign an agreement.\n2. Define their fee (usually 5-10% of gross).\n3. Define who talks to the broker.\n4. Verify they represent YOU, not the broker."
            },
            {
                id: "t7-4",
                text: "Rate Con Analysis: Read the fine print before signing!",
                tool: "PDF Reader",
                detail: "1. Open the PDF (Preview on Mac, Edge/Adobe on Windows).\n2. Check the Rate: Is it what you agreed?\n3. Check the Address: Is it correct?\n4. Check 'Lumper Fees': Will they reimburse you?\n5. Check 'Detention': Do they pay if you wait 5 hours?"
            }
        ],
        exam: [
            { question: "What document tells you how much a load pays?", options: ["The Bill of Lading", "The Rate Confirmation", "The Driver's License", "The Fuel Receipt"], correctAnswer: 1 },
            { question: "What is Factoring?", options: ["Math homework", "Getting paid early by selling invoices", "A type of insurance", "Truck maintenance"], correctAnswer: 1 },
            { question: "What is Deadheading?", options: ["A concert", "Driving with an empty trailer", "Sleeping in the cab", "A toll road"], correctAnswer: 1 },
            { question: "What are DAT and Truckstop?", options: ["Gas stations", "Load boards for finding freight", "Insurance companies", "Truck dealerships"], correctAnswer: 1 },
            { question: "Why is reading the Rate Con important?", options: ["It has jokes", "To understand pay, pickup/delivery details, and terms", "It's optional", "For entertainment"], correctAnswer: 1 }
        ]
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
            {
                id: "t8-1",
                text: "Audit Invite: Respond immediately to the FMCSA letter",
                tool: "Mail / Email",
                detail: "1. Within first 12 months, you WILL get audited.\n2. They send a letter.\n3. Do not hide. Log in to the portal immediately.\n4. You usually have 30 days to upload documents."
            },
            {
                id: "t8-2",
                text: "Upload Portal: Learn how to upload PDFs to the safety portal",
                tool: "FMCSA New Entrant Portal",
                detail: "1. Convert your DQ Files, Maintenance Files, and Logs to PDF.\n2. Use 'Print to PDF' (Ctrl+P on Windows, Cmd+P on Mac).\n3. Group them clearly (e.g., 'Driver A - DQ File').\n4. Upload to the official New Entrant portal."
            },
            {
                id: "t8-3",
                text: "CAP (Corrective Action Plan): How to fix mistakes if you fail",
                tool: "Word Doc",
                detail: "1. If you fail, you aren't shut down YET.\n2. You must write a CAP.\n3. Say: 'I messed up X. I have fixed it by doing Y. I will prevent it by doing Z.'\n4. Submit and pray."
            },
            {
                id: "t8-4",
                text: "Mock Audit: Audit yourself before they do",
                tool: "Checklist",
                detail: "1. Download a 'New Entrant Safety Audit Checklist'.\n2. Go through your own files.\n3. Is the Medical Card expired? Is the MVR there?\n4. Fix it NOW, not when the auditor is watching."
            }
        ],
        exam: [
            { question: "What happens if you fail a Safety Audit?", options: ["Free lunch", "Your MC Authority is Revoked", "Nothing", "A warning"], correctAnswer: 1 },
            { question: "What is a CAP?", options: ["A hat", "Corrective Action Plan", "Commercial Authority Permit", "Cargo Assessment Protocol"], correctAnswer: 1 },
            { question: "How long is a 'New Entrant' period?", options: ["6 months", "12 months", "18 months", "24 months"], correctAnswer: 2 },
            { question: "What should you do when you get an audit letter?", options: ["Ignore it", "Respond immediately", "Call a lawyer first", "Throw it away"], correctAnswer: 1 },
            { question: "What is a Mock Audit?", options: ["A fake test", "Auditing yourself before the real one", "An FMCSA visit", "A truck inspection"], correctAnswer: 1 }
        ]
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
            {
                id: "t9-1",
                text: "Hiring a Dispatcher: Incentive-based pay structures",
                tool: "Compensation Plan",
                detail: "1. Don't just pay hourly.\n2. Pay base + % of Gross Revenue.\n3. If trucks make more, dispatcher makes more.\n4. Align your incentives."
            },
            {
                id: "t9-2",
                text: "Yard Lease: Legal parking for your growing fleet",
                tool: "Commercial Real Estate",
                detail: "1. You can't park 10 trucks at your house.\n2. Lease an industrial lot (IOS - Industrial Outdoor Storage).\n3. Ensure it is zoned for trucking.\n4. Install cameras and fencing."
            },
            {
                id: "t9-3",
                text: "Fuel Cards: Saving 50 cents/gallon with fleet discounts",
                tool: "Wex / Pilot Apex",
                detail: "1. Sign up for a Fleet Fuel Card (e.g. Apex, NASTC).\n2. Using a regular credit card is throwing money away.\n3. Save $0.40 - $0.80 per gallon at big stops.\n4. That's $10,000s per year in savings."
            },
            {
                id: "t9-4",
                text: "IFTA Automation: Using GPS to calculate taxes instantly",
                tool: "Samsara / Motive",
                detail: "1. Stop calculating miles manually.\n2. Uses your ELD/GPS provider's IFTA report.\n3. It tracks every mile in every state automatically.\n4. Upload the CSV to the state website. Done."
            }
        ],
        exam: [
            { question: "What is the biggest expense for a fleet?", options: ["Coffee", "Tires", "Fuel", "Office Paper"], correctAnswer: 2 },
            { question: "What is Bobtailing?", options: ["Fishing", "Driving a truck without a trailer", "Backing up", "Sleeping in the cab"], correctAnswer: 1 },
            { question: "What is a Lumper?", options: ["A speed bump", "Person hired to unload freight", "A type of fuel", "A dispatcher"], correctAnswer: 1 },
            { question: "What is a Terminal in trucking?", options: ["An airport gate", "Company HQ and parking yard", "A computer screen", "End of a route"], correctAnswer: 1 },
            { question: "Why use fuel cards?", options: ["For fun", "Fleet discounts of 30-50 cents per gallon", "They're required by law", "For toll payment only"], correctAnswer: 1 }
        ]
    }
];

import discord
import os
import subprocess
import asyncio
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# CONFIGURATION
TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_USER_ID = int(os.getenv("DISCORD_USER_ID", "0"))

if not TOKEN:
    print("❌ SECURITY ERROR: No DISCORD_TOKEN found in .env or environment.")
    print("👉 Action: Create a .env file with: DISCORD_TOKEN=your_token_here")
    exit(1)

if ALLOWED_USER_ID == 0:
    print("⚠️ SETUP MODE: DISCORD_USER_ID is not set.")
    print("👉 Send a message to the bot to see your User ID.")
else:
    print("🔒 Security Protocol: Active")
    print(f"🔒 Listening only to User ID: {ALLOWED_USER_ID}")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Pocket Jarvis is online as {client.user}')

@client.event
async def on_message(message):
    # Ignore self
    if message.author == client.user:
        return

    # Setup Mode: Tell user their ID
    if ALLOWED_USER_ID == 0:
        print(f"👋 Setup Mode: Message received from User ID: {message.author.id}")
        await message.channel.send(f"⚠️ **Setup Mode**\nYour User ID is: `{message.author.id}`\nPlease add this to your configuration to lock the bot.")
        return

    # Security Check
    if message.author.id != ALLOWED_USER_ID:
        # Ignore unauthorized users
        return

    msg = message.content

    if msg.startswith('!ping'):
        await message.channel.send('Pong! 🏓 System is online.')

    if msg.startswith('!status'):
        # Check load avg
        load = os.getloadavg()
        await message.channel.send(f"💻 System Load: {load[0]} (1 min), {load[1]} (5 min)")

    if msg.startswith('!exec'):
        # DANGER: Runs shell commands. Only for allowed user.
        command = msg[6:]
        await message.channel.send(f"⚙️ Running: `{command}`...")
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            output = result.stdout[:1900] # Discord limit is 2000 chars
            if not output:
                 output = "[No Output]"
            
            await message.channel.send(f"```bash\n{output}\n```")
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    # ========== COMPLIANCE OFFICER COMMANDS ==========
    
    if msg.startswith('!check '):
        # Single MC/DOT lookup: !check MC:12345 or !check DOT:987654
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_compliance', 'tools'))
        from monitor import get_carrier_status
        
        query = msg[7:].strip()
        await message.channel.send(f"🔍 Looking up `{query}`...")
        
        # Parse TYPE:ID format
        if ":" in query:
            id_type, identifier = query.split(":", 1)
            search_type = "USDOT" if id_type.upper() == "DOT" else "MC_MX"
        else:
            identifier = query
            search_type = "MC_MX"
        
        try:
            data = get_carrier_status(identifier, search_type=search_type)
            
            if "error" in data:
                await message.channel.send(f"❌ Error: {data['error']}")
            else:
                embed = discord.Embed(title=f"🛡️ {data['legal_name']}", color=0x00FF00 if data['status'] == 'ACTIVE' else 0xFF0000)
                embed.add_field(name="Status", value=data['status'], inline=True)
                embed.add_field(name="Safety Rating", value=data['rating'], inline=True)
                embed.add_field(name="Query", value=query, inline=False)
                await message.channel.send(embed=embed)
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    # ========== LEAD QUALIFIER COMMANDS ==========
    
    if msg.startswith('!score '):
        # Score a lead by MC or DOT number
        identifier = msg[7:].strip()
        
        if not identifier:
            await message.channel.send("⚠️ Usage: `!score MC123456` or `!score DOT1234567`")
            return
        
        await message.channel.send(f"🔍 Scoring lead: **{identifier}**...")
        
        try:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_leads'))
            from lead_manager import score_by_identifier
            
            result = score_by_identifier(identifier)
            
            if "error" in result:
                await message.channel.send(f"❌ {result['error']}")
            else:
                score = result['score']
                risk_level = result['risk_level']
                risk_emoji = result['risk_emoji']
                carrier = result.get('carrier_data', {})
                
                # Build embed
                if score >= 70:
                    color = 0x27ae60  # Green
                elif score >= 50:
                    color = 0xf39c12  # Yellow
                else:
                    color = 0xe74c3c  # Red
                
                embed = discord.Embed(
                    title=f"{risk_emoji} {risk_level} - Score: {score}/100",
                    description=f"**{carrier.get('legal_name', 'Unknown')}**",
                    color=color
                )
                
                embed.add_field(name="DOT#", value=carrier.get('dot_number', 'N/A'), inline=True)
                embed.add_field(name="MC#", value=carrier.get('mc_number', 'N/A'), inline=True)
                embed.add_field(name="Status", value=carrier.get('status', 'Unknown'), inline=True)
                embed.add_field(name="Safety Rating", value=carrier.get('safety_rating', 'None'), inline=True)
                embed.add_field(name="Power Units", value=str(carrier.get('power_units', 0)), inline=True)
                embed.add_field(name="Drivers", value=str(carrier.get('drivers', 0)), inline=True)
                
                # Breakdown (truncated)
                breakdown_text = "\n".join(result.get('breakdown', [])[:5])
                embed.add_field(name="📊 Breakdown", value=breakdown_text or "N/A", inline=False)
                
                await message.channel.send(embed=embed)
                
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    # ========== RATE NEGOTIATOR COMMANDS ==========
    
    if msg.startswith('!rate '):
        # Look up lane rate stats
        parts = msg[6:].strip()
        
        # Try to parse "origin to destination" or "origin destination"
        if ' to ' in parts.lower():
            split_parts = parts.lower().split(' to ')
            origin = split_parts[0].strip()
            destination = split_parts[1].strip()
        else:
            # Try splitting by spaces (first half origin, second half dest)
            words = parts.split()
            mid = len(words) // 2
            origin = ' '.join(words[:mid])
            destination = ' '.join(words[mid:])
        
        await message.channel.send(f"📊 Looking up rates: **{origin}** → **{destination}**...")
        
        try:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_rates'))
            from rate_manager import get_lane_stats
            
            stats = get_lane_stats(origin, destination)
            
            if not stats:
                await message.channel.send(f"📭 No rate history for this lane. Log rates in the Rate Negotiator dashboard!")
            else:
                embed = discord.Embed(
                    title=f"💰 {stats['lane']}",
                    color=0x3498db
                )
                embed.add_field(name="Avg Rate", value=f"${stats['avg_rate']:,.0f}", inline=True)
                embed.add_field(name="Rate/Mile", value=f"${stats['avg_rpm']:.2f}" if stats['avg_rpm'] else "N/A", inline=True)
                embed.add_field(name="Range", value=f"${stats['min_rate']:,.0f} - ${stats['max_rate']:,.0f}", inline=True)
                embed.add_field(name="Quotes", value=str(stats['total_quotes']), inline=True)
                embed.add_field(name="Accepted", value=f"{stats['acceptance_rate']}%", inline=True)
                if stats.get('trend'):
                    embed.add_field(name="Trend", value=stats['trend'], inline=True)
                
                await message.channel.send(embed=embed)
                
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")
    
    if msg.startswith('!negotiate '):
        # Generate negotiation script
        parts = msg[11:].strip()
        
        # Parse: origin to destination rate [miles]
        import re
        match = re.match(r'(.+?)\s+to\s+(.+?)\s+(\d+(?:\.\d+)?)\s*(\d+)?', parts, re.IGNORECASE)
        
        if not match:
            await message.channel.send("⚠️ Usage: `!negotiate Chicago to Miami 1800` or `!negotiate Chicago to Miami 1800 1200`")
            return
        
        origin = match.group(1).strip()
        destination = match.group(2).strip()
        offered_rate = float(match.group(3))
        miles = int(match.group(4)) if match.group(4) else None
        
        await message.channel.send(f"📝 Generating script for **{origin}** → **{destination}** at ${offered_rate:,.0f}...")
        
        try:
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_rates'))
            from rate_manager import generate_negotiation_script
            
            scripts = generate_negotiation_script(origin, destination, offered_rate, miles)
            
            for script in scripts:
                if "LOWBALL" in script["type"] or "BELOW" in script["type"]:
                    color = 0xe74c3c  # Red
                elif "GOOD" in script["type"]:
                    color = 0x27ae60  # Green
                else:
                    color = 0xf39c12  # Yellow
                
                embed = discord.Embed(title=script["type"], description=script["message"], color=color)
                embed.add_field(name="📜 Script", value=script["script"][:1000], inline=False)
                
                await message.channel.send(embed=embed)
                
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    if msg.startswith('!compliance'):
        # Run full compliance scan
        await message.channel.send("🔍 Running full compliance scan... (this may take a moment)")
        
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
            venv_python = os.path.join(project_root, ".venv", "bin", "python3")
            script = os.path.join(project_root, "pocket_compliance", "run_compliance.py")
            
            result = subprocess.run([venv_python, script], capture_output=True, text=True, timeout=120)
            output = result.stdout[:1800] if result.stdout else "[No Output]"
            await message.channel.send(f"```\n{output}\n```")
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    # ========== CREDIT REPAIR SPECIALIST COMMANDS ==========
    
    if msg.startswith('!credit'):
        # Run Credit Wizard and return results
        await message.channel.send("🧙‍♂️ Running Credit Repair Wizard...")
        
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
            venv_python = os.path.join(project_root, ".venv", "bin", "python3")
            script = os.path.join(project_root, "pocket_credit", "run_credit_wizard.py")
            output_dir = os.path.join(project_root, "pocket_credit", "output_letters")
            
            # Get list of existing files before running
            import glob
            before_files = set(glob.glob(os.path.join(output_dir, "*.docx")))
            
            # Run the wizard
            result = subprocess.run([venv_python, script], capture_output=True, text=True, timeout=120, cwd=project_root)
            output = result.stdout[:1500] if result.stdout else "[No Output]"
            
            # Check for new files
            after_files = set(glob.glob(os.path.join(output_dir, "*.docx")))
            new_files = after_files - before_files
            
            await message.channel.send(f"```\n{output}\n```")
            
            # Send any new files
            for filepath in new_files:
                try:
                    await message.channel.send(f"📎 **Generated Letter:**", file=discord.File(filepath))
                except Exception as e:
                    await message.channel.send(f"📎 New letter at: `{filepath}`\n(File too large to send via Discord)")
                    
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    # ========== REMINDER BOT COMMANDS ==========
    
    if msg.startswith('!remind '):
        # Add reminder: !remind [category] [date] [title]
        # Examples: !remind bills 2/15 Pay electric bill
        #           !remind renewals 3/1/2026 monthly CDL medical renewal
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_reminders'))
        from reminder_manager import add_reminder, format_reminder
        
        try:
            parts = msg[8:].strip().split(' ', 2)
            if len(parts) < 3:
                await message.channel.send("❌ Usage: `!remind [category] [date] [title]`\nCategories: bills, renewals, inspections, personal\nExample: `!remind bills 2/15 Pay electric bill`")
                return
            
            category, date_str, title = parts
            
            # Check for recurring keyword at end
            recurring = None
            for rec in ['yearly', 'monthly', 'weekly', 'daily']:
                if title.lower().endswith(rec):
                    recurring = rec
                    title = title[:-len(rec)].strip()
                    break
            
            reminder = add_reminder(title, date_str, category, recurring)
            
            await message.channel.send(f"✅ Reminder added!\n{format_reminder(reminder)}")
            
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}\nUsage: `!remind [category] [date] [title]`")

    if msg == '!bills' or msg.startswith('!bills'):
        # Show upcoming bills
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_reminders'))
        from reminder_manager import get_reminders, get_monthly_bills_total
        from datetime import datetime, timedelta
        
        reminders = get_reminders()
        bills = [r for r in reminders if r.get('category', '').lower() == 'bill']
        
        if not bills:
            await message.channel.send("💰 No bills tracked yet. Add with `!remind bill 2026-02-15 Electric Bill $150`")
        else:
            # Sort by due date
            today = datetime.now()
            upcoming = []
            overdue = []
            
            for bill in bills:
                try:
                    due = datetime.fromisoformat(bill['due_date'])
                    bill['_due'] = due
                    if due < today:
                        overdue.append(bill)
                    else:
                        upcoming.append(bill)
                except:
                    upcoming.append(bill)
            
            upcoming.sort(key=lambda x: x.get('_due', today))
            
            embed = discord.Embed(title="💰 Bills Overview", color=0x2ecc71)
            
            # Monthly total
            monthly_total = get_monthly_bills_total()
            embed.add_field(name="📊 Monthly Total", value=f"${monthly_total:,.2f}", inline=False)
            
            # Overdue
            if overdue:
                overdue_text = "\n".join([f"🔴 {b['title']} (${b.get('amount', 0):,.2f})" for b in overdue[:5]])
                embed.add_field(name="⚠️ Overdue", value=overdue_text, inline=False)
            
            # Upcoming (next 5)
            if upcoming:
                upcoming_text = "\n".join([
                    f"📅 {b['_due'].strftime('%m/%d')} - {b['title']} (${b.get('amount', 0):,.2f})" 
                    for b in upcoming[:5]
                ])
                embed.add_field(name="📆 Upcoming", value=upcoming_text, inline=False)
            
            await message.channel.send(embed=embed)


    if msg == '!news':
        # News Briefing
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_news'))
        from news_manager import generate_daily_briefing
        
        await message.channel.send("📰 Fetching latest news...")
        briefing = generate_daily_briefing()
        
        # Split if too long
        if len(briefing) > 1900:
            parts = [briefing[i:i+1900] for i in range(0, len(briefing), 1900)]
            for part in parts:
                await message.channel.send(part)
        else:
            await message.channel.send(briefing)

    if msg.startswith('!invoice '):
        # Invoice Lookup: !invoice 1001
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_invoices'))
        from invoice_manager import get_invoices
        
        try:
            inv_num = int(msg[9:].strip())
            invoices = get_invoices()
            target = next((i for i in invoices if i['invoice_number'] == inv_num), None)
            
            if target:
                status_emoji = "✅" if target['status'] == 'paid' else "⏳"
                embed = discord.Embed(title=f"{status_emoji} Invoice #{inv_num}", color=0x00FF00 if target['status'] == 'paid' else 0xFFAA00)
                embed.add_field(name="Client", value=target['client']['name'], inline=False)
                embed.add_field(name="Amount", value=f"${target['total']:,.2f}", inline=True)
                embed.add_field(name="Due Date", value=target['due_date'][:10], inline=True)
                embed.add_field(name="Status", value=target['status'].upper(), inline=True)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"❌ Invoice #{inv_num} not found.")
        except ValueError:
            await message.channel.send("❌ Usage: `!invoice [invoice_number]`")
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    if msg.startswith('!route '):
        # Route Estimate: !route Chicago, IL to Miami, FL semi
        try:
            parts = msg[7:].split(' to ')
            if len(parts) < 2:
                await message.channel.send("⚠️ Usage: `!route Origin to Destination [vehicle]`")
                return
            
            origin = parts[0].strip()
            remainder = parts[1].strip()
            
            # extract vehicle if present
            vehicle = "semi_80k" # default
            dest = remainder
            
            import sys
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_router'))
            from route_manager import VEHICLES, estimate_route
            
            # Check for vehicle keywords (handle multi-word patterns)
            remainder_lower = remainder.lower()
            import re  # Move import to top of this block
            
            # Order matters - check longer patterns first
            if 'cdl hot shot' in remainder_lower or 'cdl hotshot' in remainder_lower:
                vehicle = 'hotshot_cdl'
                dest = re.sub(r'\s*(cdl\s+hot\s*shot|cdl\s+hotshot)\s*$', '', remainder, flags=re.IGNORECASE).strip()
            elif 'non-cdl' in remainder_lower or 'noncdl' in remainder_lower or 'non cdl' in remainder_lower:
                vehicle = 'hotshot_noncdl'
                dest = re.sub(r'\s*(non-?cdl\s*hot\s*shot|non-?cdl)\s*$', '', remainder, flags=re.IGNORECASE).strip()
            elif 'hotshot' in remainder_lower or 'hot shot' in remainder_lower:
                vehicle = 'hotshot_cdl'  # Default hotshot to CDL version
                dest = re.sub(r'\s*(hot\s*shot)\s*$', '', remainder, flags=re.IGNORECASE).strip()
            elif remainder_lower.endswith('semi'):
                vehicle = 'semi_80k'
                dest = remainder[:-4].strip()
            elif remainder_lower.endswith('car'):
                vehicle = 'car'
                dest = remainder[:-3].strip()

            
            await message.channel.send(f"🚛 Calculating route: **{origin}** ➡️ **{dest}** ({VEHICLES[vehicle]['name']})...")
            
            # Use Geocoding + OSRM (Simplified for Discord command - direct estimate if API fails or just nice display)
            # For resilience, we'll try the API, but fallback to a quick message if it takes too long
            # importing requests inside async function is blocking, but for low volume it's ok
            import requests, urllib.parse
            
            # reusing dashboard logic simplified
            url_base = "https://nominatim.openstreetmap.org/search"
            headers = {'User-Agent': 'AntigravityAgent/1.0'}
            r_o = requests.get(f"{url_base}?q={urllib.parse.quote(origin)}&format=json&limit=1", headers=headers).json()
            r_d = requests.get(f"{url_base}?q={urllib.parse.quote(dest)}&format=json&limit=1", headers=headers).json()
            
            if not r_o:
                await message.channel.send(f"❌ Could not find origin: `{origin}`")
            elif not r_d:
                await message.channel.send(f"❌ Could not find destination: `{dest}`")

            else:
                o_lon, o_lat = r_o[0]['lon'], r_o[0]['lat']
                d_lon, d_lat = r_d[0]['lon'], r_d[0]['lat']
                
                osrm_url = f"http://router.project-osrm.org/route/v1/driving/{o_lon},{o_lat};{d_lon},{d_lat}?overview=false"
                r_route = requests.get(osrm_url).json()
                
                if r_route['code'] == 'Ok':
                    dist_meters = r_route['routes'][0]['distance']
                    dist_miles = dist_meters * 0.000621371
                    
                    est = estimate_route(dist_miles, vehicle, 4.15) # Default fuel price
                    
                    embed = discord.Embed(title="🚛 Route Estimate", color=0x3498db)
                    embed.add_field(name="Route", value=f"{origin} ➡️ {dest}", inline=False)
                    embed.add_field(name="Distance", value=f"{est['distance']:,.1f} miles", inline=True)
                    embed.add_field(name="Drive Time", value=f"{est['drive_time_hours']} hrs", inline=True)
                    embed.add_field(name="Fuel Cost", value=f"${est['fuel_cost']:,.2f}", inline=True)
                    
                    if est['hos_info'] and est['hos_info']['is_violation']:
                        embed.add_field(name="⚠️ HOS Warning", value=f"Requires {est['hos_info']['breaks_needed']} x 10hr breaks", inline=False)
                        
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("❌ Route calculation failed.")
                    
        except Exception as e:
            await message.channel.send(f"❌ Error: {str(e)}")

        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    if msg.startswith('!email invoice '):
        # !email invoice 1001
        try:
            inv_id = int(msg[15:].strip())
            await message.channel.send(f"📧 Preparing Invoice #{inv_id}...")
            
            # 1. Get Invoice Data
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_invoices'))
            from invoice_manager import get_invoices, generate_invoice_docx
            
            invoices = get_invoices()
            target = next((i for i in invoices if i['invoice_number'] == inv_id), None)
            
            if not target:
                await message.channel.send(f"❌ Invoice #{inv_id} not found.")
                return
                
            # 2. Get Client Email
            client_email = target['client'].get('email')
            if not client_email:
                await message.channel.send(f"⚠️ Client {target['client']['name']} has no email address.")
                return

            # 3. Generate Document (to ensure latest)
            doc_path = generate_invoice_docx(inv_id)
            
            # 4. Send Email
            from email_manager import EmailManager
            sender = EmailManager()
            
            subject = f"Invoice #{inv_id} from {target.get('company_info', {}).get('name', 'Jayboi Services')}"
            body = f"""
            <h2>Invoice #{inv_id}</h2>
            <p>Dear {target['client']['name']},</p>
            <p>Please find attached invoice #{inv_id} for ${target['total']:,.2f}.</p>
            <p><strong>Due Date:</strong> {target['due_date'][:10]}</p>
            <p>Thank you for your business!</p>
            """
            
            result = sender.send_email(client_email, subject, body, attachments=[doc_path])
            
            if result.get("success"):
                await message.channel.send(f"✅ Invoice sent to {client_email}!")
            else:
                await message.channel.send(f"❌ Failed to send: {result.get('error')}")
                
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    if msg.startswith('!report'):
        # Business Status Report
        await message.channel.send("📊 Generating Daily Business Report...")
        try:
            embed = discord.Embed(title="📊 Daily Business Report", color=0x2c3e50)
            
            # --- Lead Puller Stats ---
            stats_path = "/Volumes/CeeJay SSD/Projects/lead puller/daily_stats.json"
            if os.path.exists(stats_path):
                try:
                    with open(stats_path, 'r') as f:
                        lp_stats = json.load(f)
                    embed.add_field(name="🤖 Lead Puller", value=f"Sent: {lp_stats.get('sent_count', 0)}\nTarget: {lp_stats.get('city_index', '?')}", inline=True)
                except:
                    embed.add_field(name="🤖 Lead Puller", value="Error reading stats", inline=True)
            else:
                embed.add_field(name="🤖 Lead Puller", value="Not Active / No Data", inline=True)

            # --- Invoices Stats ---
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_invoices'))
            from invoice_manager import get_stats as get_inv_stats
            i_stats = get_inv_stats()
            embed.add_field(name="💰 Invoices", value=f"Unpaid: ${i_stats['unpaid_amount']:,.0f} ({i_stats['unpaid_count']})\nPaid: ${i_stats['paid_amount']:,.0f}", inline=True)

            # --- Rate Stats (Mock or Calc) ---
            # Could import from pocket_rates if needed
            
            await message.channel.send(embed=embed)
            
        except Exception as e:
             await message.channel.send(f"❌ Reporting Error: {e}")

    if msg.startswith('!reminders'):
        # List reminders: !reminders or !reminders bills
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_reminders'))
        from reminder_manager import get_reminders, format_reminder
        
        try:
            parts = msg.split()
            category = parts[1] if len(parts) > 1 else None
            
            reminders = get_reminders(category=category)
            
            if not reminders:
                await message.channel.send("📭 No active reminders." + (f" (category: {category})" if category else ""))
                return
            
            lines = ["# 📋 Your Reminders\n"]
            for r in reminders[:15]:  # Limit to 15
                lines.append(format_reminder(r))
            
            if len(reminders) > 15:
                lines.append(f"\n... and {len(reminders) - 15} more")
            
            await message.channel.send("\n".join(lines))
            
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    if msg.startswith('!done '):
        # Mark complete: !done [id]
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_reminders'))
        from reminder_manager import mark_complete
        
        try:
            reminder_id = int(msg[6:].strip())
            
            if mark_complete(reminder_id):
                await message.channel.send(f"✅ Reminder #{reminder_id} marked complete!")
            else:
                await message.channel.send(f"❌ Reminder #{reminder_id} not found.")
                
        except ValueError:
            await message.channel.send("❌ Usage: `!done [id]` - Use the ID number from !reminders")
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

    if msg.startswith('!delreminder '):
        # Delete reminder: !delreminder [id]
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pocket_reminders'))
        from reminder_manager import delete_reminder
        
        try:
            reminder_id = int(msg[13:].strip())
            
            if delete_reminder(reminder_id):
                await message.channel.send(f"🗑️ Reminder #{reminder_id} deleted!")
            else:
                await message.channel.send(f"❌ Reminder #{reminder_id} not found.")
                
        except ValueError:
            await message.channel.send("❌ Usage: `!delreminder [id]`")
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

client.run(TOKEN)

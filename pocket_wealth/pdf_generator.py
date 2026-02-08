from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Wealth Manager Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_wealth_report(client_name, data, progress):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # 1. Executive Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Financial Snapshot: {client_name}", 0, 1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Daily Target: ${data['budget']['daily_target']:.2f}", 0, 1)
    pdf.cell(0, 10, f"Earned Today: ${progress['earned']:.2f} ({progress['percent']}%)", 0, 1)
    pdf.ln(5)
    
    # Net Worth
    latest_nw = data.get("net_worth_history", [])[-1] if data.get("net_worth_history") else {}
    nw_val = latest_nw.get("net_worth", 0)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Net Worth: ${nw_val:,.2f}", 0, 1)
    pdf.set_font("Arial", size=12)
    if latest_nw:
        pdf.cell(0, 10, f"Total Assets: ${latest_nw.get('total_assets', 0):,.2f}", 0, 1)
        pdf.cell(0, 10, f"Total Debts: ${latest_nw.get('total_debts', 0):,.2f}", 0, 1)
    else:
        pdf.cell(0, 10, "No net worth data recorded.", 0, 1)
    pdf.ln(5)
    
    # Budget Breakdown
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Monthly Bills", 0, 1)
    pdf.set_font("Arial", size=12)
    
    bills = data['budget'].get('monthly_bills', [])
    if bills:
        total_bills = sum(b['amount'] for b in bills)
        pdf.cell(0, 10, f"Total Monthly Expenses: ${total_bills:,.2f}", 0, 1)
        pdf.ln(2)
        
        # Table Header
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(100, 8, "Bill Name", 1, 0, 'L', 1)
        pdf.cell(50, 8, "Amount", 1, 1, 'R', 1)
        
        # Table Rows
        pdf.set_font("Arial", size=10)
        for bill in bills:
            pdf.cell(100, 8, str(bill['name']), 1, 0, 'L')
            pdf.cell(50, 8, f"${bill['amount']:.2f}", 1, 1, 'R')
    else:
        pdf.cell(0, 10, "No bills recorded.", 0, 1)
        
    pdf.ln(10)
    
    # Recent Earnings
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Recent Earnings (Last 10)", 0, 1)
    
    logs = data.get("daily_log", [])
    if logs:
        # Table Header
        pdf.set_fill_color(220, 255, 220)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 8, "Date", 1, 0, 'L', 1)
        pdf.cell(70, 8, "Source", 1, 0, 'L', 1)
        pdf.cell(40, 8, "Amount", 1, 1, 'R', 1)
        
        # Table Rows
        pdf.set_font("Arial", size=10)
        for log in list(reversed(logs))[:10]:
            pdf.cell(40, 8, str(log['date']), 1, 0, 'L')
            pdf.cell(70, 8, str(log['source']), 1, 0, 'L')
            pdf.cell(40, 8, f"${log['amount']:.2f}", 1, 1, 'R')
    else:
        pdf.cell(0, 10, "No earnings logged.", 0, 1)

    # Save
    report_path = os.path.join(os.path.dirname(__file__), f"Wealth_Report_{datetime.now().strftime('%Y%m%d')}.pdf")
    pdf.output(report_path)
    return report_path

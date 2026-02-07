from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_mock_report(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.drawString(100, 750, "MOCK CREDIT REPORT")
    c.drawString(100, 730, "Report Date: 02/05/2026")
    
    c.drawString(100, 700, "Account: CHASE BANK")
    c.drawString(100, 685, "Status: LATE 30 DAYS")
    c.drawString(100, 670, "Balance: $500")
    
    c.drawString(100, 640, "Account: MIDLAND CREDIT MANAGEMENT")
    c.drawString(100, 625, "Status: COLLECTION")
    c.drawString(100, 610, "Balance: $150")
    
    c.drawString(100, 580, "Account: CAPITAL ONE")
    c.drawString(100, 565, "Status: PAID AS AGREED")
    
    c.save()

if __name__ == "__main__":
    if not os.path.exists("pocket_credit/input_reports"):
        os.makedirs("pocket_credit/input_reports")
    create_mock_report("pocket_credit/input_reports/mock_report.pdf")
    print("Created mock_report.pdf")

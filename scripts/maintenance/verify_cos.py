import sys
import os

# Add pocket_jarvis to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pocket_jarvis')))

try:
    import chief_of_staff
    print("✅ Successfully imported chief_of_staff")
    metrics = chief_of_staff.get_dashboard_metrics()
    print(f"Metrics: {metrics.keys()}")
except Exception as e:
    print(f"❌ Failed to import: {e}")

import os
import sys

# Add jarsvis module to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pocket_jarvis')))

try:
    import chief_of_staff
    print("✅ Imported chief_of_staff")
    
    print("Testing get_dashboard_metrics...")
    metrics = chief_of_staff.get_dashboard_metrics()
    
    required_keys = ["finance", "system", "agents", "timestamp"]
    missing = [k for k in required_keys if k not in metrics]
    
    if missing:
        print(f"❌ Missing keys in metrics: {missing}")
    else:
        print("✅ Metrics structure looks correct.")
        print(f"Snapshot: {metrics}")
        
    print("Testing trigger_system_action (Simulated)...")
    res = chief_of_staff.trigger_system_action("system_cleanup")
    if res['success']:
        print(f"✅ Trigger successful: {res['message']}")
    else:
        print(f"❌ Trigger failed: {res['message']}")

except Exception as e:
    print(f"❌ Test Failed: {e}")

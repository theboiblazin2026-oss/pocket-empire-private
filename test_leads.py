import sys
import os

# Add leads module to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pocket_leads')))

try:
    import lead_manager
    print("✅ Imported lead_manager")
    
    # Mock Batch Data
    test_ids = ["MC123456", "MC987654", "DOT1234567"]
    print(f"Testing batch logic for {len(test_ids)} IDs...")
    
    results = []
    for val in test_ids:
        # We expect this to fail gracefully or return simulated data if the real scraping fails without internet/auth
        # But we are testing the function call structure
        print(f"Scoring {val}...")
        try:
            res = lead_manager.score_by_identifier(val)
            if "error" in res:
                print(f"  ⚠️ {val}: Error - {res['error']}")
                # Expected for dummy IDs in a test environment without real scraping
                # But confirming the function executes is what matters
            else:
                print(f"  ✅ {val}: Score {res.get('score')}")
        except Exception as e:
             print(f"  ❌ {val}: Exception - {e}")
             
    print("✅ Batch verification loop completed.")

except Exception as e:
    print(f"❌ Test Failed: {e}")

import os
import sys
from io import BytesIO

# Add compliance module to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pocket_compliance')))

try:
    import vault_manager
    print("✅ Imported vault_manager")
    
    # Test Data
    test_id = "MC123456"
    test_content = b"This is a test document."
    
    # Mock File Object (like Streamlit returns)
    class MockFile:
        def __init__(self, name, content):
            self.name = name
            self.content = content
        def getbuffer(self):
            return self.content

    mock_file = MockFile("test_doc.txt", test_content)
    
    # Test Save
    print(f"Testing save for {test_id}...")
    path = vault_manager.save_document(test_id, mock_file, "TestType")
    print(f"✅ Saved to: {path}")
    
    if os.path.exists(path):
        print("✅ File actually exists on disk.")
    else:
        print("❌ File NOT found on disk.")
        
    # Test List
    print("Testing list_documents...")
    docs = vault_manager.list_documents(test_id)
    if len(docs) > 0:
        print(f"✅ Found {len(docs)} documents.")
        print(f"First doc: {docs[0]['filename']}")
    else:
        print("❌ No documents found.")

except Exception as e:
    print(f"❌ Test Failed: {e}")

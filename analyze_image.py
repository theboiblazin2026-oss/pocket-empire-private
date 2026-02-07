import ollama
import sys
import os

# Usage: python3 analyze_image.py <path_to_image> "[Optional prompt]"

if len(sys.argv) < 2:
    print("Usage: python3 analyze_image.py <path_to_image> [prompt]")
    exit(1)

image_path = sys.argv[1]
prompt = sys.argv[2] if len(sys.argv) > 2 else "Describe this image in detail."

if not os.path.exists(image_path):
    print(f"Error: File {image_path} not found.")
    exit(1)

print(f"👁️ Looking at {image_path}...")
print(f"📝 Prompt: {prompt}")

try:
    response = ollama.chat(model='llava', messages=[
      {
        'role': 'user',
        'content': prompt,
        'images': [image_path]
      }
    ])
    
    print("\n--- 🤖 Vision Analysis ---\n")
    print(response['message']['content'])
    print("\n--------------------------")

except Exception as e:
    print(f"Error: {e}")

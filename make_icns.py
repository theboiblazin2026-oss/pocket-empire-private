from PIL import Image
import sys
import os

def create_icns(png_path, icns_path):
    if not os.path.exists(png_path):
        print(f"Error: {png_path} not found")
        sys.exit(1)

    img = Image.open(png_path)
    
    # Create the iconset directory
    iconset_name = "pocket.iconset"
    if not os.path.exists(iconset_name):
        os.makedirs(iconset_name)
    
    # Defined sizes for macOS icons
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    for size in sizes:
        # Normal resolution
        resized_img = img.resize((size, size), Image.LANCZOS)
        resized_img.save(f"{iconset_name}/icon_{size}x{size}.png")
        
        # Retina resolution (@2x), skipping 1024 as 1024x1024@2x is huge and rarely needed for simple usage
        if size < 512: 
            retina_size = size * 2
            retina_img = img.resize((retina_size, retina_size), Image.LANCZOS)
            retina_img.save(f"{iconset_name}/icon_{size}x{size}@2x.png")

    # Run iconutil to convert iconset to icns
    os.system(f"iconutil -c icns {iconset_name} -o '{icns_path}'")
    
    # Formatting cleanup
    os.system(f"rm -rf {iconset_name}")
    print(f"✅ Generated {icns_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python make_icns.py <input.png> <output.icns>")
    else:
        create_icns(sys.argv[1], sys.argv[2])

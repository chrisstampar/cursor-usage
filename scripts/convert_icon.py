from PIL import Image

def convert_to_icns(input_path, output_path):
    img = Image.open(input_path).convert('RGBA')
    
    # Ensure square
    width, height = img.size
    size = min(width, height)
    left = (width - size) / 2
    top = (height - size) / 2
    right = (width + size) / 2
    bottom = (height + size) / 2
    img = img.crop((left, top, right, bottom))
    
    # Save as ICNS directly
    img.save(output_path, format='ICNS')

if __name__ == "__main__":
    import sys
    convert_to_icns(sys.argv[1], sys.argv[2])
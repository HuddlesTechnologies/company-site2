import sys
from pathlib import Path
from PIL import Image
import hashlib

input_dir = Path(sys.argv[1])

if not input_dir.exists():
    print(f"Folder not found: {input_dir}")
    sys.exit(1)

# Keep track of hashes to detect duplicates
seen_hashes = set()

# Recursively search for images
for img_path in input_dir.rglob("*"):
    suffix = img_path.suffix.lower()
    
    # Skip existing WebP files
    if suffix == ".webp":
        print(f"Skipping existing WebP: {img_path}")
        continue

    # Only process images
    if suffix in {".jpg", ".jpeg", ".png"}:
        try:
            with Image.open(img_path) as im:
                # Compute hash of image content
                img_hash = hashlib.md5(im.tobytes()).hexdigest()
                
                if img_hash in seen_hashes:
                    print(f"Duplicate skipped: {img_path}")
                    continue  # skip duplicate
                
                seen_hashes.add(img_hash)
                
                # Convert to WebP with quality=90
                webp_path = img_path.with_suffix(".webp")
                im.save(webp_path, "WEBP", quality=90)
                print(f"Converted: {img_path} → {webp_path}")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
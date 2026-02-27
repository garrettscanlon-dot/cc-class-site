#!/usr/bin/env python3
"""
Generate images using Google Gemini 2.5 Flash Image.

Usage:
  python scripts/generate-image.py "A hero image for a SaaS landing page"
  python scripts/generate-image.py "Redesign this screenshot" --image screenshot.png
  python scripts/generate-image.py "Blog header about customer success" --output blog-header.png
"""

import argparse
import base64
import json
import os
import ssl
import sys
from datetime import datetime
from pathlib import Path
from urllib import request, error

# Handle macOS Python SSL certificate issue
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_DIR / "output"


def load_api_key():
    env_path = PROJECT_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY=") and not line.startswith("#"):
                return line.split("=", 1)[1].strip().strip("\"'")
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    print("Error: GEMINI_API_KEY not found.")
    print("Add it to .env:  GEMINI_API_KEY=your-key-here")
    print("Or export it:    export GEMINI_API_KEY=your-key-here")
    sys.exit(1)


def encode_image(image_path):
    path = Path(image_path)
    if not path.exists():
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)

    ext = path.suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    mime = mime_types.get(ext)
    if not mime:
        print(f"Error: Unsupported image format: {ext}")
        print(f"Supported: {', '.join(mime_types.keys())}")
        sys.exit(1)

    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    return {"inline_data": {"mime_type": mime, "data": data}}


def generate_image(prompt, image_path=None, output_path=None):
    api_key = load_api_key()

    # Build request parts
    parts = []
    if image_path:
        parts.append(encode_image(image_path))
        print(f"Using reference image: {image_path}")
    parts.append({"text": prompt})

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash-image:generateContent"
        f"?key={api_key}"
    )

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    print(f"Prompt: {prompt}")
    print("Generating...")

    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=120, context=SSL_CONTEXT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"API error ({e.code}): {body}")
        sys.exit(1)
    except error.URLError as e:
        print(f"Network error: {e.reason}")
        sys.exit(1)

    # Extract image from response
    candidates = result.get("candidates", [])
    if not candidates:
        print("Error: No response from API.")
        print(json.dumps(result, indent=2))
        sys.exit(1)

    image_data = None
    text_response = None

    for part in candidates[0].get("content", {}).get("parts", []):
        # API may return camelCase or snake_case keys
        if "inlineData" in part:
            image_data = part["inlineData"]["data"]
        elif "inline_data" in part:
            image_data = part["inline_data"]["data"]
        elif "text" in part:
            text_response = part["text"]

    if not image_data:
        print("Error: No image in response.")
        if text_response:
            print(f"Model said: {text_response}")
        sys.exit(1)

    # Save image
    OUTPUT_DIR.mkdir(exist_ok=True)
    if output_path:
        save_path = Path(output_path)
        if not save_path.is_absolute():
            save_path = PROJECT_DIR / save_path
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        slug = prompt[:40].lower().replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-").strip("-")
        save_path = OUTPUT_DIR / f"{timestamp}-{slug}.png"

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(base64.standard_b64decode(image_data))

    print(f"Saved: {save_path}")
    if text_response:
        print(f"Model notes: {text_response}")
    return save_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate images with Google Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate-image.py "A minimal hero image for a SaaS product"
  python scripts/generate-image.py "Make this more professional" --image input.png
  python scripts/generate-image.py "Blog header" --output images/blog-hero.png
        """,
    )
    parser.add_argument("prompt", help="Text prompt describing the image to generate")
    parser.add_argument("--image", "-i", help="Reference image path (for edits or context)")
    parser.add_argument("--output", "-o", help="Output file path (default: output/<timestamp>.png)")
    args = parser.parse_args()

    generate_image(args.prompt, args.image, args.output)


if __name__ == "__main__":
    main()

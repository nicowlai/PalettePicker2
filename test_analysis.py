#!/usr/bin/env python3
"""
Test script for the improved color analysis algorithm
"""

import base64
import io
from PIL import Image
import numpy as np

# Import the analysis functions from app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the COLOR_TYPES for testing
COLOR_TYPES = {
    'cool_winter': {'name': 'Cool Winter'},
    'neutral_winter': {'name': 'Neutral Winter'},
    'bright_spring': {'name': 'Bright Spring'},
    'warm_spring': {'name': 'Warm Spring'},
    'cool_summer': {'name': 'Cool Summer'},
    'neutral_summer': {'name': 'Neutral Summer'},
    'warm_autumn': {'name': 'Warm Autumn'},
    'deep_autumn': {'name': 'Deep Autumn'}
}

def create_test_image(skin_brightness=120, skin_warmth=15, hair_brightness=80, hair_warmth=10, eye_brightness=70, eye_warmth=5):
    """Create a test image with specific characteristics"""
    # Create a simple test image
    width, height = 200, 200
    
    # Create skin tone (center area)
    skin_r = min(255, max(0, skin_brightness + skin_warmth))
    skin_g = min(255, max(0, skin_brightness))
    skin_b = min(255, max(0, skin_brightness - skin_warmth))
    skin_color = (int(skin_r), int(skin_g), int(skin_b))
    
    # Create hair tone (top area)
    hair_r = min(255, max(0, hair_brightness + hair_warmth))
    hair_g = min(255, max(0, hair_brightness))
    hair_b = min(255, max(0, hair_brightness - hair_warmth))
    hair_color = (int(hair_r), int(hair_g), int(hair_b))
    
    # Create eye tone (upper face area)
    eye_r = min(255, max(0, eye_brightness + eye_warmth))
    eye_g = min(255, max(0, eye_brightness))
    eye_b = min(255, max(0, eye_brightness - eye_warmth))
    eye_color = (int(eye_r), int(eye_g), int(eye_b))
    
    # Create image
    img = Image.new('RGB', (width, height), (255, 255, 255))
    
    # Add skin area (center)
    for y in range(int(height * 0.25), int(height * 0.75)):
        for x in range(int(width * 0.25), int(width * 0.75)):
            img.putpixel((x, y), skin_color)
    
    # Add hair area (top)
    for y in range(int(height * 0.05), int(height * 0.35)):
        for x in range(int(width * 0.1), int(width * 0.9)):
            img.putpixel((x, y), hair_color)
    
    # Add eye area (upper face)
    for y in range(int(height * 0.3), int(height * 0.5)):
        for x in range(int(width * 0.3), int(width * 0.7)):
            img.putpixel((x, y), eye_color)
    
    return img

def test_analysis_algorithm():
    """Test the analysis algorithm with different characteristics"""
    print("🧪 Testing Color Analysis Algorithm")
    print("=" * 50)
    
    test_cases = [
        ("Cool Winter", 120, -15, 40, -10, 50, -5),  # Dark hair, dark eyes, cool skin
        ("Neutral Winter", 125, 5, 45, 0, 55, 2),    # Dark hair, dark eyes, neutral skin
        ("Bright Spring", 160, 20, 150, 15, 130, 10), # Light hair, light eyes, warm bright skin
        ("Warm Spring", 140, 15, 120, 10, 110, 8),   # Medium hair, medium eyes, warm skin
        ("Cool Summer", 145, -20, 130, -15, 125, -10), # Light hair, light eyes, cool skin
        ("Neutral Summer", 135, -5, 110, -5, 100, -3), # Medium hair, medium eyes, neutral skin
        ("Warm Autumn", 100, 25, 80, 20, 70, 15),    # Medium hair, medium eyes, warm skin
        ("Deep Autumn", 80, 30, 50, 25, 45, 20),     # Dark hair, dark eyes, warm skin
    ]
    
    for name, skin_bright, skin_warm, hair_bright, hair_warm, eye_bright, eye_warm in test_cases:
        print(f"\n📸 Testing: {name}")
        print(f"   Skin: brightness={skin_bright}, warmth={skin_warm}")
        print(f"   Hair: brightness={hair_bright}, warmth={hair_warm}")
        print(f"   Eyes: brightness={eye_bright}, warmth={eye_warm}")
        
        # Create test image
        test_img = create_test_image(skin_bright, skin_warm, hair_bright, hair_warm, eye_bright, eye_warm)
        
        # Convert to base64
        buffer = io.BytesIO()
        test_img.save(buffer, format='PNG')
        img_data = base64.b64encode(buffer.getvalue()).decode()
        image_data = f"data:image/png;base64,{img_data}"
        
        # Test analysis
        try:
            from app import analyze_image_features
            result = analyze_image_features(image_data)
            print(f"   ✅ Result: {COLOR_TYPES[result]['name']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎉 Analysis test completed!")

if __name__ == "__main__":
    test_analysis_algorithm() 
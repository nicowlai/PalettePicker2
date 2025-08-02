#!/usr/bin/env python3
"""
Test the Gemini API call
"""

import requests
import base64
import io
from PIL import Image

def test_gemini_api():
    """Test the Gemini API directly"""
    print("🧪 Testing Gemini API")
    print("=" * 30)
    
    # Create a simple test image
    img = Image.new('RGB', (200, 200), (255, 255, 255))
    
    # Add some color areas
    for y in range(50, 150):
        for x in range(50, 150):
            img.putpixel((x, y), (200, 150, 100))  # Skin tone
    
    for y in range(10, 40):
        for x in range(20, 180):
            img.putpixel((x, y), (100, 80, 60))  # Hair
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # API configuration
    GEMINI_API_KEY = "AIzaSyD_qGFz5MHnupcsO024ckw4TDrs7W3EaLg"
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
    
    # Prepare the prompt
    prompt = """
    Analyze this person's color characteristics for personal color analysis. 
    Look at their skin tone, hair color, and eye color.
    
    Based on traditional color analysis principles:
    - Light skin + Light hair + Warm undertones = Spring (Bright Spring or Warm Spring)
    - Light skin + Light hair + Cool undertones = Summer (Cool Summer or Neutral Summer)
    - Medium skin + Medium hair + Warm undertones = Autumn (Warm Autumn or Deep Autumn)
    - Dark skin + Dark hair + Cool undertones = Winter (Cool Winter or Neutral Winter)
    - High contrast features = Winter
    - Low contrast features = Summer
    
    Respond with ONLY one of these exact color types:
    - cool_winter
    - neutral_winter
    - bright_spring
    - warm_spring
    - cool_summer
    - neutral_summer
    - warm_autumn
    - deep_autumn
    """
    
    # Prepare the API request
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_base64
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "topK": 1,
            "topP": 0.1,
            "maxOutputTokens": 50,
        }
    }
    
    print(f"🔑 Using API key: {GEMINI_API_KEY[:10]}...")
    print(f"🌐 API URL: {GEMINI_API_URL}")
    
    try:
        # Make the API request
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API call successful!")
            
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                print(f"🤖 AI Response: {text}")
                
                # Check for color types
                color_types = ['cool_winter', 'neutral_winter', 'bright_spring', 'warm_spring', 
                              'cool_summer', 'neutral_summer', 'warm_autumn', 'deep_autumn']
                
                for color_type in color_types:
                    if color_type in text.lower():
                        print(f"🎨 Detected Color Type: {color_type}")
                        break
                else:
                    print("⚠️  No specific color type detected in response")
            else:
                print("❌ No candidates in response")
                print(f"Response: {result}")
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_gemini_api()
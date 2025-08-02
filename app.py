from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
from PIL import Image
import io
import json
import random
from datetime import datetime
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyD_qGFz5MHnupcsO024ckw4TDrs7W3EaLg"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision:generateContent"

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Color analysis data
COLOR_TYPES = {
    'cool_winter': {
        'name': 'Cool Winter',
        'description': 'You have a cool, bright complexion with blue undertones. Your features are striking and high contrast.',
        'characteristics': 'High contrast, cool undertones, bright eyes',
        'clothing': ['Deep jewel tones', 'Pure white', 'Navy blue', 'Hot pink', 'Emerald green'],
        'makeup': ['Cool-toned lipsticks', 'Silver eyeshadow', 'Cool pink blushes', 'Navy eyeliner'],
        'avoid': ['Warm oranges', 'Yellow-greens', 'Golden browns']
    },
    'neutral_winter': {
        'name': 'Neutral Winter',
        'description': 'You have a balanced cool-warm complexion with medium contrast. Your features are versatile and adaptable.',
        'characteristics': 'Medium contrast, neutral undertones, balanced features',
        'clothing': ['Charcoal gray', 'Burgundy', 'Teal', 'Rose pink', 'Navy'],
        'makeup': ['Neutral lipsticks', 'Rose gold eyeshadow', 'Neutral blushes', 'Brown eyeliner'],
        'avoid': ['Very warm colors', 'Very cool colors']
    },
    'bright_spring': {
        'name': 'Bright Spring',
        'description': 'You have a warm, bright complexion with golden undertones. Your features are vibrant and energetic.',
        'characteristics': 'High brightness, warm undertones, clear features',
        'clothing': ['Coral', 'Bright yellow', 'Turquoise', 'Hot pink', 'Lime green'],
        'makeup': ['Coral lipsticks', 'Gold eyeshadow', 'Peach blushes', 'Bronze eyeliner'],
        'avoid': ['Muted colors', 'Very dark colors']
    },
    'warm_spring': {
        'name': 'Warm Spring',
        'description': 'You have a warm, golden complexion with clear features. Your coloring is fresh and natural.',
        'characteristics': 'Warm undertones, medium brightness, natural features',
        'clothing': ['Coral', 'Golden yellow', 'Warm green', 'Peach', 'Camel'],
        'makeup': ['Peach lipsticks', 'Warm brown eyeshadow', 'Coral blushes', 'Bronze eyeliner'],
        'avoid': ['Cool blues', 'Gray', 'Black']
    },
    'cool_summer': {
        'name': 'Cool Summer',
        'description': 'You have a cool, soft complexion with blue undertones. Your features are gentle and refined.',
        'characteristics': 'Low contrast, cool undertones, soft features',
        'clothing': ['Soft blue', 'Lavender', 'Rose pink', 'Gray', 'Mint green'],
        'makeup': ['Soft pink lipsticks', 'Cool taupe eyeshadow', 'Cool pink blushes', 'Gray eyeliner'],
        'avoid': ['Bright colors', 'Warm oranges', 'Black']
    },
    'neutral_summer': {
        'name': 'Neutral Summer',
        'description': 'You have a balanced soft complexion with neutral undertones. Your features are harmonious and elegant.',
        'characteristics': 'Medium contrast, neutral undertones, balanced features',
        'clothing': ['Soft gray', 'Rose brown', 'Sage green', 'Dusty pink', 'Taupe'],
        'makeup': ['Neutral lipsticks', 'Taupe eyeshadow', 'Neutral blushes', 'Brown eyeliner'],
        'avoid': ['Very bright colors', 'Very dark colors']
    },
    'warm_autumn': {
        'name': 'Warm Autumn',
        'description': 'You have a warm, rich complexion with golden undertones. Your features are deep and earthy.',
        'characteristics': 'Medium contrast, warm undertones, rich features',
        'clothing': ['Rust', 'Olive green', 'Camel', 'Terracotta', 'Warm brown'],
        'makeup': ['Terracotta lipsticks', 'Warm brown eyeshadow', 'Coral blushes', 'Bronze eyeliner'],
        'avoid': ['Cool blues', 'Bright pinks', 'Pure white']
    },
    'deep_autumn': {
        'name': 'Deep Autumn',
        'description': 'You have a deep, rich complexion with warm undertones. Your features are dramatic and intense.',
        'characteristics': 'High contrast, warm undertones, deep features',
        'clothing': ['Deep burgundy', 'Forest green', 'Rich brown', 'Deep orange', 'Navy'],
        'makeup': ['Deep burgundy lipsticks', 'Rich brown eyeshadow', 'Terracotta blushes', 'Black eyeliner'],
        'avoid': ['Light pastels', 'Cool grays', 'Bright yellows']
    }
}

def analyze_image_features(image_data):
    """Analyze image features and determine color type with accurate color analysis"""
    try:
        # Decode and open the image
        img = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Try Gemini API first for more accurate analysis
        try:
            gemini_result = analyze_with_gemini(img, image_data)
            if gemini_result:
                print(f"DEBUG - Gemini API result: {gemini_result}")
                return gemini_result
        except Exception as e:
            print(f"DEBUG - Gemini API failed: {e}")
        
        # Fallback to traditional analysis
        print("DEBUG - Using traditional analysis")
        
        # Get image dimensions
        width, height = img.size
        
        # Define regions for analysis
        # Face region (center area)
        face_x1, face_y1 = int(width * 0.25), int(height * 0.25)
        face_x2, face_y2 = int(width * 0.75), int(height * 0.75)
        face_region = img.crop((face_x1, face_y1, face_x2, face_y2))
        
        # Hair region (top area)
        hair_x1, hair_y1 = int(width * 0.1), int(height * 0.05)
        hair_x2, hair_y2 = int(width * 0.9), int(height * 0.35)
        hair_region = img.crop((hair_x1, hair_y1, hair_x2, hair_y2))
        
        # Eye region (upper face area)
        eye_x1, eye_y1 = int(width * 0.3), int(height * 0.3)
        eye_x2, eye_y2 = int(width * 0.7), int(height * 0.5)
        eye_region = img.crop((eye_x1, eye_y1, eye_x2, eye_y2))
        
        # Analyze skin tone (face region)
        skin_analysis = analyze_skin_tone(face_region)
        
        # Analyze hair color (hair region)
        hair_analysis = analyze_hair_color(hair_region)
        
        # Analyze eye color (eye region)
        eye_analysis = analyze_eye_color(eye_region)
        
        # Determine color type based on traditional color analysis principles
        return determine_color_type_accurate(skin_analysis, hair_analysis, eye_analysis)
        
    except Exception as e:
        print(f"Error in image analysis: {e}")
        return random.choice(list(COLOR_TYPES.keys()))

def analyze_with_gemini(img, image_data):
    """Analyze image using Gemini API for more accurate color analysis"""
    try:
        # Prepare the image for Gemini API
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=85)
        img_buffer.seek(0)
        
        # Encode image for API
        import base64
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        # Prepare the prompt for color analysis
        prompt = """
        Analyze this person's color characteristics for personal color analysis. 
        Look at their skin tone, hair color, and eye color.
        
        Based on traditional color analysis principles:
        - Dark hair + dark eyes = Winter palette (Cool Winter or Neutral Winter)
        - Light hair + light eyes + warm skin = Spring palette (Bright Spring or Warm Spring)
        - Light hair + light eyes + cool skin = Summer palette (Cool Summer or Neutral Summer)
        - Medium features + warm skin = Autumn palette (Warm Autumn or Deep Autumn)
        
        Respond with ONLY one of these exact color types:
        - cool_winter
        - neutral_winter
        - bright_spring
        - warm_spring
        - cool_summer
        - neutral_summer
        - warm_autumn
        - deep_autumn
        
        Be very specific about the features you see and choose the most accurate color type.
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
        
        # Make the API request
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text'].strip().lower()
                
                # Extract the color type from the response
                for color_type in COLOR_TYPES.keys():
                    if color_type in text:
                        return color_type
                
                print(f"DEBUG - Gemini response: {text}")
                return None
        else:
            print(f"DEBUG - Gemini API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"DEBUG - Gemini API exception: {e}")
        return None

def analyze_skin_tone(face_region):
    """Analyze skin tone characteristics"""
    colors = face_region.getcolors(2000)
    if not colors:
        return {'brightness': 120, 'warmth': 0, 'contrast': 'medium'}
    
    # Get dominant skin colors
    dominant_colors = [color for count, color in colors if count > 100]
    if not dominant_colors:
        dominant_colors = [color for count, color in colors[:10]]
    
    # Calculate skin characteristics
    avg_r = sum(color[0] for color in dominant_colors) / len(dominant_colors)
    avg_g = sum(color[1] for color in dominant_colors) / len(dominant_colors)
    avg_b = sum(color[2] for color in dominant_colors) / len(dominant_colors)
    
    brightness = (avg_r + avg_g + avg_b) / 3
    warmth = avg_r - avg_b  # Red vs Blue balance
    saturation = max(avg_r, avg_g, avg_b) - min(avg_r, avg_g, avg_b)
    
    # Determine contrast level
    if brightness > 150:
        contrast = 'high'
    elif brightness > 100:
        contrast = 'medium'
    else:
        contrast = 'low'
    
    return {
        'brightness': brightness,
        'warmth': warmth,
        'saturation': saturation,
        'contrast': contrast
    }

def analyze_hair_color(hair_region):
    """Analyze hair color characteristics with detailed color detection"""
    colors = hair_region.getcolors(2000)
    if not colors:
        return {'brightness': 80, 'warmth': 0, 'color': 'medium', 'specific_color': 'unknown'}
    
    # Get dominant hair colors with better filtering
    dominant_colors = [color for count, color in colors if count > 20]
    if not dominant_colors:
        dominant_colors = [color for count, color in colors[:10]]
    
    # Calculate hair characteristics
    avg_r = sum(color[0] for color in dominant_colors) / len(dominant_colors)
    avg_g = sum(color[1] for color in dominant_colors) / len(dominant_colors)
    avg_b = sum(color[2] for color in dominant_colors) / len(dominant_colors)
    
    brightness = (avg_r + avg_g + avg_b) / 3
    warmth = avg_r - avg_b
    saturation = max(avg_r, avg_g, avg_b) - min(avg_r, avg_g, avg_b)
    
    # Detailed hair color detection
    if brightness < 60:
        if warmth > 10:
            specific_color = 'dark_brown'
        elif warmth < -10:
            specific_color = 'black'
        else:
            specific_color = 'dark_neutral'
        color = 'dark'
    elif brightness < 90:
        if warmth > 15:
            specific_color = 'medium_brown'
        elif warmth > 5:
            specific_color = 'auburn'
        elif warmth < -5:
            specific_color = 'ash_brown'
        else:
            specific_color = 'medium_neutral'
        color = 'medium'
    elif brightness < 130:
        if warmth > 20:
            specific_color = 'light_brown'
        elif warmth > 10:
            specific_color = 'strawberry_blonde'
        elif warmth < -10:
            specific_color = 'ash_blonde'
        else:
            specific_color = 'light_neutral'
        color = 'medium'
    else:
        if warmth > 15:
            specific_color = 'golden_blonde'
        elif warmth > 5:
            specific_color = 'honey_blonde'
        elif warmth < -5:
            specific_color = 'platinum_blonde'
        else:
            specific_color = 'neutral_blonde'
        color = 'light'
    
    print(f"DEBUG - Hair Analysis: brightness={brightness:.1f}, warmth={warmth:.1f}, saturation={saturation:.1f}, color={color}, specific={specific_color}")
    
    return {
        'brightness': brightness,
        'warmth': warmth,
        'saturation': saturation,
        'color': color,
        'specific_color': specific_color
    }

def analyze_eye_color(eye_region):
    """Analyze eye color characteristics with detailed color detection"""
    colors = eye_region.getcolors(1000)
    if not colors:
        return {'brightness': 80, 'warmth': 0, 'color': 'medium', 'specific_color': 'unknown'}
    
    # Get dominant eye colors with better filtering
    dominant_colors = [color for count, color in colors if count > 10]
    if not dominant_colors:
        dominant_colors = [color for count, color in colors[:8]]
    
    # Calculate eye characteristics
    avg_r = sum(color[0] for color in dominant_colors) / len(dominant_colors)
    avg_g = sum(color[1] for color in dominant_colors) / len(dominant_colors)
    avg_b = sum(color[2] for color in dominant_colors) / len(dominant_colors)
    
    brightness = (avg_r + avg_g + avg_b) / 3
    warmth = avg_r - avg_b
    saturation = max(avg_r, avg_g, avg_b) - min(avg_r, avg_g, avg_b)
    
    # Detailed eye color detection
    if brightness < 70:
        if warmth > 10:
            specific_color = 'dark_brown'
        elif warmth < -10:
            specific_color = 'black'
        else:
            specific_color = 'dark_neutral'
        color = 'dark'
    elif brightness < 100:
        if warmth > 15:
            specific_color = 'medium_brown'
        elif warmth > 5:
            specific_color = 'hazel'
        elif warmth < -5:
            specific_color = 'dark_gray'
        else:
            specific_color = 'medium_neutral'
        color = 'medium'
    elif brightness < 140:
        if warmth > 20:
            specific_color = 'light_brown'
        elif warmth > 10:
            specific_color = 'amber'
        elif warmth < -10:
            specific_color = 'light_gray'
        else:
            specific_color = 'light_neutral'
        color = 'medium'
    else:
        if warmth > 15:
            specific_color = 'green'
        elif warmth > 5:
            specific_color = 'hazel_green'
        elif warmth < -15:
            specific_color = 'blue'
        elif warmth < -5:
            specific_color = 'gray_blue'
        else:
            specific_color = 'neutral_light'
        color = 'light'
    
    print(f"DEBUG - Eye Analysis: brightness={brightness:.1f}, warmth={warmth:.1f}, saturation={saturation:.1f}, color={color}, specific={specific_color}")
    
    return {
        'brightness': brightness,
        'warmth': warmth,
        'saturation': saturation,
        'color': color,
        'specific_color': specific_color
    }

def determine_color_type_accurate(skin, hair, eye):
    """Determine color type based on detailed analysis of skin, hair, and eye characteristics"""
    
    # Add debugging information
    print(f"DEBUG - Skin: brightness={skin['brightness']:.1f}, warmth={skin['warmth']:.1f}, contrast={skin['contrast']}")
    print(f"DEBUG - Hair: brightness={hair['brightness']:.1f}, warmth={hair['warmth']:.1f}, color={hair['color']}, specific={hair['specific_color']}")
    print(f"DEBUG - Eyes: brightness={eye['brightness']:.1f}, warmth={eye['warmth']:.1f}, color={eye['color']}, specific={eye['specific_color']}")
    
    # Score-based system for more accurate color type determination
    scores = {
        'cool_winter': 0,
        'neutral_winter': 0,
        'bright_spring': 0,
        'warm_spring': 0,
        'cool_summer': 0,
        'neutral_summer': 0,
        'warm_autumn': 0,
        'deep_autumn': 0
    }
    
    # Skin tone scoring
    if skin['brightness'] < 110:
        if skin['warmth'] < 0:
            scores['cool_winter'] += 3
            scores['neutral_winter'] += 2
        else:
            scores['neutral_winter'] += 3
            scores['deep_autumn'] += 2
    elif skin['brightness'] < 130:
        if skin['warmth'] > 10:
            scores['warm_spring'] += 3
            scores['warm_autumn'] += 2
        elif skin['warmth'] < -5:
            scores['cool_summer'] += 3
            scores['neutral_summer'] += 2
        else:
            scores['neutral_winter'] += 2
            scores['neutral_summer'] += 2
    else:
        if skin['warmth'] > 15:
            scores['bright_spring'] += 3
            scores['warm_spring'] += 2
        elif skin['warmth'] < -10:
            scores['cool_summer'] += 3
            scores['neutral_summer'] += 2
        else:
            scores['bright_spring'] += 2
            scores['cool_summer'] += 2
    
    # Hair color scoring
    if hair['color'] == 'dark':
        if 'black' in hair['specific_color']:
            scores['cool_winter'] += 3
            scores['neutral_winter'] += 2
        elif 'brown' in hair['specific_color']:
            if hair['warmth'] > 10:
                scores['deep_autumn'] += 3
                scores['warm_autumn'] += 2
            else:
                scores['cool_winter'] += 2
                scores['neutral_winter'] += 2
    elif hair['color'] == 'medium':
        if 'auburn' in hair['specific_color'] or 'strawberry' in hair['specific_color']:
            scores['warm_spring'] += 3
            scores['bright_spring'] += 2
        elif 'ash' in hair['specific_color']:
            scores['cool_summer'] += 3
            scores['neutral_summer'] += 2
        else:
            scores['warm_autumn'] += 2
            scores['neutral_winter'] += 2
    else:  # light hair
        if 'golden' in hair['specific_color'] or 'honey' in hair['specific_color']:
            scores['warm_spring'] += 3
            scores['bright_spring'] += 2
        elif 'platinum' in hair['specific_color'] or 'ash' in hair['specific_color']:
            scores['cool_summer'] += 3
            scores['neutral_summer'] += 2
        else:
            scores['bright_spring'] += 2
            scores['cool_summer'] += 2
    
    # Eye color scoring
    if eye['color'] == 'dark':
        if 'brown' in eye['specific_color']:
            if eye['warmth'] > 10:
                scores['deep_autumn'] += 2
                scores['warm_autumn'] += 2
            else:
                scores['cool_winter'] += 2
                scores['neutral_winter'] += 2
    elif eye['color'] == 'medium':
        if 'hazel' in eye['specific_color']:
            scores['warm_spring'] += 2
            scores['warm_autumn'] += 2
        elif 'amber' in eye['specific_color']:
            scores['warm_spring'] += 3
            scores['bright_spring'] += 2
        else:
            scores['neutral_winter'] += 2
            scores['neutral_summer'] += 2
    else:  # light eyes
        if 'blue' in eye['specific_color']:
            scores['cool_winter'] += 2
            scores['cool_summer'] += 2
        elif 'green' in eye['specific_color']:
            scores['warm_spring'] += 2
            scores['bright_spring'] += 2
        else:
            scores['cool_summer'] += 2
            scores['neutral_summer'] += 2
    
    # Contrast scoring
    if skin['contrast'] == 'high':
        scores['cool_winter'] += 2
        scores['bright_spring'] += 2
        scores['deep_autumn'] += 2
    elif skin['contrast'] == 'low':
        scores['cool_summer'] += 2
        scores['neutral_summer'] += 2
    
    # Find the highest scoring color type
    best_match = max(scores, key=scores.get)
    max_score = scores[best_match]
    
    print(f"DEBUG - Color Type Scores: {scores}")
    print(f"DEBUG - Best Match: {best_match} (score: {max_score})")
    
    # If the best score is too low, use enhanced fallback
    if max_score < 3:
        print("DEBUG - Low confidence score, using enhanced fallback")
        return enhanced_fallback_analysis(skin, hair, eye)
    
    return best_match

def enhanced_fallback_analysis(skin, hair, eye):
    """Enhanced fallback analysis when primary scoring is inconclusive"""
    print("DEBUG - Using enhanced fallback analysis")
    
    # Check for very specific combinations
    if (skin['brightness'] > 140 and skin['warmth'] > 15 and 
        hair['color'] == 'light' and 'golden' in hair['specific_color']):
        return 'bright_spring'
    
    if (skin['brightness'] < 90 and skin['warmth'] > 20 and 
        hair['color'] == 'dark' and 'brown' in hair['specific_color']):
        return 'deep_autumn'
    
    if (skin['brightness'] > 130 and skin['warmth'] < -15 and 
        hair['color'] == 'light' and 'platinum' in hair['specific_color']):
        return 'cool_summer'
    
    if (skin['brightness'] < 100 and skin['warmth'] < -10 and 
        hair['color'] == 'dark' and 'black' in hair['specific_color']):
        return 'cool_winter'
    
    # Use weighted random based on skin characteristics
    if skin['brightness'] > 130:
        if skin['warmth'] > 10:
            return 'bright_spring'
        else:
            return 'cool_summer'
    elif skin['brightness'] > 110:
        if skin['warmth'] > 8:
            return 'warm_spring'
        else:
            return 'neutral_summer'
    elif skin['brightness'] > 90:
        if skin['warmth'] > 10:
            return 'warm_autumn'
        else:
            return 'neutral_winter'
    else:
        if skin['warmth'] > 15:
            return 'deep_autumn'
        else:
            return 'cool_winter'

def get_detailed_analysis_results(image_data):
    """Get detailed analysis results for display"""
    try:
        # Decode and open the image
        img = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        width, height = img.size
        
        # Define regions for analysis
        face_x1, face_y1 = int(width * 0.25), int(height * 0.25)
        face_x2, face_y2 = int(width * 0.75), int(height * 0.75)
        face_region = img.crop((face_x1, face_y1, face_x2, face_y2))
        
        hair_x1, hair_y1 = int(width * 0.1), int(height * 0.05)
        hair_x2, hair_y2 = int(width * 0.9), int(height * 0.35)
        hair_region = img.crop((hair_x1, hair_y1, hair_x2, hair_y2))
        
        eye_x1, eye_y1 = int(width * 0.3), int(height * 0.3)
        eye_x2, eye_y2 = int(width * 0.7), int(height * 0.5)
        eye_region = img.crop((eye_x1, eye_y1, eye_x2, eye_y2))
        
        # Analyze each region
        skin_analysis = analyze_skin_tone(face_region)
        hair_analysis = analyze_hair_color(hair_region)
        eye_analysis = analyze_eye_color(eye_region)
        
        return {
            'skin': {
                'brightness': round(skin_analysis['brightness'], 1),
                'warmth': round(skin_analysis['warmth'], 1),
                'contrast': skin_analysis['contrast'],
                'undertone': 'warm' if skin_analysis['warmth'] > 5 else 'cool' if skin_analysis['warmth'] < -5 else 'neutral'
            },
            'hair': {
                'color': hair_analysis['specific_color'].replace('_', ' ').title(),
                'brightness': round(hair_analysis['brightness'], 1),
                'warmth': round(hair_analysis['warmth'], 1),
                'category': hair_analysis['color']
            },
            'eyes': {
                'color': eye_analysis['specific_color'].replace('_', ' ').title(),
                'brightness': round(eye_analysis['brightness'], 1),
                'warmth': round(eye_analysis['warmth'], 1),
                'category': eye_analysis['color']
            }
        }
        
    except Exception as e:
        print(f"Error in detailed analysis: {e}")
        return {
            'skin': {'brightness': 0, 'warmth': 0, 'contrast': 'unknown', 'undertone': 'unknown'},
            'hair': {'color': 'Unknown', 'brightness': 0, 'warmth': 0, 'category': 'unknown'},
            'eyes': {'color': 'Unknown', 'brightness': 0, 'warmth': 0, 'category': 'unknown'}
        }

def generate_face_analysis(color_type):
    """Generate personalized face analysis based on color type"""
    analyses = {
        'cool_winter': {
            'complexion': 'bright and cool with blue undertones, high contrast',
            'eyes': 'striking and high contrast, often blue, gray, or dark brown',
            'hair': 'likely dark brown, black, or cool-toned with natural shine',
            'features': 'sharp and defined with clear facial structure'
        },
        'neutral_winter': {
            'complexion': 'balanced with neutral undertones, medium contrast',
            'eyes': 'versatile and adaptable, often hazel or medium brown',
            'hair': 'medium contrast with neutral tones, natural depth',
            'features': 'harmonious and balanced with elegant proportions'
        },
        'bright_spring': {
            'complexion': 'warm and bright with golden undertones, clear glow',
            'eyes': 'vibrant and energetic, often bright blue, green, or amber',
            'hair': 'likely warm-toned with brightness, natural highlights',
            'features': 'clear and lively with animated expressions'
        },
        'warm_spring': {
            'complexion': 'warm and golden with natural glow, fresh appearance',
            'eyes': 'warm and inviting, often golden brown, hazel, or warm green',
            'hair': 'warm-toned with natural highlights, golden or strawberry tones',
            'features': 'fresh and natural with approachable warmth'
        },
        'cool_summer': {
            'complexion': 'soft and cool with blue undertones, gentle appearance',
            'eyes': 'gentle and refined, often soft blue, gray, or cool brown',
            'hair': 'likely cool-toned with softness, ash brown or cool blonde',
            'features': 'delicate and elegant with refined beauty'
        },
        'neutral_summer': {
            'complexion': 'balanced soft with neutral undertones, sophisticated glow',
            'eyes': 'harmonious and elegant, often medium brown or hazel',
            'hair': 'medium contrast with neutral tones, natural sophistication',
            'features': 'balanced and sophisticated with timeless beauty'
        },
        'warm_autumn': {
            'complexion': 'warm and rich with golden undertones, natural warmth',
            'eyes': 'deep and earthy, often warm brown, amber, or hazel',
            'hair': 'warm-toned with rich depth, auburn or golden brown',
            'features': 'rich and natural with earthy beauty'
        },
        'deep_autumn': {
            'complexion': 'deep and rich with warm undertones, dramatic contrast',
            'eyes': 'dramatic and intense, often dark brown or deep hazel',
            'hair': 'likely dark with warm undertones, rich chocolate or black',
            'features': 'dramatic and striking with powerful presence'
        }
    }
    
    return analyses.get(color_type, analyses['neutral_winter'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Analyze the image
        color_type = analyze_image_features(image_data)
        color_info = COLOR_TYPES[color_type]
        face_analysis = generate_face_analysis(color_type)
        
        # Get detailed analysis results for display
        detailed_analysis = get_detailed_analysis_results(image_data)
        
        # Generate recommendations
        recommendations = {
            'color_type': color_info,
            'face_analysis': face_analysis,
            'detailed_analysis': detailed_analysis,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(recommendations)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
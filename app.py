from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
from PIL import Image
import io
import json
import random
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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
    """Analyze hair color characteristics"""
    colors = hair_region.getcolors(1000)
    if not colors:
        return {'brightness': 80, 'warmth': 0, 'color': 'unknown'}
    
    # Get dominant hair colors
    dominant_colors = [color for count, color in colors if count > 50]
    if not dominant_colors:
        dominant_colors = [color for count, color in colors[:5]]
    
    # Calculate hair characteristics
    avg_r = sum(color[0] for color in dominant_colors) / len(dominant_colors)
    avg_g = sum(color[1] for color in dominant_colors) / len(dominant_colors)
    avg_b = sum(color[2] for color in dominant_colors) / len(dominant_colors)
    
    brightness = (avg_r + avg_g + avg_b) / 3
    warmth = avg_r - avg_b
    
    # Determine hair color category
    if brightness < 60:
        color = 'dark'
    elif brightness < 100:
        color = 'medium'
    else:
        color = 'light'
    
    return {
        'brightness': brightness,
        'warmth': warmth,
        'color': color
    }

def analyze_eye_color(eye_region):
    """Analyze eye color characteristics"""
    colors = eye_region.getcolors(500)
    if not colors:
        return {'brightness': 80, 'warmth': 0, 'color': 'unknown'}
    
    # Get dominant eye colors
    dominant_colors = [color for count, color in colors if count > 20]
    if not dominant_colors:
        dominant_colors = [color for count, color in colors[:3]]
    
    # Calculate eye characteristics
    avg_r = sum(color[0] for color in dominant_colors) / len(dominant_colors)
    avg_g = sum(color[1] for color in dominant_colors) / len(dominant_colors)
    avg_b = sum(color[2] for color in dominant_colors) / len(dominant_colors)
    
    brightness = (avg_r + avg_g + avg_b) / 3
    warmth = avg_r - avg_b
    
    # Determine eye color category
    if brightness < 70:
        color = 'dark'
    elif brightness < 120:
        color = 'medium'
    else:
        color = 'light'
    
    return {
        'brightness': brightness,
        'warmth': warmth,
        'color': color
    }

def determine_color_type_accurate(skin, hair, eye):
    """Determine color type based on traditional color analysis principles"""
    
    # Traditional color analysis logic:
    # Dark hair + dark eyes = Winter palette
    # Light hair + light eyes = Spring/Summer palette
    # Medium features = Autumn palette
    
    # Check for Winter characteristics (dark features, high contrast)
    if (hair['color'] == 'dark' and eye['color'] == 'dark' and 
        skin['contrast'] == 'high' and skin['brightness'] < 130):
        if skin['warmth'] > 10:
            return 'neutral_winter'
        else:
            return 'cool_winter'
    
    # Check for Spring characteristics (light features, warm undertones)
    elif (hair['color'] == 'light' and eye['color'] == 'light' and 
          skin['warmth'] > 15 and skin['brightness'] > 140):
        return 'bright_spring'
    elif (hair['color'] in ['light', 'medium'] and 
          skin['warmth'] > 10 and skin['brightness'] > 120):
        return 'warm_spring'
    
    # Check for Summer characteristics (light features, cool undertones)
    elif (hair['color'] == 'light' and eye['color'] == 'light' and 
          skin['warmth'] < -10 and skin['brightness'] > 130):
        return 'cool_summer'
    elif (hair['color'] in ['light', 'medium'] and 
          skin['warmth'] < 5 and skin['brightness'] > 110):
        return 'neutral_summer'
    
    # Check for Autumn characteristics (medium features, warm undertones)
    elif (hair['color'] == 'medium' and eye['color'] == 'medium' and 
          skin['warmth'] > 10 and skin['brightness'] < 120):
        return 'warm_autumn'
    elif (hair['color'] == 'dark' and skin['warmth'] > 15 and 
          skin['brightness'] < 100):
        return 'deep_autumn'
    
    # Fallback logic based on skin characteristics
    if skin['brightness'] > 140:
        if skin['warmth'] > 10:
            return 'bright_spring'
        else:
            return 'cool_summer'
    elif skin['brightness'] > 110:
        if skin['warmth'] > 10:
            return 'warm_spring'
        else:
            return 'neutral_summer'
    elif skin['brightness'] > 80:
        if skin['warmth'] > 10:
            return 'warm_autumn'
        else:
            return 'neutral_winter'
    else:
        if skin['warmth'] > 10:
            return 'deep_autumn'
        else:
            return 'cool_winter'

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
        
        # Generate recommendations
        recommendations = {
            'color_type': color_info,
            'face_analysis': face_analysis,
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
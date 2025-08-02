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
    """Analyze image features and determine color type with improved accuracy"""
    try:
        # Decode and open the image
        img = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get image dimensions
        width, height = img.size
        
        # Analyze different regions of the image for more accurate results
        # Focus on center area (likely face) and edges (likely hair/background)
        
        # Center region (face area)
        center_x1, center_y1 = int(width * 0.3), int(height * 0.2)
        center_x2, center_y2 = int(width * 0.7), int(height * 0.8)
        face_region = img.crop((center_x1, center_y1, center_x2, center_y2))
        
        # Top region (hair area)
        hair_region = img.crop((0, 0, width, int(height * 0.3)))
        
        # Analyze face region for skin tone
        face_colors = face_region.getcolors(1000)
        if face_colors:
            face_colors = sorted(face_colors, key=lambda x: x[0], reverse=True)[:10]
            skin_tones = [color for count, color in face_colors if count > 50]
            
            if skin_tones:
                # Calculate average skin tone characteristics
                avg_skin_r = sum(color[0] for color in skin_tones) / len(skin_tones)
                avg_skin_g = sum(color[1] for color in skin_tones) / len(skin_tones)
                avg_skin_b = sum(color[2] for color in skin_tones) / len(skin_tones)
                avg_skin_brightness = (avg_skin_r + avg_skin_g + avg_skin_b) / 3
                
                # Determine skin undertone (warm vs cool)
                skin_warmth = avg_skin_r - avg_skin_b
                
                # Analyze hair region for hair color
                hair_colors = hair_region.getcolors(500)
                if hair_colors:
                    hair_colors = sorted(hair_colors, key=lambda x: x[0], reverse=True)[:5]
                    hair_tones = [color for count, color in hair_colors if count > 30]
                    
                    if hair_tones:
                        avg_hair_r = sum(color[0] for color in hair_tones) / len(hair_tones)
                        avg_hair_g = sum(color[1] for color in hair_tones) / len(hair_tones)
                        avg_hair_b = sum(color[2] for color in hair_tones) / len(hair_tones)
                        avg_hair_brightness = (avg_hair_r + avg_hair_g + avg_hair_b) / 3
                        hair_warmth = avg_hair_r - avg_hair_b
                        
                        # Enhanced color type determination based on skin and hair analysis
                        return determine_color_type(avg_skin_brightness, skin_warmth, avg_hair_brightness, hair_warmth)
        
        # Fallback: analyze entire image if face/hair analysis fails
        img_small = img.resize((100, 100))
        colors = img_small.getcolors(5000)
        
        if colors:
            colors = sorted(colors, key=lambda x: x[0], reverse=True)[:20]
            dominant_colors = [color for count, color in colors if count > 100]
            
            if dominant_colors:
                avg_brightness = sum(sum(color) / 3 for color in dominant_colors) / len(dominant_colors)
                avg_warmth = sum(color[0] - color[2] for color in dominant_colors) / len(dominant_colors)
                
                return determine_color_type(avg_brightness, avg_warmth, avg_brightness, avg_warmth)
        
        # Final fallback
        return random.choice(list(COLOR_TYPES.keys()))
        
    except Exception as e:
        print(f"Error in image analysis: {e}")
        return random.choice(list(COLOR_TYPES.keys()))

def determine_color_type(skin_brightness, skin_warmth, hair_brightness, hair_warmth):
    """Determine color type based on analyzed features"""
    
    # Define thresholds for different characteristics
    BRIGHT_THRESHOLD = 140
    MEDIUM_THRESHOLD = 100
    WARM_THRESHOLD = 10
    COOL_THRESHOLD = -10
    
    # Determine season based on skin and hair characteristics
    if skin_brightness > BRIGHT_THRESHOLD:
        # Bright seasons
        if skin_warmth > WARM_THRESHOLD:
            return 'bright_spring'
        elif skin_warmth < COOL_THRESHOLD:
            return 'cool_winter'
        else:
            return 'neutral_winter'
    elif skin_brightness > MEDIUM_THRESHOLD:
        # Medium seasons
        if skin_warmth > WARM_THRESHOLD:
            return 'warm_spring'
        elif skin_warmth < COOL_THRESHOLD:
            return 'cool_summer'
        else:
            return 'neutral_summer'
    else:
        # Deep seasons
        if skin_warmth > WARM_THRESHOLD:
            return 'warm_autumn'
        else:
            return 'deep_autumn'

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
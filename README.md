# ✨ Personal Color Analysis ✨

A beautiful, trendy web application that analyzes your personal color palette based on your uploaded selfie! Built with a Mean Girls theme and scrapbook aesthetic that's perfect for Gen Z users.

![Personal Color Analysis](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **Image Upload**: Drag & drop or click to upload your selfie
- **Advanced Color Analysis**: Get your personal color type with detailed analysis
- **Detailed Hair & Eye Detection**: Specific color identification (Golden Blonde, Ash Blonde, Green, Dark Gray, etc.)
- **Face Analysis**: Comprehensive analysis of your complexion, eyes, hair, and features
- **Personalized Recommendations**: Clothing and makeup color suggestions
- **Detailed Measurements**: Brightness, warmth, and undertone analysis for all features
- **Score-Based Algorithm**: Advanced color type determination using multiple factors
- **Beautiful UI**: Mean Girls theme with pink colors and scrapbook text
- **Responsive Design**: Works perfectly on all devices
- **Fun Animations**: Engaging interactions and smooth transitions

## 🎨 Color Types

The app analyzes your features and categorizes you into one of these color types:

- **Cool Winter**: Bright, cool complexion with blue undertones
- **Neutral Winter**: Balanced cool-warm complexion
- **Bright Spring**: Warm, bright complexion with golden undertones
- **Warm Spring**: Warm, golden complexion with natural glow
- **Cool Summer**: Soft, cool complexion with blue undertones
- **Neutral Summer**: Balanced soft complexion
- **Warm Autumn**: Warm, rich complexion with golden undertones
- **Deep Autumn**: Deep, rich complexion with warm undertones

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/linnfire/PalettePicker.git
   cd PalettePicker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

### Using the Startup Script

For easier setup, use the provided startup script:
```bash
chmod +x start.sh
./start.sh
```

## 🌐 Live Demo

Visit the demo page: [Demo](demo.html)

## 📱 How to Use

1. **Upload Your Selfie**: Click the upload area or drag & drop your image
2. **Preview Image**: See your uploaded image immediately
3. **Analyze**: Click "Analyze My Colors!" to process your image
4. **View Results**: See your color type, face analysis, and recommendations
5. **Share**: Share your results with friends!

## 🛠️ Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Image Processing**: PIL (Python Imaging Library)
- **AI Integration**: Google Gemini API for advanced analysis
- **Color Analysis**: Advanced algorithm with score-based determination
- **Styling**: Custom CSS with Mean Girls theme
- **Fonts**: Google Fonts (Pacifico, Indie Flower, Quicksand)

## 🎯 Current Features & Enhancements

- **✅ AI Integration**: Gemini API integration for advanced image analysis
- **✅ Detailed Color Detection**: Specific hair and eye color identification
- **✅ Score-Based Algorithm**: Advanced color type determination using multiple factors
- **✅ Enhanced Accuracy**: Eliminated bias and improved analysis precision
- **✅ Detailed Measurements**: Brightness, warmth, and undertone analysis
- **✅ Social Features**: Share results with friends
- **✅ Responsive UI**: Beautiful detailed analysis cards

## 🚀 Future Enhancements

- **Color Palette Generator**: Create custom palettes based on analysis
- **Makeup Recommendations**: Specific product suggestions
- **Clothing Suggestions**: Outfit recommendations based on color type
- **Advanced AI**: Machine learning for even more accurate analysis

## 🎨 Theme Details

The application features:
- **Mean Girls aesthetic** with pink color scheme
- **Scrapbook text format** with handwritten fonts
- **Teenage girl style** with trendy elements
- **Fun animations** and interactive elements
- **Gen Z friendly** design and language

## 📁 Project Structure

```
PalettePicker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── start.sh              # Easy startup script
├── demo.html             # Demo page
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   └── images/           # Image assets
└── uploads/              # Uploaded images (auto-created)
```

## 🔧 Customization

### Adding New Color Types

Edit the `COLOR_TYPES` dictionary in `app.py` to add new color categories:

```python
'new_color_type': {
    'name': 'New Color Type',
    'description': 'Description of the color type',
    'characteristics': 'Key characteristics',
    'clothing': ['Color 1', 'Color 2', 'Color 3'],
    'makeup': ['Makeup 1', 'Makeup 2', 'Makeup 3'],
    'avoid': ['Avoid 1', 'Avoid 2', 'Avoid 3']
}
```

### Styling Changes

Modify `static/css/style.css` to customize the appearance:
- Change colors in the CSS variables
- Update fonts in the font-family properties
- Modify animations and transitions

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Image upload fails**: Check file size and format (supports JPG, PNG, GIF)

3. **Analysis not working**: Ensure all dependencies are installed correctly

### Debug Mode

The app runs in debug mode by default. For production, set `debug=False` in `app.py`.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Add more color types
- Improve the analysis algorithm
- Add new features
- Enhance the UI/UX
- Add tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the Mean Girls aesthetic
- Built for all the fabulous people who want to discover their perfect color palette
- Special thanks to the color analysis community

## 💖 Made with Love

Built for all the fabulous people who want to discover their perfect color palette! ✨

---

**Note**: This is a demo application. For production use, consider implementing proper security measures, error handling, and AI integration for more accurate color analysis.

## 🔗 Links

- **Repository**: https://github.com/linnfire/PalettePicker
- **Issues**: https://github.com/linnfire/PalettePicker/issues
- **Demo**: Open `demo.html` in your browser 
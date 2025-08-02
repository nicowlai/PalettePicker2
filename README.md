# ✨ Personal Color Analysis ✨

A beautiful, trendy web application that analyzes your personal color palette based on your uploaded selfie! Built with a Mean Girls theme and scrapbook aesthetic that's perfect for Gen Z users.

## 🌟 Features

- **Image Upload**: Drag & drop or click to upload your selfie
- **Color Analysis**: Get your personal color type (16-color system)
- **Face Analysis**: Detailed analysis of your complexion, eyes, hair, and features
- **Personalized Recommendations**: Clothing and makeup color suggestions
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

### Installation

1. **Clone or download the project**
   ```bash
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

## 📱 How to Use

1. **Upload Your Selfie**: Click the upload area or drag & drop your image
2. **Analyze**: Click "Analyze My Colors!" to process your image
3. **View Results**: See your color type, face analysis, and recommendations
4. **Share**: Share your results with friends!

## 🛠️ Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Image Processing**: PIL (Python Imaging Library)
- **Styling**: Custom CSS with Mean Girls theme
- **Fonts**: Google Fonts (Pacifico, Indie Flower, Quicksand)

## 🎯 Future Enhancements

- **AI Integration**: Use machine learning for more accurate analysis
- **Gemini API**: Integrate with Google's Gemini API for advanced image analysis
- **Social Features**: Share results on social media
- **Color Palette Generator**: Create custom palettes based on analysis
- **Makeup Recommendations**: Specific product suggestions
- **Clothing Suggestions**: Outfit recommendations based on color type

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
├── README.md             # Project documentation
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

Feel free to contribute to this project! Some ideas:
- Add more color types
- Improve the analysis algorithm
- Add new features
- Enhance the UI/UX

## 📄 License

This project is open source and available under the MIT License.

## 💖 Made with Love

Built for all the fabulous people who want to discover their perfect color palette! ✨

---

**Note**: This is a demo application. For production use, consider implementing proper security measures, error handling, and AI integration for more accurate color analysis. 
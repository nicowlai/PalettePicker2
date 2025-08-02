// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const uploadedImage = document.getElementById('uploadedImage');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const shareBtn = document.getElementById('shareBtn');

// Upload preview elements
const uploadContent = document.getElementById('uploadContent');
const uploadedImagePreview = document.getElementById('uploadedImagePreview');
const uploadedImagePreviewImg = document.querySelector('#uploadedImagePreview img');
const changeImageBtn = document.getElementById('changeImageBtn');

// Results elements
const colorTypeName = document.getElementById('colorTypeName');
const colorDescription = document.getElementById('colorDescription');
const complexion = document.getElementById('complexion');
const eyes = document.getElementById('eyes');
const hair = document.getElementById('hair');
const features = document.getElementById('features');
const clothingColors = document.getElementById('clothingColors');
const makeupColors = document.getElementById('makeupColors');
const avoidColors = document.getElementById('avoidColors');

// Detailed analysis elements
const skinColor = document.getElementById('skinColor');
const skinBrightness = document.getElementById('skinBrightness');
const skinWarmth = document.getElementById('skinWarmth');
const skinUndertone = document.getElementById('skinUndertone');
const skinContrast = document.getElementById('skinContrast');
const hairColor = document.getElementById('hairColor');
const hairBrightness = document.getElementById('hairBrightness');
const hairWarmth = document.getElementById('hairWarmth');
const hairCategory = document.getElementById('hairCategory');
const eyeColor = document.getElementById('eyeColor');
const eyeBrightness = document.getElementById('eyeBrightness');
const eyeWarmth = document.getElementById('eyeWarmth');
const eyeCategory = document.getElementById('eyeCategory');

let uploadedImageData = null;

// Event Listeners
uploadArea.addEventListener('click', () => imageInput.click());
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('drop', handleDrop);
imageInput.addEventListener('change', handleFileSelect);
analyzeBtn.addEventListener('click', analyzeImage);
newAnalysisBtn.addEventListener('click', resetToUpload);
shareBtn.addEventListener('click', shareResults);
changeImageBtn.addEventListener('click', () => imageInput.click());

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#ff69b4';
    uploadArea.style.background = 'rgba(255, 182, 193, 0.2)';
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#ffb3d9';
    uploadArea.style.background = 'rgba(255, 255, 255, 0.5)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// File Selection Handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// File Processing
function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        showNotification('Please select an image file!', 'error');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        uploadedImageData = e.target.result;
        
        // Show image preview in upload area
        uploadedImagePreviewImg.src = uploadedImageData;
        uploadedImagePreview.style.display = 'block';
        uploadContent.style.display = 'none';
        
        // Also set the image for results section
        uploadedImage.src = uploadedImageData;
        
        // Enable analyze button
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = '1';
        
        // Add success animation
        uploadArea.style.transform = 'scale(1.05)';
        setTimeout(() => {
            uploadArea.style.transform = 'scale(1)';
        }, 200);
        
        showNotification('Image uploaded successfully! ✨', 'success');
    };
    reader.readAsDataURL(file);
}

// Image Analysis
async function analyzeImage() {
    if (!uploadedImageData) {
        showNotification('Please upload an image first!', 'error');
        return;
    }
    
    // Show loading
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: uploadedImageData
            })
        });
        
        if (!response.ok) {
            throw new Error('Analysis failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        showNotification('Analysis failed. Please try again!', 'error');
        resetToUpload();
    }
}

// Display Results
function displayResults(data) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Update color type
    colorTypeName.textContent = data.color_type.name;
    colorDescription.textContent = data.color_type.description;
    
    // Update face analysis
    complexion.textContent = data.face_analysis.complexion;
    eyes.textContent = data.face_analysis.eyes;
    hair.textContent = data.face_analysis.hair;
    features.textContent = data.face_analysis.features;
    
    // Update detailed analysis if available
    if (data.detailed_analysis) {
        // Skin analysis
        skinColor.textContent = `${data.detailed_analysis.skin.undertone} undertone`;
        skinBrightness.textContent = data.detailed_analysis.skin.brightness;
        skinWarmth.textContent = data.detailed_analysis.skin.warmth;
        skinUndertone.textContent = data.detailed_analysis.skin.undertone;
        skinContrast.textContent = data.detailed_analysis.skin.contrast;
        
        // Hair analysis
        hairColor.textContent = data.detailed_analysis.hair.color;
        hairBrightness.textContent = data.detailed_analysis.hair.brightness;
        hairWarmth.textContent = data.detailed_analysis.hair.warmth;
        hairCategory.textContent = data.detailed_analysis.hair.category;
        
        // Eye analysis
        eyeColor.textContent = data.detailed_analysis.eyes.color;
        eyeBrightness.textContent = data.detailed_analysis.eyes.brightness;
        eyeWarmth.textContent = data.detailed_analysis.eyes.warmth;
        eyeCategory.textContent = data.detailed_analysis.eyes.category;
    }
    
    // Update recommendations
    updateColorTags(clothingColors, data.color_type.clothing);
    updateColorTags(makeupColors, data.color_type.makeup);
    updateColorTags(avoidColors, data.color_type.avoid);
    
    // Add celebration animation
    resultsSection.style.animation = 'fadeIn 0.8s ease-out';
    
    showNotification('Your color analysis is ready! 🎉', 'success');
}

// Update Color Tags
function updateColorTags(container, colors) {
    container.innerHTML = '';
    colors.forEach(color => {
        const tag = document.createElement('span');
        tag.className = 'color-tag';
        tag.textContent = color;
        container.appendChild(tag);
    });
}

// Reset to Upload
function resetToUpload() {
    resultsSection.style.display = 'none';
    uploadSection.style.display = 'block';
    uploadedImageData = null;
    uploadedImage.src = '';
    uploadedImagePreviewImg.src = '';
    uploadedImagePreview.style.display = 'none';
    uploadContent.style.display = 'block';
    analyzeBtn.disabled = true;
    imageInput.value = '';
    
    // Reset upload area
    uploadArea.style.borderColor = '#ffb3d9';
    uploadArea.style.background = 'rgba(255, 255, 255, 0.5)';
}

// Share Results
function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'My Personal Color Analysis',
            text: `I just discovered I'm a ${colorTypeName.textContent}! Check out my perfect color palette! ✨`,
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        const text = `I just discovered I'm a ${colorTypeName.textContent}! Check out my perfect color palette! ✨`;
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Results copied to clipboard! 📋', 'success');
        });
    }
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#ff6b6b' : type === 'success' ? '#51cf66' : '#ff69b4'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
    `;
    
    // Add close functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.remove();
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
    
    document.body.appendChild(notification);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: background 0.2s ease;
    }
    
    .notification-close:hover {
        background: rgba(255, 255, 255, 0.2);
    }
`;
document.head.appendChild(style);

// Add some fun Easter eggs
document.addEventListener('DOMContentLoaded', () => {
    // Add sparkle effect to title
    const title = document.querySelector('.main-title');
    title.addEventListener('mouseenter', () => {
        title.style.transform = 'scale(1.05)';
        title.style.transition = 'transform 0.3s ease';
    });
    
    title.addEventListener('mouseleave', () => {
        title.style.transform = 'scale(1)';
    });
    
    // Add fun hover effects to color tags
    document.addEventListener('mouseover', (e) => {
        if (e.target.classList.contains('color-tag')) {
            e.target.style.transform = 'scale(1.1) rotate(2deg)';
        }
    });
    
    document.addEventListener('mouseout', (e) => {
        if (e.target.classList.contains('color-tag')) {
            e.target.style.transform = 'scale(1) rotate(0deg)';
        }
    });
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'u':
                e.preventDefault();
                imageInput.click();
                break;
            case 'Enter':
                if (!analyzeBtn.disabled) {
                    e.preventDefault();
                    analyzeImage();
                }
                break;
        }
    }
});

// Add some fun loading messages
const loadingMessages = [
    "This is so fetch! 🔮",
    "Analyzing your fabulous features... ✨",
    "Finding your perfect palette... 💅",
    "Working some magic... 🪄",
    "Almost there, queen! 👑"
];

let loadingMessageIndex = 0;
const loadingText = document.querySelector('.loading-card p');

if (loadingText) {
    setInterval(() => {
        loadingText.textContent = loadingMessages[loadingMessageIndex];
        loadingMessageIndex = (loadingMessageIndex + 1) % loadingMessages.length;
    }, 2000);
} 
#!/bin/bash
# Setup script to create a Mac application

echo "🍎 Sprint Analyzer - Mac App Builder"
echo "====================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.8 or higher from:"
    echo "https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install required packages
echo "📦 Installing required packages..."
pip3 install --break-system-packages pandas openpyxl pillow

# Create the app bundle structure
echo ""
echo "📁 Creating Mac app bundle..."

APP_NAME="Sprint Analyzer"
APP_DIR="$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

# Remove existing app if present
if [ -d "$APP_DIR" ]; then
    rm -rf "$APP_DIR"
fi

# Create directory structure
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"
mkdir -p "$RESOURCES_DIR/automation"
mkdir -p "$RESOURCES_DIR/config"

# Copy Python script
cp SprintAnalyzer_Mac.py "$MACOS_DIR/sprint_analyzer"

# Copy automation modules
cp automation/*.py "$RESOURCES_DIR/automation/"

# Copy config files
cp config/*.yaml "$RESOURCES_DIR/config/"

# Create launcher script
cat > "$MACOS_DIR/SprintAnalyzer" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$SCRIPT_DIR/../Resources"
export PYTHONPATH="$RESOURCES_DIR:$PYTHONPATH"
cd "$RESOURCES_DIR"
python3 "$SCRIPT_DIR/sprint_analyzer"
EOF

chmod +x "$MACOS_DIR/SprintAnalyzer"

# Create Info.plist
cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>SprintAnalyzer</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.youxel.sprintanalyzer</string>
    <key>CFBundleName</key>
    <string>Sprint Analyzer</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>xlsx</string>
                <string>xlsm</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>Excel Document</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>
EOF

# Create a simple icon (text-based)
echo "🎨 Creating app icon..."
python3 << 'PYTHON_SCRIPT'
from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple icon
size = 512
img = Image.new('RGB', (size, size), color='#3B82F6')
draw = ImageDraw.Draw(img)

# Draw emoji-style icon
try:
    # Try to use system font
    font = ImageFont.truetype("/System/Library/Fonts/AppleColorEmoji.ttf", 300)
except:
    font = None

# Draw text
text = "📊"
if font:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
else:
    text_width = size * 0.6
    text_height = size * 0.6

x = (size - text_width) / 2
y = (size - text_height) / 2 - 20

if font:
    draw.text((x, y), text, font=font)
else:
    draw.text((size//4, size//4), "SA", fill='white', font=None)

# Save as PNG first
img.save('icon.png', 'PNG')

# Convert to iconset
os.system('mkdir -p icon.iconset')
for s in [16, 32, 64, 128, 256, 512]:
    resized = img.resize((s, s), Image.Resampling.LANCZOS)
    resized.save(f'icon.iconset/icon_{s}x{s}.png')
    if s <= 256:
        resized2x = img.resize((s*2, s*2), Image.Resampling.LANCZOS)
        resized2x.save(f'icon.iconset/icon_{s}x{s}@2x.png')

print("Icon created successfully")
PYTHON_SCRIPT

# Convert iconset to icns using system tool
if command -v iconutil &> /dev/null; then
    iconutil -c icns icon.iconset -o "$RESOURCES_DIR/icon.icns"
    rm -rf icon.iconset icon.png
else
    echo "⚠️  iconutil not found, skipping icon conversion"
fi

echo ""
echo "✅ Mac application created successfully!"
echo ""
echo "📍 Location: $APP_DIR"
echo ""
echo "To use:"
echo "1. Double-click '$APP_DIR' to open"
echo "2. Select your Excel file"
echo "3. Click 'Process Sprint Data'"
echo "4. Get your analyzed file!"
echo ""
echo "💡 Tip: Drag '$APP_DIR' to your Applications folder or Desktop"
echo ""
#!/bin/bash
# Setup script to create a Mac application

echo "🍎 Sprint Analyzer - Mac App Builder"
echo "====================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.8 or higher from:"
    echo "https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install required packages
echo "📦 Installing required packages..."
pip3 install --break-system-packages pandas openpyxl pyyaml 2>/dev/null || pip3 install pandas openpyxl pyyaml

# Try to install Pillow for icon creation (optional)
pip3 install --break-system-packages pillow 2>/dev/null || pip3 install pillow 2>/dev/null || echo "⚠️  Pillow not installed, will skip custom icon"

# Create the app bundle structure
echo ""
echo "📁 Creating Mac app bundle..."

APP_NAME="Sprint Analyzer"
APP_DIR="$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

# Remove existing app if present
if [ -d "$APP_DIR" ]; then
    rm -rf "$APP_DIR"
fi

# Create directory structure
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"
mkdir -p "$RESOURCES_DIR/automation"
mkdir -p "$RESOURCES_DIR/config"

# Copy Python script
if [ ! -f "SprintAnalyzer_Mac.py" ]; then
    echo "❌ Error: SprintAnalyzer_Mac.py not found!"
    echo "Make sure you're in the correct directory."
    exit 1
fi

cp SprintAnalyzer_Mac.py "$MACOS_DIR/sprint_analyzer"

# Copy automation modules
if [ ! -d "automation" ]; then
    echo "❌ Error: automation/ folder not found!"
    exit 1
fi

cp automation/*.py "$RESOURCES_DIR/automation/" 2>/dev/null || echo "⚠️  Warning: No .py files in automation/"

# Create __init__.py for Python package
touch "$RESOURCES_DIR/automation/__init__.py"

# Copy config files
if [ -d "config" ]; then
    cp config/*.yaml "$RESOURCES_DIR/config/" 2>/dev/null || echo "⚠️  Warning: No .yaml files in config/"
else
    echo "⚠️  Warning: config/ folder not found, skipping config files"
fi

# Create launcher script
cat > "$MACOS_DIR/SprintAnalyzer" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES_DIR="$SCRIPT_DIR/../Resources"
export PYTHONPATH="$RESOURCES_DIR:$PYTHONPATH"
cd "$RESOURCES_DIR"
python3 "$SCRIPT_DIR/sprint_analyzer" 2>&1
EOF

chmod +x "$MACOS_DIR/SprintAnalyzer"

# Create Info.plist
cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>SprintAnalyzer</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundleIdentifier</key>
    <string>com.youxel.sprintanalyzer</string>
    <key>CFBundleName</key>
    <string>Sprint Analyzer</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>xlsx</string>
                <string>xlsm</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>Excel Document</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
        </dict>
    </array>
</dict>
</plist>
EOF

# Create a simple icon (optional - will skip if Pillow not available)
echo "🎨 Creating app icon..."
python3 << 'PYTHON_SCRIPT' 2>/dev/null || echo "⚠️  Skipping custom icon creation"
try:
    from PIL import Image, ImageDraw
    import os

    # Create a simple icon
    size = 512
    img = Image.new('RGB', (size, size), color='#3B82F6')
    draw = ImageDraw.Draw(img)
    
    # Draw simple text
    draw.text((size//4, size//4), "SA", fill='white')
    
    # Save as PNG first
    img.save('icon.png', 'PNG')
    
    # Convert to iconset
    os.system('mkdir -p icon.iconset')
    for s in [16, 32, 64, 128, 256, 512]:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f'icon.iconset/icon_{s}x{s}.png')
        if s <= 256:
            resized2x = img.resize((s*2, s*2), Image.Resampling.LANCZOS)
            resized2x.save(f'icon.iconset/icon_{s}x{s}@2x.png')
    
    print("Icon created successfully")
except ImportError:
    print("Pillow not available, skipping icon")
except Exception as e:
    print(f"Icon creation failed: {e}")
PYTHON_SCRIPT

# Convert iconset to icns using system tool
if command -v iconutil &> /dev/null && [ -d "icon.iconset" ]; then
    iconutil -c icns icon.iconset -o "$RESOURCES_DIR/icon.icns"
    rm -rf icon.iconset icon.png
fi

echo ""
echo "✅ Mac application created successfully!"
echo ""
echo "📍 Location: $APP_DIR"
echo ""
echo "To use:"
echo "1. Double-click '$APP_DIR' to open"
echo "2. Select your Excel file"
echo "3. Click 'Process Sprint Data'"
echo "4. Get your analyzed file!"
echo ""
echo "💡 Tip: Drag '$APP_DIR' to your Applications folder or Desktop"
echo ""
echo "🔍 If the app doesn't open:"
echo "   - Right-click the app → Open → Open (to bypass Mac security)"
echo "   - Check System Preferences → Security & Privacy"
echo ""


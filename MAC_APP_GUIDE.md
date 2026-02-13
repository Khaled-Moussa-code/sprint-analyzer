# 🍎 Sprint Analyzer - Mac App Setup Guide

## What You'll Get

A **double-clickable Mac application** that:
- ✅ Opens with a beautiful graphical interface
- ✅ No terminal commands needed
- ✅ Drag & drop or click to select files
- ✅ Shows real-time progress
- ✅ One-click to open results

---

## 📦 Setup (One-Time, 5 Minutes)

### Step 1: Download Files

Make sure you have all these files in a folder (e.g., `~/SprintAutomation`):

```
SprintAutomation/
├── SprintAnalyzer_Mac.py       ← Main app file
├── create_mac_app.sh           ← Setup script
├── automation/
│   ├── data_processor.py
│   ├── calculator.py
│   ├── excel_updater.py
│   └── notion_exporter.py
└── config/
    ├── team_mapping.yaml
    ├── kpi_weights.yaml
    └── cmmi_thresholds.yaml
```

### Step 2: Open Terminal

1. Press **⌘ + Space**
2. Type "Terminal"
3. Press **Enter**

### Step 3: Navigate to Your Folder

```bash
cd ~/SprintAutomation
```

(Replace `~/SprintAutomation` with your actual folder path)

### Step 4: Run the Setup Script

```bash
bash create_mac_app.sh
```

This will:
- ✅ Check for Python
- ✅ Install required packages
- ✅ Create the Mac app bundle
- ✅ Generate an icon
- ✅ Package everything together

You'll see output like:
```
🍎 Sprint Analyzer - Mac App Builder
=====================================

✓ Python 3 found: Python 3.11.5

📦 Installing required packages...
...
✅ Mac application created successfully!

📍 Location: Sprint Analyzer.app
```

### Step 5: Move to Applications (Optional but Recommended)

**Option A: Using Finder**
1. Open Finder
2. Find `Sprint Analyzer.app` in your folder
3. Drag it to **Applications** folder in the sidebar

**Option B: Using Terminal**
```bash
mv "Sprint Analyzer.app" /Applications/
```

---

## 🚀 Using the App

### Every Sprint (Super Easy!)

1. **Open the app**
   - Double-click `Sprint Analyzer.app` from Applications or Desktop
   
2. **A beautiful window opens with:**
   - 📊 Sprint Analysis title
   - Upload area with a folder icon
   
3. **Upload your file**
   - **Click** the upload area, or
   - **Drag & drop** your Excel file onto it
   
4. **Review file info**
   - File name, size, and sprint name are displayed
   
5. **Click "⚡ Process Sprint Data"**
   - Watch the progress bar
   - See real-time status updates
   
6. **Results appear!**
   - Summary metrics shown (staff count, KPIs, etc.)
   - Click "⬇️ Open Analyzed File" to see results
   
7. **Done!** Your Excel file is updated with all analysis

---

## 🎨 App Screenshots (What You'll See)

### 1. Welcome Screen
```
┌────────────────────────────────────────────┐
│         📊 Sprint Analysis                 │
│  Upload your Excel file and get instant    │
│              analysis                       │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │                                       │  │
│  │            📁                         │  │
│  │                                       │  │
│  │  Click to select your Sprint Excel   │  │
│  │              file                     │  │
│  │                                       │  │
│  │       or drag and drop here           │  │
│  │                                       │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  All processing happens locally on your    │
│        Mac. No data is sent anywhere.      │
└────────────────────────────────────────────┘
```

### 2. File Selected
```
┌────────────────────────────────────────────┐
│       📄 File Information                  │
│                                             │
│  File: Sprint_25_JAN_to_05_FEB.xlsx        │
│  Size: 285.2 KB                            │
│  Sprint: Check Now 26.17                   │
│                                             │
│        ┌──────────────────────┐            │
│        │ ⚡ Process Sprint Data│            │
│        └──────────────────────┘            │
└────────────────────────────────────────────┘
```

### 3. Processing
```
┌────────────────────────────────────────────┐
│       🔄 Processing...                     │
│                                             │
│  ████████████████████░░░░░  75%            │
│                                             │
│  [1/11] Loading workbook...                │
│  [2/11] Extracting sprint metadata...     │
│  [3/11] Processing Azure DevOps data...   │
│  [4/11] Validating data quality...        │
│  [5/11] Loading capacity data...          │
│  [6/11] Calculating staff metrics...      │
│  [7/11] Calculating team metrics...       │
│  [8/11] Computing CMMI measures...        │
│  ...                                        │
└────────────────────────────────────────────┘
```

### 4. Results
```
┌────────────────────────────────────────────┐
│       ✅ Analysis Complete!                │
│                                             │
│  Your sprint has been analyzed.            │
│  All KPIs and metrics have been calculated │
│                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  Staff   │ │  Teams   │ │ Avg Team │   │
│  │ Analyzed │ │Processed │ │   KPI    │   │
│  │    11    │ │    4     │ │   0.93   │   │
│  └──────────┘ └──────────┘ └──────────┘   │
│                                             │
│        ┌──────────────────────┐            │
│        │ ⬇️ Open Analyzed File │            │
│        └──────────────────────┘            │
│                                             │
│          Process Another File              │
└────────────────────────────────────────────┘
```

---

## 🆘 Troubleshooting

### "Sprint Analyzer can't be opened because it is from an unidentified developer"

This is a Mac security feature. Here's how to fix it:

**Method 1: Right-click to open**
1. Right-click (or Control+click) on `Sprint Analyzer.app`
2. Click "Open"
3. Click "Open" again in the dialog
4. App will open and remember this for future

**Method 2: System Preferences**
1. Open System Preferences
2. Go to Security & Privacy
3. Click "Open Anyway" next to the Sprint Analyzer message
4. Enter your password

### "Python 3 is not installed"

**Install Python:**
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from:
# https://www.python.org/downloads/
```

### "ModuleNotFoundError: No module named 'pandas'"

**Install missing packages:**
```bash
pip3 install --break-system-packages pandas openpyxl
```

### "Permission denied" when running create_mac_app.sh

**Make it executable:**
```bash
chmod +x create_mac_app.sh
```

### App window doesn't appear

**Check if Python has accessibility permissions:**
1. System Preferences → Security & Privacy → Privacy
2. Select "Accessibility" from the left
3. Add Python to the list (click + button)

### "No such file or directory: automation/data_processor.py"

**Make sure all files are in the correct structure:**
```bash
cd ~/SprintAutomation
ls -la automation/
ls -la config/
```

All `.py` files should be in `automation/` folder.

---

## 🎯 Features

### What the App Does

1. **Validates Your Data**
   - Checks for required columns
   - Validates data quality
   - Warns about potential issues

2. **Calculates Metrics**
   - 6 Staff KPIs per developer
   - 6 Team KPIs per team
   - 5 CMMI measures

3. **Updates Excel**
   - Creates new Analysis sheet
   - Updates KPI Indicators
   - Appends to historical tracking
   - Updates CMMI Template

4. **Uses Formulas**
   - All calculations are Excel formulas
   - Not hardcoded values
   - Workbook stays dynamic

### What Makes It Special

- ✅ **Native Mac App** - Looks and feels like a Mac app
- ✅ **Beautiful Interface** - Modern, clean design
- ✅ **Real-time Progress** - See exactly what's happening
- ✅ **Error Handling** - Clear error messages if something goes wrong
- ✅ **No Internet Required** - Everything happens locally
- ✅ **No Data Uploaded** - Your data never leaves your Mac

---

## 📁 File Structure After Setup

```
/Applications/
└── Sprint Analyzer.app/          ← Your double-clickable app!
    └── Contents/
        ├── Info.plist
        ├── MacOS/
        │   ├── SprintAnalyzer        ← Launcher
        │   └── sprint_analyzer       ← Python script
        └── Resources/
            ├── icon.icns             ← App icon
            ├── automation/
            │   ├── data_processor.py
            │   ├── calculator.py
            │   ├── excel_updater.py
            │   └── notion_exporter.py
            └── config/
                ├── team_mapping.yaml
                ├── kpi_weights.yaml
                └── cmmi_thresholds.yaml
```

---

## 🔄 Updating the App

If you need to update the automation logic:

1. **Edit the Python files** in your original folder
2. **Re-run the setup:**
   ```bash
   cd ~/SprintAutomation
   bash create_mac_app.sh
   ```
3. **Replace** the old app in Applications with the new one

---

## 💡 Tips

### Quick Access
- **Drag to Dock**: Drag `Sprint Analyzer.app` to your Dock for quick access
- **Desktop Shortcut**: Create an alias on your Desktop
- **Spotlight**: Just type "Sprint" in Spotlight (⌘+Space)

### Team Sharing
You can share the `Sprint Analyzer.app` with your team! Just:
1. Zip the app: Right-click → Compress
2. Share the `.zip` file
3. They unzip and double-click to use

### Keyboard Shortcuts
- **⌘+Q**: Quit the app
- **⌘+W**: Close the window
- **Click anywhere on upload area**: Opens file picker

---

## 🎊 You're All Set!

Your Mac app is ready to use. Just:
1. Double-click `Sprint Analyzer.app`
2. Select your Excel file
3. Click "Process"
4. Done!

No terminal, no commands, no complexity. Just a simple, beautiful Mac app. 🚀

---

## 📞 Need Help?

Common issues and solutions are in the Troubleshooting section above. For other issues, check:
- File permissions
- Python installation
- Package installation
- File structure

Happy sprint analyzing! 📊✨

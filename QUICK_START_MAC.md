# 🚀 Quick Start - Mac App (5-Minute Setup)

## ✅ Setup Checklist

### Before You Start
- [ ] All files downloaded from this chat
- [ ] Files organized in a folder (e.g., `~/SprintAutomation`)
- [ ] Python 3.8+ installed on your Mac

---

## 📋 Step-by-Step

### 1️⃣ Open Terminal
```
⌘ + Space → Type "Terminal" → Enter
```

### 2️⃣ Go to Your Folder
```bash
cd ~/SprintAutomation
```
*(Replace with your actual folder path)*

### 3️⃣ Run Setup
```bash
bash create_mac_app.sh
```

**What happens:**
- ✅ Checks Python
- ✅ Installs packages (pandas, openpyxl)
- ✅ Creates `Sprint Analyzer.app`
- ⏱️ Takes ~2 minutes

### 4️⃣ Move to Applications (Optional)
```bash
mv "Sprint Analyzer.app" /Applications/
```

---

## 🎯 Use the App (Every Sprint)

### Super Simple!

1. **Double-click** `Sprint Analyzer.app`
   
2. **Window opens** with upload area
   
3. **Click** to select your Excel file
   *(Or drag & drop)*
   
4. **Click** "⚡ Process Sprint Data"
   
5. **Wait** ~30 seconds while it processes
   
6. **Click** "⬇️ Open Analyzed File"
   
7. **Done!** Your Excel is updated ✨

---

## 📁 What You Need

```
SprintAutomation/
├── 📄 SprintAnalyzer_Mac.py
├── 📄 create_mac_app.sh
├── 📁 automation/
│   ├── data_processor.py
│   ├── calculator.py
│   ├── excel_updater.py
│   └── notion_exporter.py
└── 📁 config/
    ├── team_mapping.yaml
    ├── kpi_weights.yaml
    └── cmmi_thresholds.yaml
```

---

## 🆘 Quick Fixes

### "Can't open - unidentified developer"
**Right-click** app → **Open** → **Open** again

### "Python not found"
```bash
brew install python@3.11
```

### "Module not found"
```bash
pip3 install pandas openpyxl
```

---

## 🎨 What the App Looks Like

**Beautiful, modern interface with:**
- 📊 Clean design
- 📁 Drag & drop upload
- 📊 Real-time progress bar
- ✅ Success metrics display
- 🔵 Big, clear buttons

**No terminal needed after setup!**

---

## 💡 Pro Tips

1. **Pin to Dock** - Drag app to Dock for quick access
2. **Keyboard shortcut** - ⌘+Space, type "Sprint"
3. **Share with team** - Zip the app and send to colleagues
4. **Safe processing** - All data stays on your Mac

---

## ✨ That's It!

**Setup once** → **Use forever** → **Save hours** ⏰

Questions? Check `MAC_APP_GUIDE.md` for detailed help!

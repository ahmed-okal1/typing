# ⌨️ Typing Speed Trainer - مدرب الكتابة السريعة

A comprehensive bilingual (Arabic/English) typing speed trainer built with Python and Flet.

## Features

- 🌍 **Bilingual Support**: Full Arabic and English support with RTL text handling
- 👤 **User Profiles**: Personal profiles with level progression (1-100)
- 📚 **Text Library**: 15 built-in texts per language across 3 difficulty levels
- ➕ **Custom Texts**: Add your own practice texts
- ⚡ **Real-time Feedback**: Visual (color-coded) and audio feedback during typing
- 📊 **Comprehensive Scoring**: WPM, accuracy, and scores (1-100 scale)
- 📈 **Statistics**: Track your progress with detailed statistics
- 🎨 **Modern UI**: Beautiful dark theme with smooth interactions
- 💾 **Data Persistence**: All data automatically saved

## Installation

1. **Clone or download** this repository

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### First Time Setup
1. Enter your username
2. Select your preferred language (Arabic or English)
3. Click "Start"

### Taking a Typing Test
1. Click "Start Typing Test" from the main menu
2. Select difficulty level (Beginner, Intermediate, Advanced)
3. Choose language
4. Start typing and watch real-time feedback:
   - ✅ Green text = correct
   - ❌ Red text = incorrect
   - 🔊 Beep sound on errors
5. View your results and track your progress

### Managing Texts
- Add custom texts for practice
- Choose language and difficulty level
- All texts saved automatically

### Viewing Statistics
- Total tests completed
- Average WPM and accuracy
- Best scores
- Recent results history

## Scoring System

- **WPM (Words Per Minute)**: Standard calculation (characters ÷ 5 ÷ minutes)
- **Accuracy**: Percentage of correct characters
- **Speed Score**: 1-100 scale based on WPM
- **Accuracy Score**: 1-100 scale based on accuracy
- **Overall Score**: Average of speed and accuracy scores
- **Level**: Automatically increases based on performance

## Project Structure

typing/
├── main.py                 # Main application entry point
├── flet_typing_screen.py   # Typing test screen logic
├── ui_components.py        # UI screens (Welcome, Menu, Results, etc.)
├── data_manager.py         # Data persistence
├── typing_test.py          # Core test logic
├── requirements.txt        # Dependencies
├── data/                   # Data storage
│   ├── users.json
│   ├── texts_arabic.json
│   ├── texts_english.json
│   └── results.json
└── sounds/                 # Sound effects
```

## Requirements

- Python 3.7+
- Flet

## Features in Detail

### User Profile System
- First-time user registration
- Language preference
- Level tracking (1-100)
- Total tests counter

### Text Management
- **Arabic Texts**: 15 texts across 3 difficulty levels
- **English Texts**: 15 texts across 3 difficulty levels
- **Custom Texts**: Add unlimited custom texts
- Easy-to-edit JSON format

### Typing Test
- Real-time character comparison
- Color-coded feedback
- Audio feedback on errors
- Accurate timing
- Auto-finish when complete

### Results & Statistics
- Immediate results after each test
- Historical results tracking
- Performance statistics
- Level progression

## Screenshots

The application features a modern dark theme with:
- Clean, intuitive interface
- Bilingual labels throughout
- Color-coded feedback
- Smooth transitions

## Data Storage

All data is stored in JSON format in the `data/` directory:
- `users.json` - User profiles
- `texts_arabic.json` - Arabic text library
- `texts_english.json` - English text library
- `results.json` - Test results history

## Contributing

Feel free to:
- Add more texts to the libraries
- Suggest new features
- Report bugs
- Improve translations

## License

This project is open source and available for educational purposes.

## Author

Created with ❤️ for improving typing skills in both Arabic and English

---

**Happy Typing! 🎉**
**كتابة سعيدة! 🎉**

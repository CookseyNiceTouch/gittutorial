# Project Organizer

A simple tool to help editors organize their project files into a structured folder system. Easily sort footage, still assets, music, and more with a user-friendly interface.

## Features
- Organizes files into categories: Footage, Still Assets, Music, and Other
- Simple and modern graphical interface (Tkinter)
- Remembers last used source and destination folders
- Command-line and GUI usage

## Installation
1. Make sure you have Python 3.7 or newer installed.
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required packages (Tkinter is included with most Python installations):
   ```bash
   pip install --upgrade pip
   ```

## Usage

### Graphical User Interface (Recommended)
Run the script:
```bash
python projectorganizer.py
```
- Use the **Browse** buttons to select your source and destination folders.
- Click **Organize** to sort your files.
- The app will remember your last used folders for next time.

### Command-Line (Legacy)
You can also run the script in a terminal and follow the prompts:
```bash
python projectorganizer.py
```

## Requirements
- Python 3.7+
- Tkinter (usually included with Python)

## Notes
- The app saves your last used folders in a file called `last_folders.json` in the same directory as the script.
- If you want a custom window icon, place an `icon.ico` file in the script directory.

---

Feel free to suggest or contribute new features! 
### README.md

# EclipseChat

EclipseChat is a simple web-based chat application designed to allow two people to communicate in real time.

## Features
- Secure and private one-on-one chat
- User authentication using an Excel sheet
- Simple and lightweight UI

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/eclipsechat.git
   ```
2. Navigate to the project folder:
   ```sh
   cd eclipsechat
   ```
3. Install dependencies:
   ```sh
   pip install flask pandas openpyxl
   ```
4. Run the application:
   ```sh
   python app.py
   ```
5. Open `http://127.0.0.1:5000/` in your browser.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

### .gitignore

```
# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore virtual environments
venv/
.env

# Ignore Excel data files
users.xlsx
chats.xlsx

# Ignore IDE/editor settings
.vscode/
.idea/
.DS_Store
```

---

### LICENSE

```
MIT License

Copyright (c) 2025 Surya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


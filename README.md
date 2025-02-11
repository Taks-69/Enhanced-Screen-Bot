# Enhanced Screen & Camera Capture Bot

This bot is designed to **capture screenshots and camera images** and send them automatically to a **Discord server**. The bot can be controlled remotely via Discord commands, allowing users to start, stop, and configure the capture interval.

---

## 🚀 Features

✅ **Automated Screen & Camera Capture** – Takes periodic screenshots and camera images \
✅ **Dynamic Channel Creation** – Automatically creates dedicated Discord channels \
✅ **Remote Control via Commands** – Start, stop, and set capture frequency via Discord \
✅ **Multi-Screen Support** – Captures multiple monitors \
✅ **Optimized for Nextcord** – Uses the latest Discord API \

---

## 📂 Repository Structure

```
Enhanced-Screen-Bot/
│── bot.py  # Main script for Discord bot
│── requirements.txt  # Dependencies list
```

---

## 📥 Installation

### **Prerequisites**
- **Python 3.x**
- **pip** (Python Package Installer)
- **A Discord Bot Token**
- **Admin privileges on a Discord server**

### **Clone the Repository**
```bash
git clone https://github.com/Taks-69/Enhanced-Screen-Bot.git
cd Enhanced-Screen-Bot
```

### **Install Required Libraries**
```bash
pip install -r requirements.txt
```

### **Required Dependencies** (included in `requirements.txt`)
- `nextcord`
- `opencv-python`
- `mss`
- `asyncio`

---

## 🛠 Usage

### **Setup Configuration**
1. **Edit `bot.py` and replace:**
   - `TOKEN = "Your Token"`
   - `SERVER_ID = 000000000`

2. **Run the bot:**
```bash
python bot.py
```

### **Commands**
| Command | Description |
|---------|-------------|
| `+start_capture` | Starts screen and camera capture |
| `+stop_capture` | Stops the capture process |
| `+set_frequency <seconds>` | Adjusts capture frequency |
| `+help` | Displays available commands |

---

## 🔄 Workflow
1. **Bot connects to Discord** and checks for an existing category based on the PC name.
2. **If missing, it creates dedicated channels** (`control`, `screen-X`, `cam`).
3. **Starts capturing screenshots and camera images** at set intervals.
4. **Uploads images to Discord channels** for remote monitoring.
5. **Users can control bot behavior** with Discord commands.

---

## 📜 Disclaimer

> This project is for **educational purposes only**. The author is **not responsible** for any misuse.

---


## 📚 License

This project is licensed under the GNU General Public License v3.0.

---

🔥 **Feel free to star ⭐ the repository if you find this project useful!** 🚀

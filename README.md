# 🚧 MINECORG  
*A Python CLI tool for organizing Minecraft Bedrock mods (early development)*  

---

**⚠️ Note**: This project is actively under construction! More details, docs, and features are coming soon.  

---

### What's this?  
`MINECORG` is a open source command-line tool to help developers create, organize, and manage Minecraft Bedrock Edition mods. Think of it as your CLI companion for behavior packs, entities, and more!  

---

## Installation (Windows) 

1. **Install Python 3.11+**  
   Download from [python.org](https://www.python.org/downloads/).  
   ✅ Check **"Add Python to PATH"** during installation.  
   🚨 **Close and reopen CMD/PowerShell** after installation.

2. **Install Poetry**  
   Run in CMD/PowerShell:
   ```powershell
   pip install poetry
   ```

3. **Clone Repository**  
   Navigate to your desired folder and run:
   ```bash
   git clone https://github.com/CaetanoP/MINECORG.git
   cd MINECORG
   ```

4. **Install Dependencies**  
   Run in the project folder:
   ```bash
   poetry install
   ```

5. **Add Scripts to PATH**  
   Find the Poetry virtual environment path:
   ```bash
   poetry env info --path
   ```
   Add the `Scripts` subdirectory (e.g., `C:\...\venv\Scripts`) to your **System Environment Variables**.
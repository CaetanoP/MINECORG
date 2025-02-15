# 🚧 MINECORG  
*A Python CLI tool for organizing Minecraft Bedrock mods (early development)*  

---

**⚠️ Note**: This project is actively under construction! More details, docs, and features are coming soon.  

---

### What's this?  
`MINECORG` is a open source command-line tool to help developers create, organize, and manage Minecraft Bedrock Edition mods. Think of it as your CLI companion for behavior packs, entities, and more!  

---

# Installation Guide for MINECORG

## For Contributors (Recommended)

1. **Install Python 3.11+**  
   - Download Python from [python.org](https://www.python.org/downloads/).  
   - **Important:** Ensure you check the box **"Add Python to PATH"** during installation.  
   - **Close and reopen** your CMD or PowerShell window after installation to apply changes.

2. **Install Poetry**  
   - Open CMD or PowerShell and run:
     ```powershell
     pip install poetry
     ```

3. **Clone the Repository**  
   - Navigate to your desired directory and run:
     ```bash
     git clone https://github.com/CaetanoP/MINECORG.git
     ```

4. **Install Dependencies**  
   - Go to the project folder
      ```bash
      cd MINECORG
      ```
   - In the project folder, run:
     ```bash
     poetry install
     ```

5. **Add Scripts to PATH**  
   - Find the path to the Poetry virtual environment by running:
     ```bash
     poetry env info --path
     ```
   - Add the `Scripts` subdirectory (e.g., `C:\...\venv\Scripts`) to your **System Environment Variables**.

---

## For End-Users (Using PyPI)

1. **Install Python 3.11+**  
   - Download Python from [python.org](https://www.python.org/downloads/).  
   - **Important:** Ensure you check the box **"Add Python to PATH"** during installation.  
   - **Close and reopen** your CMD or PowerShell window after installation to apply changes.

2. **Install MINECORG via PyPI**  
   - Open CMD or PowerShell and run:
     ```powershell
     pip install -i https://test.pypi.org/simple/ minecorg
     ```

---

### Notes:
- **For Contributors:** The first method is recommended if you plan to contribute to the project, as it sets up the development environment with all dependencies.
- **For End-Users:** The second method is simpler and intended for users who only want to use the package without modifying the source code.
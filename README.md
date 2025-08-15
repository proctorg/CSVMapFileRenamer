Simple program that will rename files in a folder using the two column CSV file as a mapping.

<img width="743" height="626" alt="Screenshot 2025-08-15 142526" src="https://github.com/user-attachments/assets/af872f32-1e84-4a18-b482-076930e0ff52" />

File Renamer with CSV Mapping
Uses Gooey to provide a GUI for renaming files based on CSV key-value mapping.

Required dependencies:
pip install gooey pandas

CSV format expected:
Column 1: Current filename (key)
Column 2: New filename (target)


Executable built with pyinstaller:
(for venv) ..\FileRenamer\.venv\Scripts\activate
pip install pyinstaller pandas
pyinstaller.exe build.spec

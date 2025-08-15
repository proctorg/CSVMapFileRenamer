Simple program that will rename files in a folder using the two column CSV file as a mapping.

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
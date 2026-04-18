import os
import subprocess
import sys
from pathlib import Path

def main():
    base_dir = Path(__file__).parent / "project_made"
    
    if not base_dir.exists() or not any(base_dir.iterdir()):
        print("No projects found in project_made/ directory.")
        return

    print("=== App-Builder Project Runner ===")
    projects = [d for d in base_dir.iterdir() if d.is_dir()]
    
    for i, p in enumerate(projects):
        print(f"{i + 1}. {p.name}")
        
    try:
        choice = int(input("Select project to run (number): ")) - 1
        if choice < 0 or choice >= len(projects):
            print("Invalid choice.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
        
    target_dir = projects[choice]
    print(f"\nAnalyzing {target_dir.name}...")
    
    command = None
    target_path = str(target_dir.resolve())
    
    if (target_dir / "package.json").exists():
        print("Detected Node.js project.")
        command = "npm install && npm start"
    elif (target_dir / "main.py").exists():
        print("Detected Python project (main.py).")
        command = f"{sys.executable} main.py"
    elif (target_dir / "app.py").exists():
        print("Detected Python project (app.py).")
        command = f"{sys.executable} app.py"
    elif (target_dir / "index.html").exists():
        print("Detected Static Web project (index.html).")
        command = f"{sys.executable} -m http.server 8000"
    else:
        print("Could not auto-detect the project type. Looking for Python scripts...")
        py_files = list(target_dir.glob("*.py"))
        if py_files:
            print(f"Running '{py_files[0].name}' as fallback.")
            command = f"{sys.executable} {py_files[0].name}"
        else:
            print("No recognizable entry point found.")
            return
            
    if command:
        print(f"\n>> Running command: {command}")
        print("-" * 40)
        try:
            subprocess.run(command, shell=True, cwd=target_path)
        except KeyboardInterrupt:
            print("\nProject execution stopped by user.")
        except Exception as e:
            print(f"\nError running project: {e}")

if __name__ == "__main__":
    main()

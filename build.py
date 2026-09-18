import os
import sys
import subprocess
import shutil
import customtkinter

def build_exe():
    print("[Build] Starting Soul Client compilation...")

    # 1. Locate CustomTkinter path for asset bundling
    ctk_path = os.path.dirname(customtkinter.__file__)
    print(f"[Build] Found CustomTkinter at: {ctk_path}")

    # 2. PyInstaller build arguments
    # Change 'main.py' if your primary UI script has a different filename
    entry_point = "main.py" 
    
    if not os.path.exists(entry_point):
        print(f"[Build Error] Could not find entry point script: {entry_point}")
        return

    pyinstaller_args = [
        entry_point,
        "--name=SoulClient",
        "--onefile",
        "--windowed", # Hides the background command prompt window
        f"--add-data={ctk_path};customtkinter/",
        "--clean",
        "--noconfirm"
    ]

    # Optional: Include icon if you have one in an 'assets' folder
    icon_path = os.path.join("assets", "logo.ico")
    if os.path.exists(icon_path):
        pyinstaller_args.append(f"--icon={icon_path}")
        print(f"[Build] Using icon: {icon_path}")

    # 3. Run PyInstaller
    print("[Build] Running PyInstaller...")
    subprocess.run(["pyinstaller"] + pyinstaller_args, check=True)

    print("[Build] PyInstaller compilation finished successfully!")

    # 4. Organize distribution folder for Inno Setup or ZIP distribution
    dist_dir = os.path.join(os.getcwd(), "dist")
    
    print("[Build] Copying runtime dependencies to dist folder...")
    
    # Copy Runtimes folder to dist/Runtimes
    src_runtimes = os.path.join(os.getcwd(), "Runtimes")
    dst_runtimes = os.path.join(dist_dir, "Runtimes")
    if os.path.exists(src_runtimes):
        if os.path.exists(dst_runtimes):
            shutil.rmtree(dst_runtimes)
        shutil.copytree(src_runtimes, dst_runtimes)
        print("[Build] Copied Runtimes successfully.")

    # Copy modpack folder to dist/modpack
    src_modpack = os.path.join(os.getcwd(), "modpack")
    dst_modpack = os.path.join(dist_dir, "modpack")
    if os.path.exists(src_modpack):
        if os.path.exists(dst_modpack):
            shutil.rmtree(dst_modpack)
        shutil.copytree(src_modpack, dst_modpack)
        print("[Build] Copied modpack successfully.")

    # Copy OneConfig folder to dist/OneConfig
    src_oneconfig = os.path.join(os.getcwd(), "OneConfig")
    dst_oneconfig = os.path.join(dist_dir, "OneConfig")
    if os.path.exists(src_oneconfig):
        if os.path.exists(dst_oneconfig):
            shutil.rmtree(dst_oneconfig)
        shutil.copytree(src_oneconfig, dst_oneconfig)
        print("[Build] Copied OneConfig successfully.")
    else:
        print("[Build Warning] OneConfig folder not found in root directory!")

    print("\n==============================================")
    print(" BUILD COMPLETE! Your files are ready in /dist ")
    print("==============================================")

if __name__ == "__main__":
    build_exe()
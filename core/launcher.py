import minecraft_launcher_lib
import subprocess
import os
import sys
import zipfile

class MinecraftLauncher:
    def __init__(self):
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    def get_java_path(self):
        """Resolves path to portable Java 8 in Runtimes directory."""
        if sys.platform.startswith("win"):
            for path_name in ["Runtimes", "runtimes"]:
                java_bin = os.path.join(os.getcwd(), path_name, "zulujava8", "bin", "javaw.exe")
                if os.path.exists(java_bin):
                    return java_bin
                
                runtimes_dir = os.path.join(os.getcwd(), path_name, "zulujava8")
                if os.path.exists(runtimes_dir):
                    for root, dirs, files in os.walk(runtimes_dir):
                        if "javaw.exe" in files:
                            return os.path.join(root, "javaw.exe")
            return os.path.join(os.getcwd(), "Runtimes", "zulujava8", "bin", "javaw.exe")
        else:
            return os.path.join(os.getcwd(), "Runtimes", "zulujava8", "bin", "java")

    def extract_modpack(self, status_callback=None):
        """Extracts pre-configured modpack, mods, and configs to .minecraft."""
        zip_path = os.path.join(os.getcwd(), "modpack", "1.8.9.zip")
        if os.path.exists(zip_path):
            if status_callback:
                status_callback("Syncing mods & configs...")
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.minecraft_directory)
            except Exception as e:
                print(f"[Launcher Error] Failed to extract modpack: {e}")

    def find_forge_version(self):
        """Scans installed versions and verifies the .json file actually exists."""
        if not os.path.exists(self.minecraft_directory):
            return None
            
        installed_versions = minecraft_launcher_lib.utils.get_installed_versions(self.minecraft_directory)
        for ver in installed_versions:
            ver_id = ver["id"]
            if "1.8.9" in ver_id and "forge" in ver_id.lower():
                json_path = os.path.join(self.minecraft_directory, "versions", ver_id, f"{ver_id}.json")
                if os.path.exists(json_path):
                    return ver_id
                else:
                    print(f"[Launcher Notice] Found corrupted Forge directory missing JSON: {ver_id}")
        return None

    def install_forge_safely(self, java_executable, status_callback=None):
        """Installs Forge 1.8.9 dynamically using valid version strings."""
        if status_callback:
            status_callback("Downloading & Installing Forge 1.8.9...")

        if os.path.exists(java_executable):
            java_bin_dir = os.path.dirname(java_executable)
            os.environ["PATH"] = java_bin_dir + os.path.pathsep + os.environ.get("PATH", "")

        # 1. Look up exact Forge version string for 1.8.9
        forge_version = None
        try:
            forge_version = minecraft_launcher_lib.forge.find_forge_version("1.8.9")
            print(f"[Launcher Log] Resolved dynamic Forge version: {forge_version}")
        except Exception as e:
            print(f"[Launcher Warning] Failed to query dynamic Forge version: {e}")

        # Fallback to recommended 1.8.9 Forge version string format
        if not forge_version:
            forge_version = "1.8.9-11.15.1.2318-1.8.9"

        # Clean up stale directory before installing
        corrupt_dir = os.path.join(self.minecraft_directory, "versions", f"1.8.9-forge{forge_version}")
        if os.path.exists(corrupt_dir):
            import shutil
            try:
                shutil.rmtree(corrupt_dir)
                print(f"[Launcher Log] Removed stale directory: {corrupt_dir}")
            except Exception as e:
                print(f"[Launcher Warning] Could not remove stale directory: {e}")

        # 2. Run installation using exact version string
        try:
            print(f"[Launcher Log] Installing Forge: {forge_version}")
            minecraft_launcher_lib.forge.install_forge_version(forge_version, self.minecraft_directory)
        except Exception as e:
            print(f"[Launcher Error] install_forge_version failed: {e}")
            try:
                print("[Launcher Log] Trying run_forge_installer fallback...")
                minecraft_launcher_lib.forge.run_forge_installer(forge_version, self.minecraft_directory)
            except Exception as e2:
                print(f"[Launcher Error] run_forge_installer fallback failed: {e2}")

        # 3. Verify directory installation
        forge_id = self.find_forge_version()
        if not forge_id:
            # Fallback scan: check if any version directory containing 'forge' was created
            versions_dir = os.path.join(self.minecraft_directory, "versions")
            if os.path.exists(versions_dir):
                for folder in os.listdir(versions_dir):
                    if "1.8.9" in folder and "forge" in folder.lower():
                        json_file = os.path.join(versions_dir, folder, f"{folder}.json")
                        if os.path.exists(json_file):
                            return folder

            raise Exception("Forge installation completed, but valid version JSON was not found.")
        return forge_id

    def launch(self, username, ram_gb, app_root=None, status_callback=None):
        base_version = "1.8.9"
        
        def update_step(message):
            print(f"[Launch Step] {message}", flush=True)
            if status_callback:
                status_callback(message)

        update_step("Verifying Environment...")

        java_executable = self.get_java_path()
        print(f"[Launcher Log] Java Path: {java_executable}")

        # 1. Extract modpack
        self.extract_modpack(update_step)

        # 2. Base version setup
        installed_versions = minecraft_launcher_lib.utils.get_installed_versions(self.minecraft_directory)
        installed_version_ids = [v["id"] for v in installed_versions]

        if base_version not in installed_version_ids:
            update_step("Downloading Vanilla 1.8.9...")
            minecraft_launcher_lib.install.install_minecraft_version(base_version, self.minecraft_directory)

        # 3. Forge version setup & verification
        forge_version_id = self.find_forge_version()
        if not forge_version_id:
            forge_version_id = self.install_forge_safely(java_executable, update_step)

        update_step("Building Launch Options...")

        jvm_args = [
            f"-Xmx{ram_gb}G",
            f"-Xms{ram_gb}G",
            "-XX:+UseG1GC",
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:G1NewSizePercent=20",
            "-XX:G1ReservePercent=20",
            "-XX:MaxGCPauseMillis=50",
            "-XX:G1HeapRegionSize=32M",
            "-XX:+DisableExplicitGC",
            "-XX:+AlwaysPreTouch",
            "-XX:+ParallelRefProcEnabled",
            "-XX:+UseStringDeduplication",
            "-Dfml.ignoreInvalidMinecraftCertificates=true",
            "-Dfml.ignorePatchDiscrepancies=true",
            "-Dsun.rmi.dgc.client.gcInterval=3600000",
            "-Dsun.rmi.dgc.server.gcInterval=3600000"
        ]
        options = {
            "username": username,
            "uuid": "1st-line-offline",
            "token": "1st-line-offline",
            "jvmArguments": jvm_args
        }

        if os.path.exists(java_executable):
            options["executablePath"] = java_executable

        update_step("Generating Command...")
        command = minecraft_launcher_lib.command.get_minecraft_command(forge_version_id, self.minecraft_directory, options)
        
        update_step("Spawning Process...")
        print(f"[Launcher Log] Command executed: {' '.join(command)}")
            
        # Spawn Minecraft independently using process creation flags on Windows
        creation_flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform.startswith("win") else 0

        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            bufsize=1,
            creationflags=creation_flags
        )
        
        # Automatically close the CustomTkinter UI window & exit Python script
        if app_root:
            try:
                app_root.destroy()
            except Exception:
                pass
        
        sys.exit(0)
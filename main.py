import traceback
from gui.app import App

if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except Exception as e:
        print("\n--- CRITICAL LAUNCHER ERROR ---")
        traceback.print_exc()
        print("-------------------------------\n")
        input("Press Enter to exit...")
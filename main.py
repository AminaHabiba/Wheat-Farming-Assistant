# main.py

# Main entry point (starts all services).
# Usage: python main.py

import subprocess
import sys
import time
import os
import webbrowser
from pathlib import Path

# ── Constants ────────────────────────────────────────────────
PROJECT_ROOT  = Path(__file__).resolve().parent
BACKEND_CMD   = [sys.executable,
                 "backend/app.py"]
FRONTEND_CMD  = ["streamlit", "run",
                 "frontend/app_streamlit.py",
                 "--server.headless=true"]
OLLAMA_CMD    = ["ollama", "serve"]
APP_URL       = "http://localhost:8501"
BACKEND_URL   = "http://localhost:5000"
OLLAMA_URL    = "http://localhost:11434"


# ── Print Banner ─────────────────────────────────────────────
def print_banner():
    print()
    print("=" * 55)
    print("   AI-Powered Wheat Farming Assistant")
    print("   Amina Habiba  ")
    print("   UAF Faisalabad ")
    print("=" * 55)
    print()


# ── Check Service Running ────────────────────────────────────
def is_service_running(url, timeout=2):
    """
    Checks if a service is already running
    by sending a request to its URL.

    url     : service URL to check
    timeout : seconds to wait
    Output  : True if running, False if not
    """
    try:
        import urllib.request
        urllib.request.urlopen(
            url, timeout=timeout)
        return True
    except Exception:
        return False


# ── Start Ollama ─────────────────────────────────────────────
def start_ollama():
    """
    Starts Ollama server if not already running.
    Returns process object or None.
    """
    print("[1/3] Checking Ollama AI Model...")

    if is_service_running(OLLAMA_URL):
        print("      ✅ Ollama already running!")
        return None

    print("      Starting Ollama...")
    try:
        if sys.platform == "win32":
            process = subprocess.Popen(
                OLLAMA_CMD,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=
                subprocess.CREATE_NEW_CONSOLE
            )
        else:
            process = subprocess.Popen(
                OLLAMA_CMD,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        # wait for Ollama to start
        for i in range(10):
            time.sleep(2)
            if is_service_running(OLLAMA_URL):
                print("      ✅ Ollama started "
                      "on port 11434!")
                return process
            print(f"      Waiting... "
                  f"({(i+1)*2}s)")

        print("      ⚠️  Ollama taking long "
              "to start — continuing anyway")
        return process

    except FileNotFoundError:
        print("      ❌ Ollama not found!")
        print("         Install from: "
              "https://ollama.com/download")
        print("         Chatbot will not work "
              "without Ollama.")
        return None


# ── Start Flask Backend ──────────────────────────────────────
def start_backend():
    """
    Starts Flask backend server.
    Returns process object or None.
    """
    print("\n[2/3] Starting Flask Backend...")

    if is_service_running(BACKEND_URL):
        print("      ✅ Backend already running!")
        return None

    try:
        if sys.platform == "win32":
            process = subprocess.Popen(
                BACKEND_CMD,
                cwd=str(PROJECT_ROOT),
                creationflags=
                subprocess.CREATE_NEW_CONSOLE
            )
        else:
            process = subprocess.Popen(
                BACKEND_CMD,
                cwd=str(PROJECT_ROOT),
            )

        # wait for backend to start
        for i in range(8):
            time.sleep(2)
            if is_service_running(BACKEND_URL):
                print("      ✅ Backend started "
                      "on port 5000!")
                return process
            print(f"      Waiting... "
                  f"({(i+1)*2}s)")

        print("      ⚠️  Backend taking long "
              "to start — continuing anyway")
        return process

    except Exception as e:
        print(f"      ❌ Backend error: {e}")
        return None


# ── Start Streamlit Frontend ─────────────────────────────────
def start_frontend():
    """
    Starts Streamlit frontend.
    Returns process object or None.
    """
    print("\n[3/3] Starting Streamlit Frontend...")

    try:
        if sys.platform == "win32":
            process = subprocess.Popen(
                FRONTEND_CMD,
                cwd=str(PROJECT_ROOT),
                creationflags=
                subprocess.CREATE_NEW_CONSOLE
            )
        else:
            process = subprocess.Popen(
                FRONTEND_CMD,
                cwd=str(PROJECT_ROOT)
            )

        # wait for streamlit to start
        print("      Waiting for Streamlit...")
        time.sleep(6)
        print("      ✅ Streamlit started "
              "on port 8501!")
        return process

    except FileNotFoundError:
        print("      ❌ Streamlit not found!")
        print("         Run: "
              "pip install streamlit")
        return None
    except Exception as e:
        print(f"      ❌ Frontend error: {e}")
        return None


# ── Open Browser ─────────────────────────────────────────────
def open_browser():
    """Opens app in default browser."""
    print("\n   Opening browser...")
    time.sleep(2)
    webbrowser.open(APP_URL)


# ── Print Status ─────────────────────────────────────────────
def print_status():
    """Prints final status of all services."""
    print()
    print("=" * 55)
    print("   SERVICE STATUS")
    print("=" * 55)

    services = [
        ("Ollama AI",
         OLLAMA_URL,
         "port 11434"),
        ("Flask Backend",
         BACKEND_URL,
         "port 5000"),
        ("Streamlit App",
         APP_URL,
         "port 8501")
    ]

    all_ok = True
    for name, url, port in services:
        ok = is_service_running(url)
        if ok:
            print(f"   ✅ {name:<20} "
                  f"running on {port}")
        else:
            print(f"   ❌ {name:<20} "
                  f"NOT running")
            all_ok = False

    print("=" * 55)

    if all_ok:
        print()
        print("   🌾 All services running!")
        print(f"   🌐 Open: {APP_URL}")
    else:
        print()
        print("   ⚠️  Some services failed.")
        print("   Check errors above.")

    print()
    print("   Press CTRL+C to stop all services")
    print("=" * 55)


# ── Stop All Services ────────────────────────────────────────
def stop_all(processes):
    """
    Stops all running processes.
    Called when user presses CTRL+C.
    """
    print("\n")
    print("=" * 55)
    print("   Stopping all services...")
    print("=" * 55)

    for name, process in processes:
        if process:
            try:
                process.terminate()
                print(f"   ✅ {name} stopped")
            except Exception:
                print(f"   ⚠️  {name} "
                      "already stopped")

    print()
    print("   All services stopped!")
    print("   Goodbye! 🌾")
    print("=" * 55)


# ── Main ─────────────────────────────────────────────────────
def main():
    print_banner()

    processes = []

    try:
        # start all services
        ollama_proc  = start_ollama()
        backend_proc = start_backend()
        frontend_proc = start_frontend()

        processes = [
            ("Ollama",    ollama_proc),
            ("Backend",   backend_proc),
            ("Frontend",  frontend_proc)
        ]

        # open browser
        open_browser()

        # print final status
        print_status()

        # keep running until CTRL+C
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_all(processes)
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        stop_all(processes)
        sys.exit(1)


if __name__ == "__main__":
    main()

import os
import signal
import subprocess
import time

def kill_uvicorn():
    try:
        # Find process ID of uvicorn
        # Windows: taskkill
        subprocess.run(["taskkill", "/F", "/IM", "uvicorn.exe", "/T"], shell=True)
        # Also python if running as python -m
        # But risky. Let's rely on port 8000
        cmd = "netstat -ano | findstr :8000"
        output = subprocess.check_output(cmd, shell=True).decode()
        for line in output.splitlines():
            parts = line.split()
            if len(parts) > 4:
                pid = parts[-1]
                if pid != "0":
                    print(f"Killing PID {pid}")
                    subprocess.run(["taskkill", "/F", "/PID", pid], shell=True)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    kill_uvicorn()

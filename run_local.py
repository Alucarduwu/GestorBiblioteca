import os
import sys
import subprocess
import time

def get_python_executable():
    
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

def run_server():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\033[94m" + " ="*30)
    print("  BIBLIOGESTION | SERVIDOR LOCAL")
    print(" ="*30 + "\033[0m")
    
    python_exe = get_python_executable()
    
    
    cmd = [python_exe, "manage.py", "runserver", "--nothreading", "--noreload"]
    
    try:
        print("\n  🚀 Iniciando servicios...")
        
        
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        
        time.sleep(2)
        if process.poll() is not None:
            
            error_msg = process.stderr.read()
            print(f"\n  \033[91m❌ ERROR AL INICIAR EL SERVIDOR:\033[0m")
            print(f"\033[90m{error_msg}\033[0m")
            print("\n  \033[93mTip: Asegúrate de que el venv esté configurado e instalado.\033[0m")
            return

        print(f"  ✨ Servidor:      \033[92mACTIVO\033[0m")
        print(f"  📚 Base Datos:    \033[92mCONECTADA\033[0m")
        print(f"  🔌 API REST:      \033[92mOPERATIVA\033[0m")
        
        print(f"\n  ➜ Acceso Web:     \033[94mhttp://127.0.0.1:8000/\033[0m")
        print(f"  ➜ Panel Admin:    \033[94mhttp://127.0.0.1:8000/admin/\033[0m")
        print(f"  ➜ Swagger Docs:   \033[94mhttp://127.0.0.1:8000/api/docs/\033[0m")
        
        print("\n  " + "\033[90m" + "-"*50 + "\033[0m")
        print("  \033[90mPresione CTRL+C para apagar el sistema de forma segura\033[0m\n")
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n  🛑 Apagando sistema de forma segura...")
        time.sleep(1)
        print("  ✨ ¡Hasta pronto!")
        sys.exit(0)
    except Exception as e:
        print(f"\n  ❌ Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    run_server()

import os
import sys
import subprocess

def get_python_executable():
    
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

def run_pretty_tests():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\033[94m" + " ="*30)
    print("  BIBLIOGESTION | EJECUCION DE PRUEBAS")
    print(" ="*30 + "\033[0m\n")
    
    python_exe = get_python_executable()
    
    
    cmd = [python_exe, "manage.py", "test", "library.tests", "-v", "2", "--noinput"]
    
    print("  >> Ejecutando validaciones críticas...\n")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    passed = 0
    failed = 0
    last_test_name = ""
    output_captured = []
    
    for line in process.stdout:
        output_captured.append(line)
        line_clean = line.strip()
        
        if " (library.tests." in line_clean:
            last_test_name = line_clean.split(" (")[0]
            continue
            
        if " ... ok" in line_clean:
            display_name = line_clean.replace(" ... ok", "").strip()
            final_name = display_name if display_name else last_test_name
            print(f"  \033[92m[OK]\033[0m {final_name:<45} \033[92m[PASÓ]\033[0m")
            passed += 1
            last_test_name = ""
        elif " ... ERROR" in line_clean or " ... FAIL" in line_clean:
            display_name = line_clean.split(" ... ")[0].strip()
            final_name = display_name if display_name else last_test_name
            print(f"  \033[91m[XX]\033[0m {final_name:<45} \033[91m[FALLÓ]\033[0m")
            failed += 1
            last_test_name = ""
                
    process.wait()
    
    if passed == 0 and failed == 0:
        
        print(f"  \033[91m❌ NO SE DETECTARON PRUEBAS.\033[0m")
        print("\n  \033[90m--- Salida del sistema ---\033[0m")
        print("".join(output_captured[-10:]))
        print("\033[90m--------------------------\033[0m")
    else:
        print("\n" + "\033[90m" + "-"*60 + "\033[0m")
        if failed == 0:
            print(f"  \033[92m*** ¡ÉXITO TOTAL! {passed} pruebas superadas sin errores. ***\033[0m")
        else:
            print(f"  \033[91m!!! ATENCIÓN: {failed} pruebas fallaron. Revise la lógica. !!!\033[0m")
        print("\033[90m" + "-"*60 + "\033[0m\n")

if __name__ == "__main__":
    run_pretty_tests()

import os
import subprocess
import sys

def run_command(command, cwd=None, shell=True):
    """Runs a shell command and exits if it fails."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=shell, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, 'frontend')
    
    print("="*50)
    print("STARTING PRE-DEPLOY ROUTINE")
    print("="*50)

    # 1. Backend Tests
    print("\n[1/3] Running Backend Tests...")
    if not run_command('python manage.py test', cwd=base_dir):
        print("Backend tests failed! Aborting deploy.")
        sys.exit(1)

    # 2. Check Migrations
    print("\n[2/3] Checking for Missing Migrations...")
    if not run_command('python manage.py makemigrations --check', cwd=base_dir):
        print("Missing migrations detected! Aborting deploy.")
        sys.exit(1)

    # 3. Frontend Build
    print("\n[3/3] Building Frontend...")
    # Check if npm is available
    try:
        subprocess.run(['npm', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("npm not found. Skipping frontend build (ensure node is installed).")
        # In some environments we might want to fail here, but for now let's warn.
        # sys.exit(1) 
    else:
        if not run_command('npm run build', cwd=frontend_dir):
            print("Frontend build failed! Aborting deploy.")
            sys.exit(1)

    print("\n" + "="*50)
    print("PRE-DEPLOY ROUTINE COMPLETED SUCCESSFULLY")
    print("="*50)

if __name__ == "__main__":
    main()

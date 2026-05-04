import os
import subprocess

os.chdir(os.path.abspath(os.path.dirname(__file__)))
proc = subprocess.run(
    ['python', '-m', 'PyInstaller', '--clean', 'main.spec'],
    capture_output=True,
    text=True
)
with open('build_log.txt', 'w', encoding='utf-8') as f:
    f.write(proc.stdout)
    f.write('\n--- STDERR ---\n')
    f.write(proc.stderr)
print('returncode', proc.returncode)

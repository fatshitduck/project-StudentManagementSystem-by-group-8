import os

files = [
    "database/__init__.py",
    "models/__init__.py",
    "utils/__init__.py",
    "views/__init__.py"
]

for path in files:
    with open(path, "wb") as f:
        f.write(b"")  # ghi file rỗng sạch
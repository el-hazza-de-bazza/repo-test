import os
import sys

src_dir = r"C:\Users\harry\repo-test\src"
target_file = os.path.join(src_dir, "parameters.py")

# 1. Read the file directly off the hard drive
with open(target_file, "r") as f:
    file_content = f.read()

print("--- FILE CONTENT ON DISK ---")
print(file_content.strip())
print("----------------------------")

# 2. Check where Python loaded 'parameters' from
if "parameters" in sys.modules:
    print("Loaded module file path:", sys.modules["parameters"].__file__)
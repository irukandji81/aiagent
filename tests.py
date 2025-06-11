from functions.run_python import run_python_file

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))  # Should return an error
print(run_python_file("calculator", "nonexistent.py"))  # Should return an error
import subprocess 

# Script to get network interfaces names

# Get network interfaces names
result = subprocess.run(["ipconfig", "/all"], stdout=subprocess.PIPE, text=True)

interfaces = []

print(result.stdout)

for line in result.stdout.split("\n"):
    if "Description" in line:
        interfaces.append(line.split(":")[1].strip())

for element in interfaces:
    print(element)
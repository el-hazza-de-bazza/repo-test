# repo-test
# hello
# i
hello!!!!
how are you doing?
im good how are ytu?

# Importing variables from parameters.py
import requests
url = "https://raw.githubusercontent.com/el-hazza-de-bazza/repo-test/refs/heads/main/src/parameters.py"
response = requests.get(url)
scope = {}
exec(response.text, scope)
""" To obtain parameters, use x = scope.get("x") """

x = scope.get("x")
print(x)
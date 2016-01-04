import json

f =open("jikexueyuan.json")
paths = json.load(f)
print(paths)
f.close()
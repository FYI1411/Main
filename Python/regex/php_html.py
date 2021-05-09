import re
from os import getcwd as cwd
print(f"cwd: {cwd()}")
# file = input("file? ")
file = "tim-kiem.html"
case = r'''(href=["|']/*\w+-*\w+.php)'''
case2 = r'''(action=["|']/*\w+-*\w+.php)'''
with open(file, "r", encoding='utf-8') as f:
    text = f.read()


def foo(matchobj, repl="html"):
    return f"{matchobj.group().split('.')[0]}.{repl}"


if not re.findall(case, text):
    print("No case found.")
else:
    results = re.sub(case, foo, text)
    with open(file, "w", encoding='utf-8') as f:
        f.write(results)

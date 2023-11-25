import interpreter2
i = interpreter2.Interpreter()
file = "code.l" # input("file -> ")
with open(file, "r") as f:
    data = f.read()
    i.parse(data)

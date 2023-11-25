from KEYWORDS import *
import pygame

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = []
        self.main = None
    def parse(self, data:str):
        data = data.replace("\n","").replace(" ", "")
        data = data.split(END)
        while '' in  data:
            data.remove('')
        main_function = Function("main",[],[])
        current_func = main_function
        seperate_code = 0
        code = ""
        for x in data:
            if COMMENT != x[0]:
                for i in x:
                    if i == "{":
                        current_func.code.append(code)
                        code = ""
                        switch = 0
                        function_name = ""
                        parameters = ""
                        for x, i in enumerate(current_func.code[len(current_func.code)-1]):
                            if i != "(" and switch == 0:
                                function_name += i
                            elif switch > 0 and x < len(current_func.code[len(current_func.code)-1])-1:
                                parameters += i
                            else:
                                switch += 1
                        function_parameters = parameters.split(",")
                        current_func.code.pop(len(current_func.code)-1)
                        current_func.code.append(Function(function_name,function_parameters,[],current_func))
                        current_func = current_func.code[len(current_func.code)-1]
                        seperate_code += 1
                    elif i == "}":
                        current_func.code.append(code)
                        code = ""
                        current_func = current_func.parent
                        seperate_code -= 1
                    else:
                        code += i
            current_func.code.append(code)
            code = ""
        self.main = main_function
        self.run(self.main)
        # print(self.variables)

    def sweep_function(self, start):
        for i in start.code:
            if i:
                if type(i) != Function:
                    print(start.name,join(start.parameters," | ")+":", i)
                else:
                    print("FUNCTION:", i.name, join(i.parameters," | "))
                    self.sweep_function(i)
    
    def run(self, start):
        do = True
        for i in start.parameters:
            if self.operate(i) != "True":
                do = False
        if start.name == "if":
            if do:
                for i in start.code:
                    if type(i) != Function:
                        self.operate(i)
                    else:
                        self.run(i)
        elif start.name == "while":
            while do:
                do = True
                for i in start.parameters:
                    if self.operate(i) != "True":
                        do = False
                for i in start.code:
                    if type(i) != Function:
                        self.operate(i)
                    else:
                        self.run(i)
        else:
            for i in start.code:
                if type(i) != Function:
                    self.operate(i)
                else:
                    self.run(i)


    def operate(self, ops):
        operations = []
        operators = 0
        code = ""
        for x in rangelen(ops):
            if ops[x] in OPERATORS:
                operations.append(code)
                operations.append(ops[x])
                operators += 1
                code = ""
            else:
                code += ops[x]
        operations.append(code)
        while any_in(operations, MATH_OPERATORS):
            new_operation = []
            for y in rangelen(operations):
                point = operations[y]
                if point in MATH_OPERATORS:
                    A = operations[y-1]
                    B = operations[y+1]
                    if A in self.variables:
                        A = self.variables[A]
                    if B in self.variables:
                        B = self.variables[B]
                    if point == ADD:
                        new_operation.pop(y-1)
                        new_operation.append(str(float(A) + float(B)))
                    if point == SUBTRACT:
                        new_operation.pop(y-1)
                        new_operation.append(str(float(A) - float(B)))
                    if point == MULTIPLY:
                        new_operation.pop(y-1)
                        new_operation.append(str(float(A) * float(B)))
                    if point == DIVIDE:
                        new_operation.pop(y-1)
                        new_operation.append(str(float(A) / float(B)))
                    if point == MOD:
                        new_operation.pop(y-1)
                        new_operation.append(str(float(A) % float(B)))
                    if point == DIV:
                        new_operation.pop(y-1)
                        new_operation.append(str(float(A) // float(B)))
                    if point == EQUALS:
                        new_operation.pop(y-1)
                        new_operation.append(str(A == B))
                    if point == NOT_EQUALS:
                        new_operation.pop(y-1)
                        new_operation.append(str(A != B))
                    if point == NOT:
                        new_operation.pop(y-1)
                        if B == "False":
                            new_operation.append("True")
                        if B == "True":
                            new_operation.append("False")

                    for i in range(y+2, len(operations)):
                        new_operation.append(operations[i])
                    break
                else:
                    new_operation.append(point)
            operations = new_operation
        if PRINT in operations:
            operations.remove(PRINT)
            buffer = ""
            for i in operations:
                if i != BRACKET_OPEN and i != BRACKET_CLOSE:
                    A = i
                    if A in self.variables:
                        A = self.variables[A]
                    buffer += A
            print(buffer)
        if DEFINE in operations:
            A = operations[operations.index(DEFINE)-1]
            B = operations[operations.index(DEFINE)+1]
            if B in self.variables:
                B = self.variables[B]
            self.variables[A] = B
        return operations[0]


def rangelen(x):
    return range(len(x))

def join(x, w) -> str:
    out = ""
    for a, b in enumerate(x):
        out+=str(b)
        if a != len(x)-1:
            out+=w
    return out

def any_in(a, b):
    for i in a:
        if i in b:
            return True
    return False

class Function:
    def __init__(self, name:str, parameters:list, code:list, parent = None) -> None:
        self.name = name
        self.parameters = parameters
        self.code = code
        self.parent = parent
    def do(self, x):
        pass

class Datatype:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

class String(Datatype):
    pass

class Intiger(Datatype):
    pass

class Float(Datatype):
    pass

class Array(Datatype):
    pass


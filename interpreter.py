class Interpreter:
    def __init__(self):
        self.ADD = "+"
        self.SUBTRACT = "-"
        self.MULTIPLY = "*"
        self.DIVIDE = "/"
        self.DIV = "$"
        self.MOD = "%"

        self.AND = "&"
        self.OR = "|"
        self.EQUAL = ":"
        self.NOT = "!"

        self.END = ";"
        self.SUBSECTION_START = "{"
        self.SUBSECTION_END = "}"
        self.FUNCTION_START = "("
        self.FUNCTION_END = ")"
        self.DEFINE_VAR = "="

        self.PRINT = "print"
        self.PRINTLN = "println"

        self.math_symbols = [self.ADD, self.SUBTRACT, self.MULTIPLY, self.DIVIDE, self.DIV, self.MOD, self.AND, self.OR, self.EQUAL, self.NOT, self.DEFINE_VAR]
        self.symbols = [self.ADD, self.SUBTRACT, self.MULTIPLY, self.DIVIDE, self.DIV, self.MOD, self.AND, self.OR, self.NOT, self.END, self.SUBSECTION_START, self.SUBSECTION_END, self.FUNCTION_START, self.FUNCTION_END, self.DEFINE_VAR]
        self.numbers = list("0123456789")
        self.program = []
        self.variables = {}
        self.number_of_operators = 0

    def rangelen(self, x):
        return range(len(x))

    def decode(self, data: str):
        data = data.replace("\n", "")
        split_data = data.split(";") # Split lines
        while '' in split_data: # Remove all empty parts
            split_data.remove('')
        
        for i in self.rangelen(split_data):
            split_data[i] = list(split_data[i])
        
        for i in self.rangelen(split_data):
            start_space = True
            buff = ""
            for j in self.rangelen(split_data[i]):
                if split_data[i][j] in self.symbols:
                    if buff:
                        self.program.append(buff.strip())
                        buff = ""
                    self.program.append(self.symbols[self.symbols.index(split_data[i][j])])
                    split_data[i][j] = " "
                    self.number_of_operators += 1
                else:
                    if split_data[i][j] != " " and start_space == True:
                        buff += split_data[i][j]
                        start_space = False
                    elif split_data[i][j] == " " and start_space == False:
                        self.program.append(buff.strip())
                        buff = ""
                        start_space = True
                    else:
                        buff += split_data[i][j]
                    if j == len(split_data[i])-1:
                        self.program.append(buff.strip())

            self.program.append("END")


    def simplify(self):
        for x in range(self.number_of_operators):
            while "" in self.program:
                self.program.remove("")
            for i in self.rangelen(self.program):
                if self.program[i] in self.math_symbols:
                    operator = self.program[i]
                    if not(i-1 in self.rangelen(self.program)) or not(i+1 in self.rangelen(self.program)):
                        print("MATH ERROR")
                        return False
                    else:
                        
                        A = self.program[i-1]
                        B = self.program[i+1]
                        if operator != self.DEFINE_VAR:
                            if A in self.variables:
                                A = self.variables[A]
                            if B in self.variables:
                                B = self.variables[B]
                            if operator == self.ADD:
                                Q = str(float(A) + float(B))
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                            if operator == self.SUBTRACT:
                                Q = str(float(A) - float(B))
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                            if operator == self.MULTIPLY:
                                Q = str(float(A) * float(B))
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                            if operator == self.DIVIDE:
                                Q = str(float(A) / float(B))
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                            if operator == self.DIV:
                                Q = str(float(A) // float(B))
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                            if operator == self.MOD:
                                Q = str(float(A) % float(B))
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                            if operator == self.EQUAL:
                                Q = float(A) == float(B)
                                if Q:
                                    Q = "true"
                                else:
                                    Q = "false"
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                            if operator == self.NOT:
                                if B == "false":
                                    Q = "true"
                                else:
                                    Q = "false"
                                self.program[i] = Q
                                self.program[i-1] = ""
                                self.program[i+1] = ""
                                break
                        else:
                            if B in self.variables:
                                self.variables[A] = self.variables[B]
                            else:
                                self.variables[A] = B
        return True    

    
    def do(self):
        self.original_program = self.program.copy()
        # pass
        for x in range(self.number_of_operators):
            self.simplify()
        for i in self.rangelen(self.program):
            if self.program[i] == "print":
                buffer = ""
                if self.program[i+1] == "(":
                    j = i+2
                    if j in self.rangelen(self.program):
                        while self.program[j] != ")":
                            if self.program[j] == "END":
                                print("UNCLOSED_BRACKET error")
                                return
                            buffer += self.program[j]
                            if j+1 in self.rangelen(self.program):
                                j += 1
                            else:
                                print("EOL error")
                                return
                        if buffer in self.variables:
                            print(self.variables[buffer])
                        else:
                            print(buffer)
                    else:
                        print("EOL error")
                        return
        lines = join(self.program, " ").split("END")
        for i in lines:
            print(i)



def join(x:list,y:str):
    out = ""
    for i in x:
        out += i + y
    return out





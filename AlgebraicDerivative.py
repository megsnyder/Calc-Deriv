def derivativeHub(equation):
    expression = ""
    for i in equation[equation.find("=")+1:len(equation)]:
        if i != " ":
            expression += i
    for varTerm in expressionSplitter("x", expression):
        print(deriv("x", varTerm))

def expressionSplitter(indepVar, expression):
    if expression.find(indepVar) == -1:
        print("IndepVars not found", expression)
        return([expression])
    else:
        terms = []
        term = ""
        p = 0
        for i in expression:
            term += i
            if i == "(":
                p += 1
            elif i == ")":
                p -= 1
            if (i == "+" or i == "-") and p == 0:
                if len(term) > 1:
                    if term[len(term)-2].isdigit() or term[len(term)-2] == indepVar or term[len(term)-2] == ")":
                        print("oh yeah")
                        terms.append(term[0:len(term)-1])
                        term = i
                        
                if len(term) == 2:
                    if term == "+":
                        if i == "-":
                            term = "-"
                        else:
                            print("Something Went Wrong :(")
                    elif term[len(term)-2] == "-":
                        if i == "-":
                            term = "+"
                        elif i == "+":
                            term = "-"
        if term != "":
            terms.append(term)
        print("IndepVars found", terms)
        return(terms)

def getOperandsAndTerms(equation):
    #initial Seperation
    terms = []
    term = ""
    operands = []
    letterOperands = "sincotaelg" #Letters in complex operands like trig and log functions
    p = 0
    op = 1
    for i in str(equation):
        status = 0
        for letterOp in letterOperands:
            if i == letterOp:
                status = 1
        if i != " " and i != "'"  and i != "[" and i != "]":
            if i == "(" or i == "{":
                p += 1
                if term != "" and term.count("(") == 0:
                    if letterOperands.find(term[len(term)-1]) == -1:
                        terms.append(term)
                        term = ""
                        op = 0
                if op == 0 and p == 1:
                    if len(term) > 0:
                        if letterOperands.find(term[len(term)-1]) == -1:
                            operands.append("*")
                    #print("OP == 0", term, terms, operands)
                    else:
                        operands.append("*")
            elif i == ")" or i == "}":
                p -= 1
            if p == 0 and i != ")" and i != "}":
                if i == "+" or i == "*" or i == "/" or i == "^":
                    operands.append(i)
                    op = 1
                    if term != "":
                        terms.append(term)
                        term = ""
                elif i == "-":
                    if op == 1:
                        op = 2
                        term += i
                    elif op == 2:
                        op = 0
                        term = term[0:len(term)-1]
                    else:
                        #minusOperator
                        operands.append(i)
                        op = 1
                        if term != "":
                            terms.append(term)
                            term = ""
                elif i.isdigit() == True or i == "." or status == 1:
                    if status == 1 and len(term) > 0:
                        if term[0].isdigit():
                            terms.append(term)
                            term = i
                            operands.append("*")
                        else:
                            term += i
                    else:
                        term += i
                        op = 0
                elif i.isdigit() == False:
                    if term != "":
                        terms.append(term)
                        term = ""
                        op = 0
                    terms.append(i)
                if len(terms) > len(operands) + 1:
                    operands.append("*")
                    op = 1
            elif p == 0 and (i == ")" or i == "}"):
                term += i
                terms.append(term)
                term = ""
                op = 0
            else:
                term += i
    if term != "":
        terms.append(term)
    #print("GottenTerms", terms, "GottenOperands", operands, "from", equation)
    return((terms,operands))

def deriv(indepVar, term):
    #print(term)
    if term.find(indepVar) == -1:
        return(0)
    else:
        output = ""
        terms = getOperandsAndTerms(term)[0]
        operands = getOperandsAndTerms(term)[1]
        num = "" #Numerator
        denom = "" #Denominator
        num += terms[0]
        for i in range(len(operands)):
            if i == "/":
                print("meh")
                
        return(output)
    #Quotient
    #Product
    #Power
    #Trig
    #Log
    #Expo
    #Constant
print(derivativeHub("y = (x/x)/(x/x) + 3"))
#print(expressionSplitter("x", "x/x+3"))
def derivativeHub(equation):
    expression = ""
    for i in equation[equation.find("=")+1:len(equation)]:
        if i != " ":
            expression += i
    derivFinal = ""
    for varTerm in expressionSplitter("x", expression):
        derivFinal += str(deriv("x", varTerm)) + "+"
    derivFinal = derivFinal[0:len(derivFinal)-1]
    return derivFinal
    
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
            if term[0] != "+" and term[0] != "-":
                terms.append("+" + term)
            else:
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
    print("DERIV WITH TERM:",term)
    if term.find(indepVar) == -1:
        return("0")
    elif term.count(indepVar) == 1:
        coefficient = ""
        power = 0
        if len(term) >= term.find(indepVar)+2:
            if term[term.find(indepVar)+1] != "^":
                if term[term.find(indepVar)+1].isdigit():
                    term = term[0:term.find(indepVar)+1] + indepVar + "^1*" + term[term.find(indepVar)+1:len(term)]
                    power = 1
                    coefficient = term[0:term.find(indepVar)] + "*" + term[term.find(indepVar)+1+4:len(term)]
                else:
                    print("ey")
                    term = term[0:term.find(indepVar)+1] + indepVar + "^1" + term[term.find(indepVar)+1:len(term)]
                    power = 1
                    coefficient = term[0:term.find(indepVar)] + "*" + term[term.find(indepVar)+1+4:len(term)]
        else:
            term = term + "^1"
            power = 1
            coefficient = term[0:term.find(indepVar)]
        print(coefficient)
        if coefficient != "":
            if coefficient[0] == "+":
                if len(coefficient) == 1:
                    coefficient = 1
                else:
                    coefficient = coefficient[1:len(coefficient)]
            print(coefficient)
            coefficient = funcSolver(getOperandsAndTerms(coefficient)[0],getOperandsAndTerms(coefficient)[1])
        else:
            i = 0
            index = 0
            while i < 4 and index < len(term):
                if term[i] == "x":
                    i += 1
                elif term[i] == "^" and i == 1:
                    i += 1
                elif term[i].isdigit() and i == 2:
                    i += 1
                elif term[i].isdigit() == False and i == 3:
                    i += 1
                
                index += 1
            if index != len(term) and index - 1 != len(term):
                coefficient = term[0:term.find(indepVar)] + term[index - 1: len(term)]
                coefficient = funcSolver(getOperandsAndTerms(coefficient)[0],getOperandsAndTerms(coefficient)[1])
            else:
                coefficient = term[0:term.find(indepVar)]
                coefficient = funcSolver(getOperandsAndTerms(coefficient)[0],getOperandsAndTerms(coefficient)[1])
        if power == 0:
            power = getOperandsAndTerms(term[term.find("^")+1:len(term)])[0]
            power = power[0]
        coefficient = str(coefficient) + "*" + str(power)
        coefficient = funcSolver(getOperandsAndTerms(coefficient)[0],getOperandsAndTerms(coefficient)[1])
        power = str(float(power) - 1)
        if float(power) == 0.0:
            return(str(coefficient))
        else:
            return(str(coefficient) + str(indepVar) + "^" + str(power))

    else:
        output = "0"
        terms = getOperandsAndTerms(term)[0]
        operands = getOperandsAndTerms(term)[1]
        num = "" #Numerator
        denom = "" #Denominator
        num += terms[0]
        if operands[0] == "/":
            print("QUOTIENT")
        elif operands[0] == "*":
            print("PRODUCT")
        elif operands[0] == "^":
            print("POWER")
        return(output)
    #Quotient
    #Product
    #Power
    #Trig
    #Log
    #Expo
    #Constant








def prenEliminator(terms, operands):
    newTerms = []
    operators = []
    for z in terms:
        newTerms.append(z)
    for z in operands:
        operators.append(z)
    pp = 1 #Status of parenthesis being present
    g = 0 #Just a method to stop infinite loops if there is an error in my code
    
    while pp == 1 and g != 20:
        #print("while", newTerms, "g=", g)
        #print("pren:", newTerms)
        #print("pren:", operands)
        g += 1
        pcheck = ""
        letterOperands = "sincotaelg"
        status = 0
        for i in range(0,len(newTerms)):
            status = 0
            for k in letterOperands:
                if newTerms[i].find(k) != -1:
                    status += 1
            if status != 0:
                newTerms[i] = str(funcSolver(getOperandsAndTerms(newTerms[i])[0],getOperandsAndTerms(newTerms[i])[1]))
        if status == 0:
            for i in range(0,len(newTerms)):
                if str(newTerms[i]).isdigit() == False:
                    #print("Non-int detected in prenElim")
                    p = str(newTerms[i]).count("(")
                    term = ""
                    newTerm = ""
                    outside = ""
                    for k in range(len(newTerms[i])):
                        currentTerm = (newTerms[i])[k]
                        term += currentTerm
                        if currentTerm == "(":
                            #print("Hey we found an opening parenthesis!", newTerms, k)
                            outside += term[0:len(term)-1:]
                            #print("This is the outside:", outside)
                            if len(outside) > 0:
                                #print("The outside is longer than 0")
                                if outside[len(outside) - 1] == ")" or outside[len(outside) - 1].isdigit() == True or outside[len(outside) - 1] == "x" or outside[len(outside) - 1] == "y":
                                    #print("We decided to add a multiplier")
                                    outside += "*"
                            term = "("
                        elif currentTerm == ")" and term[0] == "(" and len(term[1:len(term)-1:]) > 0:
                            term = term[1:len(term)-1:]
                            newTerm = str(funcSolver(getOperandsAndTerms(term)[0],getOperandsAndTerms(term)[1]))
                            outside += "{0}"
                            term = ""
                            outside = outside.format(newTerm)
                        elif currentTerm == ")" and term[0] == "(" and len(term[1:len(term)-1:]) == 0:
                            #print("There is an empty term; Substituting 0")
                            term = ""
                            outside += "0"
                    if len(term) > 0 and len(outside) > 0:
                        if outside[len(outside) - 1].isdigit() == True and term[0].isdigit == True:
                            term = "*" + term
                        outside += term
                        #print("cash me", outside, term)
                    else:
                        outside += term

                    newTerms[i] = str(outside)
                    ##print("newTerms[i]", newTerms[i])
        for h in newTerms:
            pcheck += str(h)
        if pcheck.count("(") == 0:
            pp = 0
    
    if len(newTerms) > 1:
        #print("Int Solver", newTerms)
        newTerms = funcSolver(newTerms, operands)
        return(newTerms)
    else:
        output = ""
        for i in newTerms:
            output += i
        output = float(output)
        return(output) 

def funcSolver(terms, operands):
    letterOperands = "sincotaelg"
    #print("funcSolverCalled")
    #print("terms:", terms)
    #print("operands:", operands)
    newTerms = []
    for i in terms:
        status = 0
        for letter in letterOperands:
            if i.find(letter) != -1:
                status = 1
        if status == 1:
            if i.find("(") != -1:
                term = ""
                for k in i:
                    if i != "(" and i != ")":
                        term += k
                inside = i[i.find("(")+1:i.find(")")]
                term = i[0:i.find("(")]
            else:
                #term = i[i.find("(")+1:len(i)]
                inside = ""
                status = 0 
                for i in term:
                    if term.isdigit() == False and status == 0:
                        #THIS NEEDS TO CHANGE FOR NESTED COMPLEX OPERANDS
                        inside += i
                    else:
                        status += 1
                    if status == 1:
                        term = term[0:term.find(i)-1]
            #print(i, "term", term, "inside", inside)
            if term[0:3] == "log":
                #print("INSIDE", inside)
                expression = ""
                logBase = 0
                if inside.find(",") != -1:
                    expression = inside[0:inside.find(",")]
                    logBase = inside[inside.find(",")+1:len(inside)]
                    #print(logBase)
                    if len(expression) > 1:
                        expression = str(prenEliminator(getOperandsAndTerms(expression)[0],getOperandsAndTerms(expression)[1]))
                    newTerms.append(log(float(expression))/log(float(logBase)))
                else:
                    if len(inside) > 1:
                        inside = prenEliminator(getOperandsAndTerms(inside)[0],getOperandsAndTerms(inside)[1])
                    newTerms.append(log(float(inside))/log(10))
                #print("logBase", logBase, "expression", expression)

                #print("Term", term, float(term[3:len(term)]), log(float(term[3:len(term)])))
                #newTerms.append(log(float(term[3:len(term)])))
                
            else:
                #print(term, "NOT LOG")
                if len(inside) > 0:
                    term = term + str(prenEliminator(getOperandsAndTerms(inside)[0],getOperandsAndTerms(inside)[1]))
                #print(term)
                #print(i[0:3], term[0:3])
                if term[0:3] == "sin":
                    newTerms.append(sin(float(term[3:len(term)])))
                elif term[0:3] == "cos":
                    newTerms.append(cos(float(term[3:len(term)])))
                elif term[0:3] == "tan":
                    newTerms.append(tan(float(term[3:len(term)])))
                elif term[0:3] == "sec":
                    newTerms.append(1/cos(float(term[3:len(term)])))
                elif term[0:3] == "csc":
                    newTerms.append(1/sin(float(term[3:len(term)])))
                elif term[0:3] == "cot":
                    newTerms.append(1/tan(float(term[3:len(term)])))
                else:
                    newTerms.append(i)
                    #print("The equation you entered was weird. Maybe you should check it.")
        else:
            newTerms.append(i)
    terms = newTerms
    final = 0
    holder = ""
    found = 0
    if len(operands) > 0:
        for i in range(0,len(operands)):
            i = i - found
            if operands[i] == "^":
                #print("ExpoFound")
                newTerms[i] = float(terms[i])**float(terms[i+1])
                #print("NewTermsAdded", terms[i], terms[i+1], newTerms[i], "n")
                del newTerms[i+1]
                del operands[i]
                found += 1
                #print("done")
        #print("expo:", newTerms, operands)
        found = 0
        for i in range(0,len(operands)):
            #print(found, terms, newTerms, operands)
            i = i - found
            #print(i,len(terms),len(operands))
            #print(terms,operands)
            if operands[i] == "*":
                newTerms[i] = float(terms[i])*float(terms[i+1])
                del newTerms[i+1]
                del operands[i]
                found += 1
            elif operands[i] == "/":
                newTerms[i] = float(terms[i])/float(terms[i+1])
                del newTerms[i+1]
                del operands[i]
                found += 1
        #print("mult:", newTerms)
        for i in range(0,len(operands)):
            if operands[i] == "-":
                newTerms[i+1] = str((-1)*float(terms[i+1]))
        #print("sub:", newTerms)
        for i in newTerms:
            final += float(i)
    else:
        final = ""
        for i in str(terms):
            for k in i:
                if k.isdigit() == True or k == "." or k == "-":
                    final += str(k)
        #print(final)
        final = float(final)
    ##print("solved:", final)
    return(final)
    
print(derivativeHub("y = 2x*2 + x + 3x^2"))
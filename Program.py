def derivative(equation, interval):
    if equation.find("=") != -1:
        equation = equation[equation.find("=")+1:len(equation)]
    final = pluggerSetup("y", "x", equation)
    print(final)
    extrema(final, interval)
    
def extrema(equation, interval):
    incr = []
    decr = []
    zeroes = []
    status = 0
    #print(list(range(interval[0],interval[1]+1)))
    for i in range(interval[0],interval[1]+1):
        expression = getOperandsAndTerms(equation.format(i))
        if prenEliminator(expression[0],expression[1]) == 0:
            zeroes.append(i)
            status = 0
        elif prenEliminator(expression[0],expression[1]) > 0:
            incr.append(i)
        elif prenEliminator(expression[0],expression[1]) < 0:
            decr.append(i)
    print("Increasing:", incr)
    print("Decreasing:", decr)
    print("Zeroes:", zeroes)
    
def getOperandsAndTerms(equation):
    #initial Seperation
    terms = []
    term = ""
    operands = []
    p = 0
    op = 1
    for i in str(equation):
        if i != " " and i != "'"  and i != "[" and i != "]":
            if i == "(" or i == "{":
                p += 1
                if term != "" and term.count("(") == 0:
                    terms.append(term)
                    term = ""
                    op = 0
                if op == 0 and p == 1:
                    #print("OP == 0", term, terms, operands)
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
                elif i.isdigit() == True or i == ".":
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
                        print("There is an empty term; Substituting 0")
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
    ##print("returning")
                #Solving Inner parenthetical Terms Like (4 + (3 + 2))
    #print(newTerms, g, "G", pp, ": PP", pcheck, pcheck.count("("))
    return(newTerms) 

def funcSolver(terms, operands):
    #print("funcSolverCalled")
    #print("terms:", terms)
    #print("operands:", operands)
    newTerms = terms
    final = 0
    holder = ""
    found = 0
    if len(operands) > 0:
        for i in range(0,len(operands)):
            i = i - found
            if operands[i] == "^":
                newTerms[i] = float(terms[i])**float(terms[i+1])
                del newTerms[i+1]
                del operands[i]
                found += 1
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
        for i in terms:
            for k in i:
                if k.isdigit() == True or k == "." or k == "-":
                    final += str(k)
        final = float(final)
    #print("solved:", final)
    return(final)
    
def pluggerSetup(depVar, indepVar, equation):
    output = ""
    #print("PluggerSetup", depVar, indepVar, equation)
    for i in equation:
        #print("plug?", i, i == indepVar)
        if i == indepVar:
            if len(output)>0:
                if output[len(output)-1].isdigit():
                    output += "*"+"{0}"
                else:
                    output += "{0}"
            else:
                output += "{0}"
        elif len(output)>0: 
            if output[len(output)-1] == "}" and (i.isdigit() or i == "(" or i == "{"):
                output += "*"+i
            else:
                output += i
        else:
            output += i
        #print(output)
    return output
    
derivative("y=100-x^2", [-100,100])
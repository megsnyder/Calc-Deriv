from math import sin, cos, tan, log

def funcCompiler(terms, operands):
    output = ""
    for i in range(0, len(terms)):
        output += terms[i]
        if i < len(terms) - 1:
            output += operands[i]
    return(output)

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
    for i in range(0,len(terms)):
        #print(terms[i])
        if terms[i] == "-":
            terms[i] = "-1"
    return((terms,operands))
    
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
                term = i
                inside = ""
                status = 0 
                for k in term:
                    if k.isdigit() and status == 0:
                        #THIS NEEDS TO CHANGE FOR NESTED COMPLEX OPERANDS
                        inside += k
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
                    newTerms.append(round(log(float(inside))/log(10),5))
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
                    newTerms.append(round(sin(float(term[3:len(term)])),5))
                elif term[0:3] == "cos":
                    newTerms.append(round(cos(float(term[3:len(term)])),5))
                elif term[0:3] == "tan":
                    newTerms.append(round(tan(float(term[3:len(term)])),5))
                elif term[0:3] == "sec":
                    newTerms.append(round(1/cos(float(term[3:len(term)])),5))
                elif term[0:3] == "csc":
                    newTerms.append(round(1/sin(float(term[3:len(term)])),5))
                elif term[0:3] == "cot":
                    newTerms.append(round(1/tan(float(term[3:len(term)])),5))
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
        #print("FINAL:",final)
        final = float(final)
    ##print("solved:", final)
    return(final)

def funcPlugger(depVar, indepVar, equation, t):
    if equation.find("=") != -1:
        equation = equation[equation.find("=")+1:len(equation)]
    a = getOperandsAndTerms(equation.format(t))
    b = prenEliminator(a[0],a[1])
    c = 0
    #print("Wubbo", equation.format(t),a,b)
    if isinstance(b, (list,)):
        #print(b)
        for i in b:
            c += float(i)
    else:
        c = b
    if depVar == "x":
        return(c,t)
    else:
        return(t,c)
        
def pluggerSetup(depVar, indepVar, equation):
    output = ""
    #print("PluggerSetup", depVar, indepVar, equation)
    for i in equation:
        #print("plug?", i, i == indepVar)
        if i == indepVar:
            if len(output)>0:
                if output[len(output)-1].isdigit():
                    output += "*"+"{0}"
                elif output[len(output)-1] == "-":
                    output += "1" + "*" + "{0}"
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

def derivHub(depVar, equation):
    if equation.find("=") != -1:
        equation = equation[equation.find("=")+1:len(equation)]
    splittedFunc = derivSplitter(depVar, equation)
    terms = splittedFunc[0]
    operands = splittedFunc[1]
    final = ""
    #print("Terms",terms, equation)
    for i in terms:
        newSplit = getOperandsAndTerms(i)
        newTerms = newSplit[0]
        newOperands = newSplit[1]
        num = [newTerms[0]]
        denom = []
        for k in range(0,len(newOperands)):
            if newOperands[k] == "*":
                
                num.append(newTerms[k+1])
            elif newOperands[k] == "^":
                num[len(num)-1] += newOperands[k] + newTerms[k+1]
            elif newOperands[k] == "/":
                denom.append(newTerms[k+1])
        conDensedNum = funcCompiler(num,[x for x in "*"*(len(num)-1)])
        conDensedDenom = funcCompiler(denom,[x for x in "*"*(len(denom)-1)])
        print("NUM:", num, "DENOM", denom)
        if final != "":
            final += "+"
        if conDensedNum.count(depVar) + conDensedDenom.count(depVar) == 0:
            final += "0"
        elif len(num) == 1 and conDensedNum[0]== "(" and conDensedNum[len(conDensedNum)-1] == ")":
            print("Guts")
            final += derivHub("x",conDensedNum[1:len(conDensedNum)-1])
        elif denom != []:
            final += quotient(conDensedNum,conDensedDenom)
        elif conDensedNum.count(depVar) == 1:
            final+=power(num)
            "PWRRULE"
        else:
            final += product(num)
    print("FINAL", final, "Eqaution", equation)
    return(final)

def derivSplitter(depVar, expression):
    terms = getOperandsAndTerms(expression)[0]
    operands = getOperandsAndTerms(expression)[1]
    shift = 0
    shifted = 0
    for i in range(len(terms)):
        i = i - shift
        if shifted == 0:
            if terms[i].find(depVar) == -1:
                if len(terms)>i+1:
                    if terms[i+1].find(depVar) != -1:
                        if operands[i] == "*" or operands[i] == "/" or operands[i] == "^":
                            terms[i] = terms[i] + operands[i] + terms[i+1]
                            del terms[i+1]
                            del operands[i]
                            shift += 1
                            shifted = 1
                    elif terms[i+1].find(depVar) == -1:
                        terms[i] = getOperandsAndTerms(terms[i] + operands[i] + terms[i+1])
                        terms[i] = prenEliminator(terms[i][0],terms[i][1])
                        del terms[i+1]
                        del operands[i]
                        shift += 1
                        shifted = 1
            else:
                if len(operands) >= i+1:
                    if operands[i] == "*" or operands[i] == "/" or operands[i] == "^":
                        terms[i] = terms[i] + operands[i] + terms[i+1]
                        del terms[i+1]
                        del operands[i]
                        shift += 1
                        shifted = 1
        else:
            if len(operands) >= i+1 and i != len(terms): 
                if operands[i] == "*" or operands[i] == "/" or operands[i] == "^":
                    terms[i] = terms[i] + operands[i] + terms[i+1]
                    del terms[i+1]
                    del operands[i]
                    shift += 1
            else:
                shifted = 0
    for i in range(len(terms)):
        if i != 0 and i+1 <= len(terms) and len(operands)>0:
            if operands[i-1] == "-":
                terms[i] = "-1*"+terms[i]
                if terms[i].find(depVar) == -1:
                    terms[i] = getOperandsAndTerms(terms[i])
                    terms[i] = prenEliminator(terms[i][0],terms[i][1])
                operands[i-1] = "+"
    return(terms, operands)

def product(terms):
    print("PRODUCT", terms)
    final = ""
    for i in range(len(terms)):
        print(i)
        if i != 0:
            final += "+"
        temp = terms[i]
        for k in range(len(terms)):
            if i != k:
                temp += "*" + str(derivHub("x",terms[k]))
        final += temp
    print("PRODOUT",final)
    return(final)

def quotient(num,denom):
    print("NUMDENOM", num, denom)
    final = "(" + denom + "*" + "(" + derivHub("x",denom) +")" + "-"  + num + "*" "(" + derivHub("x",denom) + ")" + ")" + "/" + "("+"("+ denom + ")" + "^2" +")"
    print("final:", final)
    return(final)

def power(term):
    terms = getOperandsAndTerms(term)[0]
    operands = getOperandsAndTerms(term)[1]
    coefficient = "1"
    power = "1"
    base = "x"
    expo = 0
    for i in range(len(operands)):
        if operands[i] == "^":
            if terms[i].find("x") != -1:
                base = terms[i]
                power = terms[i+1]
            elif terms[i+1].find("x") != -1:
                print("EXPONENTIAL")
                expo = 1
        else:
            coefficient += "*" + terms[i]
    if expo == 0:
        if power.find("x") == -1:
            power = getOperandsAndTerms(power + "-1")
            power = str(prenEliminator(power[0],power[1]))
            if coefficient.find("x") == -1:
                coefficient = getOperandsAndTerms(coefficient + "*" + "(" + power + "+1" + ")")
                coefficient = str(prenEliminator(coefficient[0],coefficient[1]))
                final = coefficient + "*" + base + "^" + "(" + power + ")"
            else:
                print("SOMETHING WENT WRONG")
                final = coefficient + "*" + power + "*" + base + "^" + "(" + power + ")"
        else:
            final = coefficient + "*" + power + "*" + base# + "^(" + power + "-1" + ")"
            print("SOMEThING WENT WRONG")
    else:
        final = "EXPO"
    return(final)
print("Done",derivHub("x", "y=(2x+1*2)^2"))
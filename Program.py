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
        #elif prenEliminator(expression[0],expression[1]) > 0:
        #    incr.append(i)
        #elif prenEliminator(expression[0],expression[1]) < 0:
        #    decr.append(i)
    #print("Increasing:", incr)
    #print("Decreasing:", decr)
    print("Zeroes:", zeroes)
    
def funcInterpreter(depVar, indepVar, equation,t):
    if equation.count("(") != equation.count(")") or equation.count("=") != 1:
        print("Invalid input given")
    else:
        newEquation = ""
        for i in equation:
            if i != " ":
                newEquation += i
        #print("Interpreting:", newEquation)
        if newEquation.find("=") != 1:
            print("Implementation of implicits needed")
        else:
             equationR = newEquation[newEquation.find("=")+1: len(newEquation)]
        #     print("equationR", equationR)
             if equationR.count(indepVar) > 0 or indepVar == "nil":
                  pluggableEquation = pluggerSetup(depVar, indepVar, equationR)
        #          print("pluggable:", pluggableEquation)
             else:
                  b = getOperandsAndTerms(equationR)
                  pluggableEquation = prenEliminator(b[0],b[1])
        points = []
        #for i in range(1,10):
        #    points.append((funcPlugger(depVar, indepVar, str(pluggableEquation), i)))
        points = (funcPlugger(depVar, indepVar, str(pluggableEquation), t))
        #points = "nil"
        
        return(points)
      
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
                else:
                    output += "{0}"
            else:
                output += "{0}"
        elif len(output)>0: 
            if output[len(output)-1] == "}" and i.isdigit():
                output += "*"+i
            else:
                output += i
        else:
            output += i
        #print(output)
    return output

def derivative(equation, interval):
    if equation.find("=") != -1:
        equation = equation[equation.find("=")+1:len(equation)]
    points=[]
    dpoints=[]
    d2points=[]
    function=input("Function: ")
    start=float(input("Start: "))
    end=float(input("End: "))
    i=start
    while i<=end:
        points.append(funcInterpreter("y","x",function,i))
        i+=1
    print(points)
    for i in range(0,len(points)):
        dpoints.append(round(((funcInterpreter("y","x",function,points[i][0]+0.00001)[1]-points[i][1])/.00001),4))
    print(dpoints)
    for i in range(0,len(dpoints)):
        if len(dpoints)>i+1:
            d2points.append(round(((dpoints[i+1]-dpoints[i])/(points[i+1][0]-points[i][0])),4))
        
    print(d2points)
    extremas=[]
    if funcInterpreter("y","x",function,start)[1]>funcInterpreter("y","x",function,start+.5)[1]:
        print("Local max at: " + str(points[0]))
        extremas.append(points[0])
    elif funcInterpreter("y","x",function,start)[1]<funcInterpreter("y","x",function,start+.5)[1]:
        print("Local min at: " + str(points[0]))
        extremas.append(points[0])
    if funcInterpreter("y","x",function,end)[1]>funcInterpreter("y","x",function,end-.5)[1]:
        print("Local max at: " + str(points[len(points)-1]))
        extremas.append(points[len(points)-1])
    elif funcInterpreter("y","x",function,end)[1]<funcInterpreter("y","x",function,end-.5)[1]:
        print("Local min at: " + str(points[len(points)-1]))
        extremas.append(points[len(points)-1])
    for i in range(0,len(dpoints)):
        if len(dpoints)>i+1:
            if dpoints[i]>0:
                if dpoints[i+1]<0:
                    print("Local max at: " + str(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2)))
                    extremas.append(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2))
                elif dpoints[i+1]==0:
                    if len(dpoints)>i+2:
                        if dpoints[i+2]<0:
                            print("Local max at: " + str(points[i+1]))
                            extremas.append(points[i+1])
            if dpoints[i]<0:
                if dpoints[i+1]>0:
                    print("Local min at: " + str(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2)))
                    extremas.append(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2))
                elif dpoints[i+1]==0:
                    if len(dpoints)>i+2:
                        if dpoints[i+2]>0:
                            print("Local min at: " + str(points[i+1]))
                            extremas.append(points[i+1])
    if len(extremas)>0:
        y=extremas[0]
        for i in range(0,len(extremas)):
            if y[1]<extremas[i][1]:
                y = extremas[i]
                
            
    extremasort=[]
    for i in range(0,len(extremas)):
        extremasort.append(extremas[i])
        extremasort.sort()
    print(extremasort)
    
    for i in range(0,len(extremasort)):
        if len(extremasort)>i+1:
            if extremasort[i][1]<extremasort[i+1][1]:
                print("Increasing on interval: [" + str(extremasort[i][0]) + "," + str(extremasort[i+1][0]) + "]")
            if extremasort[i][1]>extremasort[i+1][1]:
                print("Decreasing on interval: [" + str(extremasort[i][0]) + "," + str(extremasort[i+1][0]) + "]")
                
    poi=[]
 
    for i in range(0,len(d2points)):
        if len(d2points)>i+1:
            if d2points[i]>0:
                if d2points[i+1]<0:
                    print("Point of inflection at: " + str("y","x",function,(points[i][0]+points[i+1][0])/2))
                    poi.append(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2))
                elif d2points[i+1]==0:
                    if len(d2points)>i+2:
                        if d2points[i+2]<0:
                            print("Point of inflection at: " + str(points[i+1]))
                            poi.append(points[i+1])
            if d2points[i]<0:
                if d2points[i+1]>0:
                    print("Point of inflection at: " + str(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2)))
                    poi.append(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2))
                elif d2points[i+1]==0:
                    if len(d2points)>i+2:
                        if d2points[i+2]>0:
                            print("Point of inflection at: " + str(points[i+1]))
                            poi.append(points[i+1])
    if len(poi)>0:
        y=poi[0]
        for i in range(0,len(poi)):
            if y[1]<poi[i][1]:
                y = poi[i]
                
            
    poisort=[]
    for i in range(0,len(poi)):
        poisort.append(poi[i])
        poisort.sort()
    print(poisort)
    
    for i in range(0,len(poisort)):
        if len(poisort)>i+1:
            if poisort[i][1]<poisort[i+1][1]:
                print("Concave up on interval: [" + str(poisort[i][0]) + "," + str(poisort[i+1][0]) + "]")
            if poisort[i][1]>poisort[i+1][1]:
                print("Concave down on interval: [" + str(poisort[i][0]) + "," + str(poisort[i+1][0]) + "]")
    
            
    '''
    Integrate: -, parenthesis, and operators
    '''
    final = pluggerSetup("y", "x", equation)
    print(final)
    extrema(final, interval)

derivative("y=100-x^2", [-100,100])

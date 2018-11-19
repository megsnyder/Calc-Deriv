from math import log, sin, cos, tan

print("""Welcome To Meg and Noah's Calculus Project:
The Derivative Calculator
This calculator will ask you for an equation in terms of x (make sure it is lower cased) and an interval (it is broken down into starting and ending points).
Please make sure the starting point is less than the ending point
Example: 
Function: y = x^2-2x+sin(5)
Start: -4
End: 4
Once proper inputs are evaluated, this program will return:
Local Extremas
Absolute Extremas
Increase/Decreasing Intervals
Concave Up/Down Intervals
Points of Inflection
The Algebraic Derivative (We have not done exstensive testing, so take Algebraic derivatives with a grain of salt)
P.S. When using logarithms, we will default to base ten, but if you want a different base you can use a comma seperating the term and log
Example 1: log(10) = 1
Example 2: log(400,20) = log(400)/log(20) = 2
Also, pleasre make sure endpoints are in the interval, because our increasing/decreasing and concavity intervals depend upon them.
""")

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

def funcCompiler(terms, operands):#Take a liste of operands and terms and compiles them into a single string
    output = ""
    for i in range(0, len(terms)):
        output += terms[i]
        if i < len(terms) - 1: #If not the last term, add an operand after the term
            output += operands[i]
    return(output)

def prenEliminator(terms, operands): #This function (combined with func solver) will complete order of operations. This functions specializes in terms with parenthesis.
    newTerms = []
    operators = []
    for z in terms:
        newTerms.append(z)
    for z in operands:
        operators.append(z)
    pp = 1 #Status of parenthesis being present
    g = 0 #Just a method to stop infinite loops if there is an error in my code
    
    while pp == 1 and g != 20:
        g += 1
        pcheck = ""#A variable to determine how many parenthesis there are left over
        letterOperands = "sincotaelg"#The letters of the complex operands (sin, cos, tan, cot, sec, csc, and log)
        status = 0 #Status indicator of the presence of the letters of complex operands
        for i in range(0,len(newTerms)):#This loop checks for complex operands
            status = 0
            for k in letterOperands:
                if newTerms[i].find(k) != -1:
                    status += 1
            if status != 0:#If a complex operand is present, funcsolver will operate on the term in order to get a number
                newTerms[i] = str(funcSolver(getOperandsAndTerms(newTerms[i])[0],getOperandsAndTerms(newTerms[i])[1]))
        if status == 0:#If no complex operands were found...
            for i in range(0,len(newTerms)):
                if str(newTerms[i]).isdigit() == False:#If non-numerical characters are in the string...
                    p = str(newTerms[i]).count("(") #Check the number of opening parenthesis encountered so terms with multiple parenthesis aren't split
                    term = ""
                    newTerm = ""
                    outside = ""
                    for k in range(len(newTerms[i])):
                        '''Here I seperate things outside of the parenthesis and inside the parenthesis
                        4(6+x)
                        becomes
                        outside = 4 + place holder for substitution ("{0}")
                        term = 6+x
                        '''
                        currentTerm = (newTerms[i])[k]
                        term += currentTerm
                        if currentTerm == "(":
                            outside += term[0:len(term)-1:]
                            if len(outside) > 0:
                                if outside[len(outside) - 1] == ")" or outside[len(outside) - 1].isdigit() == True or outside[len(outside) - 1] == "x" or outside[len(outside) - 1] == "y":
                                    outside += "*"
                            term = "("
                        elif currentTerm == ")" and term[0] == "(" and len(term[1:len(term)-1:]) > 0:#If the term has an entire set of parenthesis
                            term = term[1:len(term)-1:]
                            newTerm = str(funcSolver(getOperandsAndTerms(term)[0],getOperandsAndTerms(term)[1]))
                            outside += "{0}"#Adding PlaceHolder
                            term = ""
                            outside = outside.format(newTerm)#Adding term back in
                        elif currentTerm == ")" and term[0] == "(" and len(term[1:len(term)-1:]) == 0:
                            #Checking for empty terms and substituting 0 if any are found - empty terms being "()"
                            term = ""
                            outside += "0"
                    if len(term) > 0 and len(outside) > 0:
                        if outside[len(outside) - 1].isdigit() == True and term[0].isdigit == True:
                            term = "*" + term
                        outside += term
                    else:
                        outside += term

                    newTerms[i] = str(outside)
        for h in newTerms:#Checking for remaining parenthesis (we work inside, outwards)
            pcheck += str(h)
        if pcheck.count("(") == 0:
            pp = 0
    
    if len(newTerms) > 1:
        newTerms = funcSolver(newTerms, operands) #If there are multiple float terms, we feed them to funcSovler
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
    p = 0 #Number of parenthesis present
    op = 1 #Status of last term being an operand or not (this is really only to check is a minus is for subtraction or a negative multiplier)
    for i in str(equation):
        status = 0
        for letterOp in letterOperands:#Checking for complex operands (they are considered terms because they only act on one term not two)
            if i == letterOp:
                status = 1
        if i != " " and i != "'"  and i != "[" and i != "]":#If the character is valid then...
            if i == "(" or i == "{":
                p += 1#Checking for terms with parenthesis because they don't get resolved here
                if term != "" and term.count("(") == 0:
                    if letterOperands.find(term[len(term)-1]) == -1:
                        terms.append(term)
                        term = ""
                        op = 0
                if op == 0 and p == 1:
                    if len(term) > 0:
                        if letterOperands.find(term[len(term)-1]) == -1:
                            operands.append("*")
                    else:
                        operands.append("*")
            elif i == ")" or i == "}":#Finding the end of the parenthetical term
                p -= 1
            if p == 0 and i != ")" and i != "}": #No opened parenthesis present
                if i == "+" or i == "*" or i == "/" or i == "^":#If an operand is present then add the preceding term to the term list and operand to the operand list (minuses are annoying)
                    operands.append(i)
                    op = 1
                    if term != "":
                        terms.append(term)
                        term = ""
                elif i == "-":#Determing the role of a minus
                    if op == 1:#"-" functioning at -1*
                        op = 2
                        term += i
                    elif op == 2:#Double negative
                        op = 0
                        term = term[0:len(term)-1]#Erasing both negatives
                    else:
                        operands.append(i)#Normal minus
                        op = 1
                        if term != "":
                            terms.append(term)
                            term = ""
                elif i.isdigit() == True or i == "." or status == 1:#Determing what is a term (decimal points too!)
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
                elif i.isdigit() == False:#This is for variables or pointing out mistakes
                    if term != "":
                        terms.append(term)
                        term = ""
                    op = 0
                    terms.append(i)
                if len(terms) > len(operands) + 1:#If the number of terms is greater than operands by 2, there is probably a missing "*", so we add it here. This is caused by things like: 2x because there is no operand
                    operands.append("*")
                    op = 1
            elif p == 0 and (i == ")" or i == "}"):#If parenthesis have just been closed, let's add it to the terms
                term += i
                terms.append(term)
                term = ""
                op = 0
            else:
                term += i
    if term != "":#If there is a forgotten term at the end, let's add it in!
        terms.append(term)
    for i in range(0,len(terms)):#If there is just a minus, we make is a negative 1. Example: -(x+1) becomes -1 * (x+1)
        if terms[i] == "-":
            terms[i] = "-1"
    return((terms,operands))
    
def funcSolver(terms, operands):#This function takes simple mathematical statements and returns floats
    letterOperands = "sincotaelg"#Letters of complex operands
    newTerms = []
    for i in terms:#This whole for loop is for complex operands
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
                inside = i[i.find("(")+1:i.find(")")]#This is what the operand is acting upon - this is an integer or variable
                #NESTED COMPLEX OPERANDS - This was a note to myself, which I think I fixed, but I am not sure, so I will keep it in for future reference.
                term = i[0:i.find("(")]#This is for determing what kind of operand is being used
            else:
                term = i
                inside = ""
                status = 0 
                for k in term:
                    if (k.isdigit() and status == 0) or status >= 3:
                        #THIS NEEDS TO CHANGE FOR NESTED COMPLEX OPERANDS - same thing here
                        inside += k
                    else:
                        status += 1
                    if status == 1:
                        term = term[0:term.find(i)-1]
            if term[0:3] == "log":
                expression = ""
                logBase = 0
                if inside.find(",") != -1:#Here we do logs with given bases (we default to base 10)
                    expression = inside[0:inside.find(",")]
                    logBase = inside[inside.find(",")+1:len(inside)]
                    if len(expression) > 1:#If term has operands within, let's get rid of them! - By doing them not just erasing them
                        expression = str(prenEliminator(getOperandsAndTerms(expression)[0],getOperandsAndTerms(expression)[1]))
                    newTerms.append(log(float(expression))/log(float(logBase)))#We have to convert from the natural log to the common log
                else:
                    if len(inside) > 1:
                        inside = prenEliminator(getOperandsAndTerms(inside)[0],getOperandsAndTerms(inside)[1])
                    newTerms.append(round(log(float(inside))/log(10),5))#Here we have a given base. The rounding is present because I could not get around exponential notation without rounding :(.
            else:
                if len(inside) > 0:#If log isn't present we haven't solved the innards of the complex operands, so we do it here
                    term = term + str(prenEliminator(getOperandsAndTerms(inside)[0],getOperandsAndTerms(inside)[1]))
                if term[0:3] == "sin":#Now we distinguish the operands and act upon them
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
                    print("The equation you entered was weird. Maybe you should check it.")
        else:
            newTerms.append(i)
    #Here we resolve the normal operands after the complex operands have finished
    terms = newTerms 
    final = 0
    holder = ""
    found = 0
    if len(operands) > 0:#If there is something to solve, let's solve it
        for i in range(0,len(operands)):
            i = i - found #Since we may be deleting terms from a list, and are iterating at a length of that list, we need to correct for that. Found just tells me how many terms I have deleted
            if operands[i] == "^":#Checking operands
                newTerms[i] = float(terms[i])**float(terms[i+1])#Operating
                del newTerms[i+1]#Making sure we don't do the same thing twice
                del operands[i]
                found += 1#Shielding my program from crashing
        found = 0
        for i in range(0,len(operands)):
            i = i - found
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
        for i in range(0,len(operands)):
            if operands[i] == "-":
                newTerms[i+1] = str((-1)*float(terms[i+1]))
        for i in newTerms:
            final += float(i)
    else:#If there's nothing to solve, let's just combine it and make sure nothing is wrnog
        final = ""
        for i in str(terms):
            for k in i:
                if k.isdigit() == True or k == "." or k == "-":
                    final += str(k)
        final = float(final)
    return(final)

def funcPlugger(depVar, indepVar, equation, t):
    t = round(t,7)
    if equation.find("=") != -1:
        equation = equation[equation.find("=")+1:len(equation)]
    a = getOperandsAndTerms(equation.format(t))
    b = prenEliminator(a[0],a[1])
    c = 0
    if isinstance(b, (list,)):
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

def derivHub(depVar, equation):#This is the brains of the derivative
    letterOperands = "sincotaelg"
    if equation.find("=") != -1:#Again, we only care about the right side of the equation
        equation = equation[equation.find("=")+1:len(equation)]
    splittedFunc = derivSplitter(depVar, equation)#This splits the function into different terms based upon addition and subtraction
    terms = splittedFunc[0]
    operands = splittedFunc[1]
    final = ""
    derivType = ""
    for i in terms:
        newSplit = getOperandsAndTerms(i)#Further splitting each term
        newTerms = newSplit[0]
        newOperands = newSplit[1]
        num = [newTerms[0]]
        denom = []
        for k in range(0,len(newOperands)):#If there is any multiplication/division/exponents we combine terms
            if newOperands[k] == "*":
                num.append(newTerms[k+1])
            elif newOperands[k] == "^":
                num[len(num)-1] += newOperands[k] + newTerms[k+1]
            elif newOperands[k] == "/":
                denom.append(newTerms[k+1])
        conDensedNum = funcCompiler(num,[x for x in "*"*(len(num)-1)])#conDensed is just formatting issue - also I am not sure why the d is capitolized
        conDensedDenom = funcCompiler(denom,[x for x in "*"*(len(denom)-1)])
        if final != "":#As we go through terms, we add the derivatives into final. This just makes sure we have addition symbols
            final += "+"
        if conDensedNum.count(depVar) + conDensedDenom.count(depVar) == 0:#If no variable is found, we have constant. Therefore d/dx(term) = 0
            final += "0" #Constant found
        elif len(num) == 1 and conDensedNum[0]== "(" and conDensedNum[len(conDensedNum)-1] == ")":#This is used for guts or anything with parenthesis
            derivType = "GUTS"
            final += derivHub(depVar,conDensedNum[1:len(conDensedNum)-1])#Calling derivative on the same term without parenthesis
        elif denom != []:#If there is a variable in the denominator, we use the quotient rule
            derivType = "QUOTIENT"
            final += quotient(conDensedNum,conDensedDenom)
        else:
            numOperands = getOperandsAndTerms(conDensedNum)[1]#Here we are checking if the product rule is necessary
            numTerms = getOperandsAndTerms(conDensedNum)[0]
            shift = 0
            for i in range(len(numOperands)):#We condense terms with exponents here
                i = i - shift
                if i+1<len(numOperands):
                    if numOperands[i] == "^":
                        del numOperands[i]
                        numTerms[i] = numTerms[i] + "^" + numTerms[i+1]
                        del numTerms[i+1]
            status = 0
            for i in range(len(numOperands)):#If multiplication is present we update status
                if numOperands[i] == "*":
                    if numTerms[i].find(depVar) != -1 or numTerms[i+1].find(depVar) != -1:
                        status += 1
            if status != 0:#If status has been updated we use the product rule
                derivType = "PRODUCT"
                final += product(num)
            else:#Here we check for complex operands and the power rule
                for letter in letterOperands:#Complex Operand Checker
                    if conDensedNum.find(letter) != -1:
                        status = 1
                if status == 1:
                    if conDensedNum.find("(") != -1:
                        term = ""
                        for k in conDensedNum:
                            if conDensedNum != "(" and conDensedNum != ")":
                                term += k
                        inside = conDensedNum[conDensedNum.find("(")+1:len(conDensedNum)-1]
                        term = conDensedNum[0:conDensedNum.find("(")]
                    else:
                        term = conDensedNum
                        inside = ""
                        status = 0 
                        for k in term:
                            if (k.isdigit() and status == 0) or status >= 3:
                                #THIS NEEDS TO CHANGE FOR NESTED COMPLEX OPERANDS - Again, this is probably fixed by the last or statement
                                inside += k
                            else:
                                status += 1
                            if status == 1:
                                term = term[0:term.find(i)-1]
                if status != 0:#If complex operands were present we use the complex operand function
                    final += complexOp(term, inside)
                else:#If nothing else can be used, we use the power rule - this means we are probably close to the end
                    final+=power(conDensedNum)
    #    if derivType != "": #Relic of attempting the chain rule
    #        final += 
    #print("FINAL", final, "Eqaution", equation)
    return(final)

def complexOp(term,inside):#Here we evaluate complex operands
    i = 0
    coefficient = ""
    while term[i].isdigit():
        coefficient += term[i]#Just saving the coefficient for later
        i+=1
    term = term[i:len(term)]
    if term[0] == "*":#Removing relics of coefficients
        term = term[1:len(term)]
    final = ""
    if term[0:3] == "log":
        expression = ""
        logBase = 0
        if inside.find(",") != -1:
            logBase = inside[inside.find(",")+1:len(inside)]
            inside = inside[0:inside.find(",")]
            final += "1/("+inside+"*"+"ln"+str(logBase)+")"#Derivative of logs with given bases
        else:
            final += "1/("+inside+"*"+str(log(10))+")"#Derivative of logs without given bases
    else:
        if term[0:3] == "sin":#Alternative complex operands and their derivatives
            final += "cos("+inside+")"
        elif term[0:3] == "cos":
            final += "-1*sin("+inside+")"
        elif term[0:3] == "tan":
            final += "1/((cos("+inside+"))^2)"
        elif term[0:3] == "sec":
            final += "tan("+inside+")*sec("+inside+")"
        elif term[0:3] == "csc":
            final += "-1*csc("+inside+")*cot("+inside+")"
        elif term[0:3] == "cot":
            final += "-1*(csc("+inside+"))^2"
        else:
            final += inside
            print("Something may have gone wrong! :(")
    if len(inside) > 0:#Chain rule
        final += "*(" + derivHub("x", inside) + ")"
    if coefficient != "":#Coefficient reincorporation
        final += "*"+coefficient
    return(final)

def derivSplitter(depVar, expression):#Splits and expression into terms of x based upon addition and subtraction
    terms = getOperandsAndTerms(expression)[0]
    operands = getOperandsAndTerms(expression)[1]
    shift = 0#Error Protection
    shifted = 0#Stops reusing a term
    for i in range(len(terms)):
        i = i - shift
        if shifted == 0:
            if terms[i].find(depVar) == -1:#If no variable
                if len(terms)>i+1:#Error protection
                    if terms[i+1].find(depVar) != -1:#Variable in next term
                        if operands[i] == "*" or operands[i] == "/" or operands[i] == "^":
                            terms[i] = terms[i] + operands[i] + terms[i+1]#Combine them through string methods
                            del terms[i+1]
                            del operands[i]
                            shift += 1
                            shifted = 1
                    elif terms[i+1].find(depVar) == -1:#No variables at all
                        terms[i] = getOperandsAndTerms(terms[i] + operands[i] + terms[i+1])#Combining terms through mathematical analysis
                        terms[i] = prenEliminator(terms[i][0],terms[i][1])
                        del terms[i+1]
                        del operands[i]
                        shift += 1
                        shifted = 1
            else:
                if len(operands) >= i+1:#Error shield
                    if operands[i] == "*" or operands[i] == "/" or operands[i] == "^":#Given 1+ variable
                        terms[i] = terms[i] + operands[i] + terms[i+1]#String Analysis
                        del terms[i+1]
                        del operands[i]
                        shift += 1
                        shifted = 1
        else:
            if len(operands) >= i+1 and i != len(terms): #More of the same just different situation
                if operands[i] == "*" or operands[i] == "/" or operands[i] == "^":
                    terms[i] = terms[i] + operands[i] + terms[i+1]
                    del terms[i+1]
                    del operands[i]
                    shift += 1
            else:
                shifted = 0
    for i in range(len(terms)):
        if i != 0 and i+1 <= len(terms) and len(operands)>0:#Error shield
            if operands[i-1] == "-":#Making minuses into multiplication
                terms[i] = "-1*"+terms[i]
                if terms[i].find(depVar) == -1:
                    terms[i] = getOperandsAndTerms(terms[i])
                    terms[i] = prenEliminator(terms[i][0],terms[i][1])
                operands[i-1] = "+"
    return(terms, operands)

def product(terms):#Product Rule
    final = ""
    for i in range(len(terms)):
        if i != 0:
            final += "+"#Just making sure there is addition between terms
        temp = derivHub("x",terms[i])
        for k in range(len(terms)):#deriv * other terms
            if i != k:
                temp += "*" + terms[k]
        final += temp
    return(final)

def quotient(num,denom):#Quotient Rule
    final = "(" + denom + "*" + "(" + derivHub("x",num) +")" + "-"  + num + "*" "(" + derivHub("x",denom) + ")" + ")" + "/" + "("+"("+ denom + ")" + "^2" +")"
    return(final)

def power(term):#Power Rule
    terms = getOperandsAndTerms(term)[0]
    operands = getOperandsAndTerms(term)[1]
    coefficient = "1"
    power = "1"
    base = "x"
    expo = 0
    for i in range(len(operands)):#This complicated mess if for determing the power and coefficient of the given term
        if operands[i] == "^":#Just to make sure there isn't a term with exponent that doesn't have a variable: 3^2*x^4
            if terms[i].find("x") != -1 and terms[i+1].find("x")==-1:
                base = terms[i]
                power = terms[i+1]
            elif terms[i+1].find("x") != -1:#Exponential distinction
                base = terms[i]
                power = terms[i+1]
                expo = 1
        else:
            coefficient += "*" + terms[i]
    if expo == 0:#If it's not exponential...
        if power.find("x") == -1:#Error shield that may not be necessary, but why not (just protection against formatting issues)
            power = getOperandsAndTerms(power + "-1")
            power = str(prenEliminator(power[0],power[1]))
            if coefficient.find("x") == -1:
                coefficient = getOperandsAndTerms(coefficient + "*" + "(" + power + "+1" + ")")
                coefficient = str(prenEliminator(coefficient[0],coefficient[1]))
                final = coefficient + "*" + base + "^" + "(" + power + ")"
            else:
                final = coefficient + "*" + power + "*" + base + "^" + "(" + power + ")"
        else:
            final = coefficient + "*" + power + "*" + base + "^(" + power + "-1" + ")"
    else:
        final = base + "^" + power + "*log(" + base + ",e)" #Exponential
    if base != "x" and expo == 0:
        final += "*("+ derivHub("x",base) +")"
    elif expo == 1 and power != "x":
        final += "*("+derivHub("x",power) +")"
    return(final)

def derivative(function, start, end):
    points=[] #list of points on the function
    dpoints=[] #list of the derivatives of the function points, dy/dx
    d2points=[] #list of the second derivatives of the function points, d(dy/dx)/dx
    dpointsfull=[] #list of points with (x, dy/dx)
    
    i=start #start of the interval
    
    while i<= end: #runs through interval from start to end, adds points on the function
        try:
            points.append(funcInterpreter("y","x",function,i))
            i+=0.05
        except:
            i+=0.05
            print("point out of domain")
    
    degreeofprecision = 0.1 #We find the numerical derivative by using very small secant lines (this is the distance in the x direction of the points we create the secant line with)
    for i in range(0,len(points)): #adds points to derivate and second derivative
        try:
            dpoints.append((funcInterpreter("y","x",function,points[i][0]+degreeofprecision)[1]-points[i][1])/(degreeofprecision)) #first derivative using limit definition and substituting .000001 in for h, rounded to 4 decimals
            dpoint=(points[i][0],((funcInterpreter("y","x",function,points[i][0]+degreeofprecision)[1]-points[i][1])/(degreeofprecision))) #(x, first derivative)
            dpointsfull.append(dpoint) #adds the full points of derivative to the list
            d1=(funcInterpreter("y","x",function,points[i][0]+degreeofprecision), points[i]) #again derivative substituting .000001 in for h
            #print(d1)
            d1=(d1[0][0],(d1[0][1]-d1[1][1])/(d1[0][0]-d1[1][0]))
            d2=(funcInterpreter("y","x",function,points[i][0]+2*degreeofprecision),funcInterpreter("y","x",function,points[i][0]+degreeofprecision)) #first derivative using the x value of the previous line (ends up .000002 away from original point)
            d2=(d2[0][0],(d2[0][1]-d2[1][1])/(d2[0][0]-d2[1][0]))
            #print("2",d2,"1",d1, d2-d1,(d2-d1)/degreeofprecision)
            d2points.append(((d2[1]-d1[1])/(d2[0]-d1[0]))) #adds to the list of second derivatives the slope between the two first derivatives found
        except:
            pass
    extremas=[] #list of all the local extrema
    
    #first checking the endpoints of the function for local extrema
    try:
        if funcInterpreter("y","x",function,start)[1]>funcInterpreter("y","x",function,start+degreeofprecision)[1]: #if the starting point is greater than a point very close to it, there is a local max there
            print("Local max at: " + str(points[0]))
            extremas.append(points[0]) #adds to the grand list of locals
        elif funcInterpreter("y","x",function,start)[1]<funcInterpreter("y","x",function,start+degreeofprecision)[1]: #if the starting point is smaller than a point very close to it, local min
            print("Local min at: " + str(points[0]))
            extremas.append(points[0])
    except:
        print("Starting point is not in the domain of the function. This could result in faulty conacivty and increasing/decreasing intervals.")
    #next checking sign changes in the derivative
    for i in range(0,len(dpoints)): #iterate through the list of derivatives
        if len(dpoints)>i+1: #only runs if within the range of the loop
            if dpoints[i]>0: 
                if dpoints[i+1]<0: #if derivative is positive and then negative, there is a local max at approximately the average of the two x values
                    print("Local max at: " + str(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2)))
                    extremas.append(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2)) #adds to the grand list
                elif dpoints[i+1]==0: #detects a sign change if there is a zero in between, and adds the extrema
                    if len(dpoints)>i+2:
                        if dpoints[i+2]<0:
                            print("Local max at: " + str(points[i+1]))
                            extremas.append(points[i+1])
                        elif dpoints[i+2]==0:
                            if len(dpoints)>i+3: #this is just in case rounding caused two zero derivatives in a row
                                if dpoints[i+3]<0:
                                    print("Local max at: " + str(points[i+2]))
                                    extremas.append(points[i+2])
            if dpoints[i]<0: #if derivative is negative and then positve, there is a local min at approximately the average of the two x values
                if dpoints[i+1]>0:
                    print("Local min at: " + str(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2)))
                    extremas.append(funcInterpreter("y","x",function,(points[i][0]+points[i+1][0])/2))
                elif dpoints[i+1]==0: #detects a sign change if there is a zero in between, and adds the extrema
                    if len(dpoints)>i+2:
                        if dpoints[i+2]>0:
                            print("Local min at: " + str(points[i+1]))
                            extremas.append(points[i+1])
                        elif dpoints[i+2]==0:
                            if len(dpoints)>i+3: #this is just in case rounding caused two zero derivatives in a row
                                if dpoints[i+3]>0:
                                    print("Local min at: " + str(points[i+2]))
                                    extremas.append(points[i+2])
    try:
        if funcInterpreter("y","x",function,end+degreeofprecision)[1]>funcInterpreter("y","x",function,end)[1]: #do the same for the end point
            print("Local max at: " + str(points[len(points)-1]))
            extremas.append(points[len(points)-1])
        elif funcInterpreter("y","x",function,end+degreeofprecision)[1]<funcInterpreter("y","x",function,end-degreeofprecision)[1]:
            print("Local min at: " + str(points[len(points)-1]))
            extremas.append(points[len(points)-1])
    except:
        print("Ending point is not in the domain of the function. This could result in faulty conacivty and increasing/decreasing intervals.")
                            
    maxabsolute=[] #list of absolute maxes
    if len(extremas)>0: #if any extremas exist, (which they have to), then we check what the biggest one is
        y=extremas[0] #the first point in the list of extremas, what we use to compare to the rest
        maxabsolute=[y] #add to the list of extremas
        for i in range(1,len(extremas)): #run through the list of local extrema
            if y[1]<extremas[i][1]: #if one of the extremas is bigger than the first, this changes the variable y to the bigger one
                y = extremas[i]
                maxabsolute=[extremas[i]] #changes the absolute max to the bigger extrema
            elif y[1]==extremas[i][1]: #if they equal, they could both be absolute maxes
                maxabsolute.append(extremas[i]) #add the equal point while keeping the old one so it will print multiple, if present
    for i in maxabsolute: #prints out all the absolute maxes
        print("Absolute max at: " + str(i))
        
    minabsolute=[] #list of absolute mins
    if len(extremas)>0: #the same as the maxes, only run if extremas exist
        y=extremas[0] #use the first point in extremas
        minabsolute=[y]
        for i in range(1,len(extremas)):
            if y[1]>extremas[i][1]: #if the extrema is smaller than the previous, change the variable to that extrema and add it to the list of minima
                y = extremas[i]
                minabsolute=[y]
            elif y[1]==extremas[i][1]: #if they are equally small, keep both the lise
                minabsolute.append(y)
    for i in minabsolute: #print out the minima
        print("Absolute min at: " + str(i))            
            
    extremasort=[] #the list of extremas sorted by their x value
    for i in range(0,len(extremas)): #runs through the list of extremas
        extremasort.append(extremas[i]) #adds the extremas
        extremasort.sort() #sorts the extremas by x value
    
    #we compare extrema to figure out whether the function is increasing or decreasing between them
    for i in range(0,len(extremasort)): #runs through the list of extremas sorted by x value
        if len(extremasort)>i+1: #makes sures the loop is in range
            if extremasort[i][1]<extremasort[i+1][1]: #if the y value of the extrema is smaller than the y value of the next extrema, the graph is increasing
                print("Increasing on interval: [" + str(extremasort[i][0]) + ", " + str(extremasort[i+1][0]) + "]") #print the two extremas with closed brackets
            if extremasort[i][1]>extremasort[i+1][1]: #if the y value of the extrema is larger than the y value of the next extrema, the graph is decreasing
                print("Decreasing on interval: [" + str(extremasort[i][0]) + ", " + str(extremasort[i+1][0]) + "]") #print the two extremas with closed brackets
                
    poi=[dpointsfull[0],dpointsfull[len(dpointsfull)-1]] #list of points of inflection with endpoints added. although these endpoints aren't points of inflection (we don't print them), using endpoints allows us to check for concavity, even if no points of inflection are present within the interval
        
    #checks for sign changes in the second derivative
    for i in range(0,len(d2points)): #runs through the list of derivatives
        if len(d2points)>i+1: #checks if loop is in range
            if d2points[i]>0:
                if d2points[i+1]<0: #if second derivative is positive, then negative, there is a point of inflection at about the average of x values of those two points
                    print("Point of inflection at: " + str(funcInterpreter("y","x",function,(dpointsfull[i][0]+dpointsfull[i+1][0])/2)))
                    poi.append(funcInterpreter("y","x",function,(dpointsfull[i][0]+dpointsfull[i+1][0])/2)) #add points of inflection to the grand list
                elif d2points[i+1]==0: #detects a sign change if there is a zero in between, and adds the point of inflection
                    if len(d2points)>i+2:
                        if d2points[i+2]<0:
                            print("Point of inflection at: " + str(dpointsfull[i+1]))
                            poi.append(dpointsfull[i+1])
                        elif d2points[i+2]==0:
                            if len(d2points)>i+3: #this is just in case rounding caused two zero derivatives in a row
                                if d2points[i+3]<0:
                                    print("Point of inflection at: " + str(dpointsfull[i+2]))
                                    poi.append(dpointsfull[i+2])
            if d2points[i]<0: #if second derivative is negative, then positive, there is a point of inflection at about the average of x values of those two points
                if d2points[i+1]>0:
                    print("Point of inflection at: " + str(funcInterpreter("y","x",function,(dpointsfull[i][0]+dpointsfull[i+1][0])/2)))
                    poi.append(funcInterpreter("y","x",function,(dpointsfull[i][0]+dpointsfull[i+1][0])/2)) #add points of inflection to the grand list
                elif d2points[i+1]==0: #detects a sign change if there is a zero in between, and adds the point of inflection
                    if len(d2points)>i+2:
                        if d2points[i+2]>0:
                            print("Point of inflection at: " + str(dpointsfull[i+1]))
                            poi.append(dpointsfull[i+1])
                        elif d2points[i+2]==0:
                            if len(d2points)>i+3: #this is just in case rounding caused two zero derivatives in a row
                                if d2points[i+3]>0:
                                    print("Point of inflection at: " + str(dpointsfull[i+2]))
                                    poi.append(dpointsfull[i+2])
    poisort=[] #list of points of inflection sorted by x values
    for i in range(0,len(poi)): #runs through the points of inflection and adds them in order
        poisort.append(poi[i])
        poisort.sort()
    
    #comparing the points of inflection in the same way we compared extrema allows us to determine concave up/down (why we added endpoints to the list of points of inflection)
    for i in range(0,len(poisort)): #runs through the sorted points of inflection
        try:
            if len(poisort)>i+1: #makes sure loop range isn't exceeded
                d1=(funcInterpreter("y","x",function,poisort[i][0]+degreeofprecision)[1]-funcInterpreter("y","x",function,poisort[i][0])[1])/.000001 #derivative at point of inflection x value
                d2=(funcInterpreter("y","x",function,poisort[i+1][0]+degreeofprecision)[1]-funcInterpreter("y","x",function,poisort[i+1][0])[1])/.000001 #derivative at the next point of inflection x value
                if d1<d2: #if the derivative at the point of inflection or endpoint is smaller than the next point of inflection, the function is concave up between them, open brackets
                    print("Concave up on interval: (" + str(poisort[i][0]) + ", " + str(poisort[i+1][0]) + ")")
                if d1>d2: #if the derivative at the point of inflection or endpoint is bigger than the next point of inflection, the function is concave down between them, open brackets
                    print("Concave down on interval: (" + str(poisort[i][0]) + ", " + str(poisort[i+1][0]) + ")")
        except:
            pass
function=input("Function: ") #input the function
start=float(input("Start: ")) #input the start of the interval 
end=float(input("End: ")) #input the end of the interval
derivative(function, start, end) #calls the derivative function
print("y = ", derivHub("x", function))

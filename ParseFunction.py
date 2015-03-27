from PyCamellia import *
from SolutionFns import *
import sys
import math

####### Debug variable, for debug output
nDebug = True

# states represent accept states
class State:
    __implementation = None
    def __init__(self, imp):
        self.__implementation = imp
    def changeImp(self, imp):
        self.__implementation = imp
    def __getattr__(self, name):
        return getattr(self.__implementation,name)

# beginning state
class begin:
    name = 'begin'
    def num(self,context,d):
        context.currNum += d
        context.currState.changeImp(numPreDec())
    def dec(self,context):
        context.currNum += '0.'
        context.currState.changeImp(numPostDec())
    def minus(self,context):
        context.currNum += '-'
        context.currState.changeImp(numPreDec())
    def add(self,context):
        context.currState.changeImp(reject("Cannot begin input with +."))
    def div(self,context):
        context.currState.changeImp(reject("Cannot begin input with /."))
    def mult(self,context):
        context.currState.changeImp(reject("Cannot begin input with *."))
    def exp(self,context):
        context.currState.changeImp(reject("Cannot begin input with ^."))
    def x(self,context):
        fn = Function_xn(1)
        context.fnStack.append(fn)
        context.currState.changeImp(inX())
    def y(self,context):
        fn = Function_yn(1)
        context.fnStack.append(fn)
        context.currState.changeImp(inY())
    def lp(self,context):
        fn = Function_constant(1)
        context.opStack.append('*')
        context.fnStack.append(fn)
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        context.currState.changeImp(reject("Cannot begin input with )."))

# directly after a left paren
class lParen:
    name = 'lParen'    
    def num(self,context,d):
        context.currNum += d
        context.currState.changeImp(numPreDec())
    def dec(self,context):
        context.currNum += '0.'
        context.currState.changeImp(numPostDec())
    def minus(self,context):
        context.currNum += '-'
        context.currState.changeImp(numPreDec())
    def add(self,context):
        context.currState.changeImp(reject("Invalid use of +."))
    def div(self,context):
        context.currState.changeImp(reject("Invalid use of /."))
    def mult(self,context):
        context.currState.changeImp(reject("Invalid use of *."))
    def exp(self,context):
        context.currState.changeImp(reject("Invalid use of ^."))
    def x(self,context):
        fn = Function_xn(1)
        context.fnStack.append(fn)
        context.currState.changeImp(inX())
    def y(self,context):
        fn = Function_yn(1)
        context.fnStack.append(fn)
        context.currState.changeImp(inY())
    def lp(self,context):
        fn = Function_constant(1)
        context.opStack.append('*')
        context.fnStack.append(fn)
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        if len(context.parenStack) == 0:
            context.currState.changeImp(reject("Invalid input."))
        else:
            if len(context.parenStack) != 0:
                context.parenStack.pop()
            else:
                context.currState.changeImp(reject("Invalid input."))
            context.currState.changeImp(rParen()) 
            

# number pre dec state
class numPreDec:
    name = 'numPreDec'
    def num(self,context,d):
        context.currNum += d
    def dec(self,context):
        context.currNum += '.'
        context.currState.changeImp(numPostDec())
    def minus(self,context):
        context.opStack.append('-')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def add(self,context):
        context.opStack.append('+')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def div(self,context):
        context.opStack.append('/')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def mult(self,context):
        context.opStack.append('*')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def exp(self,context):
        context.opStack.append('^')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def x(self,context):
        if context.currNum == '-':
            context.currNum += '1'
        const = Function_constant(float(context.currNum))
        context.currNum = ""
        x1 = Function_xn(1)
        fn = x1*const
        context.fnStack.append(fn)
        context.currState.changeImp(inX())
    def y(self,context):
        if context.currNum == '-':
            context.currNum += '1'
        const = Function_constant(float(context.currNum))
        context.currNum = ""
        y1 = Function_yn(1)
        fn = y1*const
        context.fnStack.append(fn)
        context.currState.changeImp(inY())
    def lp(self,context):
        const = Function_constant(float(context.currNum))
        context.currNum = ""
        context.fnStack.append(const)
        context.opStack.append('*')
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        if len(context.parenStack) == 0:
            context.currState.changeImp(reject("Invalid input."))
        else:
            context.fnStack.append(Function_constant(float(context.currNum)))
            context.currNum = ''
            operate(context)
            if len(context.parenStack) != 0:
                context.parenStack.pop()
            else:
                context.currState.changeImp(reject("Invalid input."))
            context.currState.changeImp(rParen()) 


# number post dec state
class numPostDec:
    name = 'numPostDec'
    def num(self,context,d):
        context.currNum += d
    def dec(self,context):
        context.currState.changeImp(reject())
    def minus(self,context):
        context.opStack.append('-')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def add(self,context):
        context.opStack.append('+')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def div(self,context):
        context.opStack.append('/')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def mult(self,context):
        context.opStack.append('*')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def exp(self,context):
        context.opStack.append('^')
        context.fnStack.append(Function_constant(float(context.currNum)))
        context.currNum = ''
        context.currState.changeImp(inOp())
    def x(self,context):
        const = Function_constant(float(context.currNum))
        context.currNum = ""
        x1 = Function_xn(1)
        fn = x1*const
        context.fnStack.append(fn)
        context.currState.changeImp(inX())
    def y(self,context):
        const = Function_constant(float(context.currNum))
        context.currNum = ""
        y1 = Function_yn(1)
        fn = y1*const
        context.fnStack.append(fn)
        context.currState.changeImp(inY())
    def lp(self,context):
        const = Function_constant(float(context.currNum))
        context.currNum = ""
        context.fnStack.append(const)
        context.opStack.append('*')
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        if len(context.parenStack) == 0:
            context.currState.changeImp(reject("Invalid input."))
        else:
            context.fnStack.append(Function_constant(float(context.currNum)))
            context.currNum = ''
            operate(context)
            if len(context.parenStack) != 0:
                context.parenStack.pop()
            else:
                context.currState.changeImp(reject("Invalid input."))
            context.currState.changeImp(rParen()) 


# inX
class inX:
    name = 'inX'
    def num(self,context,d):
        context.currState.changeImp(reject("Cannot have a number following an x, use *."))
    def dec(self,context):
        context.currState.changeImp(reject("Cannot have a . following an x, use *."))
    def minus(self,context):
        context.opStack.append('-')
        context.currState.changeImp(inOp())
    def add(self,context):
        context.opStack.append('+')
        context.currState.changeImp(inOp())
    def div(self,context):
        context.opStack.append('/')
        context.currState.changeImp(inOp())
    def mult(self,context):
        context.opStack.append('*')
        context.currState.changeImp(inOp())
    def exp(self,context):
        context.opStack.append('^')
        context.currState.changeImp(inOp())
    def x(self,context):
        context.currState.changeImp(reject("Cannot have an x following an x, use ^."))
    def y(self,context):
        if len(context.fnStack) != 0:
            preFn = context.fnStack.pop()
        else:
            context.currState.changeImp(reject("Invalid input."))
        y1 = Function_yn(1)
        fn = y1*preFn
        context.fnStack.append(fn)
        context.currState.changeImp(inY())
    def lp(self,context):
        context.opStack.append('*')
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        if len(context.parenStack) == 0:
            context.currState.changeImp(reject("Invalid input."))
        else:
            operate(context)
            if len(context.parenStack) != 0:
                context.parenStack.pop()
            else:
                context.currState.changeImp(reject("Invalid input."))
            context.currState.changeImp(rParen()) 

# inY
class inY:
    name = 'inY'
    def num(self,context,d):
        context.currState.changeImp(reject("Cannot have a number following a y, use *."))
    def dec(self,context):
        context.currState.changeImp(reject("Cannot have a decimal following a y, use *."))
    def minus(self,context):
        context.opStack.append('-')
        context.currState.changeImp(inOp())
    def add(self,context):
        context.opStack.append('+')
        context.currState.changeImp(inOp())
    def div(self,context):
        context.opStack.append('/')
        context.currState.changeImp(inOp())
    def mult(self,context):
        context.opStack.append('*')
        context.currState.changeImp(inOp())
    def exp(self,context):
        context.opStack.append('^')
        context.currState.changeImp(inOp())
    def x(self,context):
        context.currState.changeImp(reject("Cannot have an x following a y, place in the other order."))
    def y(self,context):
        context.currState.changeImp(reject("Cannot have a y following a y, use ^."))
    def lp(self,context):
        context.opStack.append('*')
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        if len(context.parenStack) == 0:
            context.currState.changeImp(reject("Invalid input."))
        else:
            operate(context)
            if len(context.parenStack) != 0:
                context.parenStack.pop()
            else:
                context.currState.changeImp(reject("Invalid input."))
            context.currState.changeImp(rParen()) 

# needs Op
class inOp:
    name = 'needOp'
    def num(self,context,d):
        context.currNum += d
        context.currState.changeImp(numPreDec())
    def dec(self,context):
        context.currNum += '0.'
        context.currState.changeImp(numPostDec())
    def minus(self,context):
        context.currNum += '-'
        context.currState.changeImp(numPreDec())
    def add(self,context):
        context.currState.changeImp(reject("Cannot have two operations next to each other."))
    def div(self,context):
        context.currState.changeImp(reject("Cannot have two operations next to each other."))
    def mult(self,context):
        context.currState.changeImp(reject("Cannot have two operations next to each other."))
    def exp(self,context):
        context.currState.changeImp(reject("Cannot have two operations next to each other."))
    def x(self,context):
        fn = Function_xn(1)
        context.fnStack.append(fn)
        context.currState.changeImp(inX())
    def y(self,context):
        fn = Function_yn(1)
        context.fnStack.append(fn)
        context.currState.changeImp(inY())
    def lp(self,context):
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        context.currState.changeImp(reject("Invalid input."))

class rParen:
    name = 'rParen'
    def num(self,context,d):
        context.currState.changeImp(reject("Cannot have a number directly behind a ), use *."))
    def dec(self,context):
        context.currState.changeImp(reject("Cannot have a . directly behind a ), use *."))
    def minus(self,context):
        context.opStack.append('-')
        context.currState.changeImp(inOp())
    def add(self,context):
        context.opStack.append('+')
        context.currState.changeImp(inOp())
    def div(self,context):
        context.opStack.append('/')
        context.currState.changeImp(inOp())
    def mult(self,context):
        context.opStack.append('*')
        context.currState.changeImp(inOp())
    def exp(self,context):
        context.opStack.append('^')
        context.currState.changeImp(inOp())
    def x(self,context):
        if len(context.fnStack) != 0:
            preFn = context.fnStack.pop()
        else:
            context.currState.changeImp(reject("Invalid input."))
        x1 = Function_xn(1)
        fn = x1*preFn
        context.fnStack.append(fn)
        context.currState.changeImp(inX())
    def y(self,context):
        if len(context.fnStack) != 0:
            preFn = context.fnStack.pop()
        else:
            context.currState.changeImp(reject("Invalid input."))
        y1 = Function_yn(1)
        fn = y1*preFn
        context.fnStack.append(fn)
        context.currState.changeImp(inY())
    def lp(self,context):
        context.opStack.append('*')
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        if len(context.parenStack) == 0:
            context.currState.changeImp(reject("Invalid input."))
        else:
            operate(context)
            if len(context.parenStack) != 0:
                context.parenStack.pop()
            else:
                context.currState.changeImp(reject("Invalid input."))
            context.currState.changeImp(rParen()) 

    
# set to reject string
class reject:
    name = 'reject'
    msg = ''
    def __init__(self, msg):
        self.msg = msg
    def num(self,context,d):
        return
    def dec(self,context):
        return
    def minus(self,context):
        return
    def add(self,context):
        return
    def div(self,context):
        return  
    def mult(self,context):
        return
    def exp(self,context):
        return
    def x(self,context):
        return
    def y(self,context):
        return
    def lp(self,context):
        return
    def rp(self,context):
        return

def operate(context):
    if len(context.opStack) != 0:
        oper = context.opStack.pop()
        if not nDebug:
            print oper
    else:
        raise ValueError("Input does not have a valid amount of operations.")
    if len(context.fnStack) > 1:
        fn2 = context.fnStack.pop()
        fn1 = context.fnStack.pop()
        if not nDebug:
            print fn2
            print fn1
    else:
        raise ValueError("Input does not have valid parentheses.")
    fn = None
    if(oper == '+'):
        fn = fn1 + fn2
    if(oper == '-'):
        fn = fn1 - fn2
    if(oper == '*'):
        fn = fn1 * fn2
    if(oper == '/'):
        fn = fn1 / fn2
    if(oper == '^'):
        d = fn2.evaluate(0)
        if d != fn2.evaluate(1):
            context.currState.changeImp(reject())
        else:
            if d < 0:
                d = -d
                fn1 = 1 / fn1
            if math.floor(d) != d:
                context.currState.changeImp(reject()) 
            else:
                fn = recExp(fn1,d)
    
    context.fnStack.append(fn)
             
def recExp(fn, d):
    if d == 0:
        return Function_constant(1.0)
    if d == 1:
        return fn
    else:
        return fn * recExp(fn,d-1)

class Context:
    currState = State(None)
    parenStack = []
    fnStack = []
    opStack = []
    currNum = ""
    def __init__(self):
        self.currState = State(None)
        self.parenStack = []
        self.fnStack = []
        self.operStack = []

def stringToFunction(toFunction):
    currContext = Context()
    currContext.currState.changeImp(begin())
    withParen = addParen(toFunction)
    for c in withParen:
        if c.isdigit():
            currContext.currState.num(currContext,c)
        elif c == ".":
            currContext.currState.dec(currContext)
        elif c == "-":
            currContext.currState.minus(currContext)
        elif c == "+":
            currContext.currState.add(currContext)
        elif c == "/":
            currContext.currState.div(currContext)
        elif c == "*":
            currContext.currState.mult(currContext)
        elif c == "^":
            currContext.currState.exp(currContext)
        elif c == "x" or c == "X":
            currContext.currState.x(currContext)    
        elif c == "y" or c == "Y":
            currContext.currState.y(currContext) 
        elif c == '(':
            currContext.currState.lp(currContext)
        elif c == ')':
            currContext.currState.rp(currContext)
        else:
            raise ValueError("The character "+c+" is not a valid character.");
    

    if len(currContext.fnStack) == 0:
        currContext.fnStack.append(Function_constant(float(currContext.currNum)))    

    fn = currContext.fnStack.pop()
    if currContext.currState.name == 'reject':
        raise ValueError(currContext.currState.msg)
    elif len(currContext.parenStack) != 0:
        raise ValueError("Parentheses do not match.")   
    return fn

def addParen(toFunction):
    toReturn = ""
    l = 0
    for i,c in enumerate(toFunction):

        if i >= l:
            toReturn += c

            if c == '(':
                l = i + 1
                parenStack = []

                while toFunction[l] != ')' or len(parenStack) != 0:
                    curr = toFunction[l]
                    if curr == '(':
                        parenStack.append('(')
                    if curr == ')':
                        if len(parenStack) != 0:
                            parenStack.pop()
                        else:
                            raise ValueError("Parentheses do not match.")
                    l += 1
                    if l == len(toFunction):
                        break

                substring = toFunction[i+1:l]
                if not nDebug:
                    print "substring in paren is: "+substring
                inside = addParen(substring)
                toReturn += inside[1:-1]     #get rid of extra parens

    toReturn = hasOp(toReturn)

    toReturn = expon(toReturn)

    toReturn = negSign(toReturn)

    toReturn = parenMult(toReturn)
            
    toReturn = multDiv(toReturn)

    toReturn = addSub(toReturn)            
    
    if not nDebug:
        print "paren: " +toReturn
    return toReturn

def hasOp(toFunction):
    mainParen = []
    for c in enumerate(toFunction):
        if c == '(':
            mainParen.append('(')

        if c == ')':
            if len(mainParen) != 0:
                mainParen.pop()
            else:
                raise ValueError("Parentheses do not match")
        if len(mainParen) == 0 and (c == '^' or c == '*' or c == '/' or c == '+' or c == '-'):
            return toFunction

    return "1*"+toFunction

def expon(toFunction):
    if not nDebug:
        print toFunction
    toReturn = ""
    l = 0
    mainParen = []
    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            if len(mainParen) != 0:
                mainParen.pop()
            else:
                raise ValueError("Parentheses do not match.")

        if i >= l:
            toReturn += c

            if c == '^' and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while (not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0) and k >= 0:
                    if(toFunction[k] == '-') and len(parenStack) == 0:
                        if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                            k -= 1                            
                        break

                    if toFunction[k] == 'x' or toFunction[k] == 'y':
                        k -= 1
                        break

                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')',k)
                    if curr == '(':
                        if len(parenStack) != 0:
                            parenStack.pop()
                        else:
                            raise ValueError("Parentheses do not match.")
                        
                    k -= 1
                    if k == -1:
                        break
                if toFunction[l] != '(' and l != len(toFunction):
                    while toFunction[l].isdigit() or (l == i+1 and toFunction[l] == '-'):
                        l += 1
                        if l == len(toFunction):
                            break
                else:
                    l += 1
                    while toFunction[l].isdigit() or (l == i+2 and toFunction[l] == '-'):
                        l += 1
                        if l == len(toFunction):
                            break
                    l += 1

                substring = toFunction[k+1:l]
                pSubstring = '('+substring+')'
                toReturn = toReturn[:k+1]+pSubstring   

                recurRet = toReturn + toFunction[l:len(toFunction)] 
                return expon(recurRet)

    return toReturn

def negSign(toFunction):
    toReturn = ""
    l = 0
    mainParen = []
    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            if len(mainParen) != 0:
                mainParen.pop()
            else:
                raise ValueError("Parentheses do not match.")
        if i >= l:
            toReturn += c

            if c == '-'  and len(mainParen) == 0:
                if i != 0:
                    d = toFunction[i-1]
                    if d == '(' or d == '*' or d == '/' or d == '+' or d == '-':
                        l = i + 1
                        parenStack = []
                        while (not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '*' or toFunction[l] == '-' or toFunction[l] == '/' or toFunction[l] == '0') or len(parenStack) != 0) and l != len(toFunction):

                            curr = toFunction[l]
                            if curr == '(':
                                parenStack.append('(')
                            if curr == ')':
                                if len(parenStack) != 0:
                                    parenStack.pop()
                                else:
                                    raise ValueError("Parentheses do not match.")
                            l += 1
                            if l == len(toFunction):
                                break   

                        substring = toFunction[i:l]
                        pSubstring = '(0'+substring+')'                       
                        toReturn = toReturn[:i]+pSubstring

                        recurRet = toReturn + toFunction[l:len(toFunction)]
                        return negSign(recurRet)
                if i == 0:
                    l = i + 1
                    parenStack = []
                    while (not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '*' or toFunction[l] == '-' or toFunction[l] == '/' or toFunction[l] == '0') or len(parenStack) != 0) and l != len(toFunction):

                        curr = toFunction[l]
                        if curr == '(':
                            parenStack.append('(')
                        if curr == ')':
                            if len(parenStack) != 0:
                                parenStack.pop()
                            else:
                                raise ValueError("Parentheses do not match.")
                        l += 1
                        if l == len(toFunction):
                            break   

                    substring = toFunction[1:l]
                    pSubstring = '(0-'+substring+')'                       
                    toReturn = pSubstring

                    recurRet = toReturn + toFunction[l:len(toFunction)]
                    return negSign(recurRet)

    return toReturn

def parenMult(toFunction):
    toReturn = ""
    l = 0
    mainParen = []

    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            if len(mainParen) != 0:
                mainParen.pop()
            else:
                raise ValueError("Parentheses do not match.")

        if i >= l:
            toReturn += c

            if (c.isdigit() or c == '.' or c == 'x' or c == 'y')  and len(mainParen) == 0:
                if i + 1 != len(toFunction) and toFunction[i+1] == '(':
                    k = i - 1
                    l = i + 1
                    parenStack = []
                    while (not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0) and k >= 0:

                        if(toFunction[k] == '-') and len(parenStack) == 0:
                            if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                                k -= 1                               
                                break

                        curr = toFunction[k]
                        if curr == ')':
                            parenStack.append(')')
                        if curr == '(':
                            if len(parenStack) != 0:
                                parenStack.pop()
                            else:
                                raise ValueError("Parentheses do not match.")
                        k -= 1
                        if k == -1:
                            break   

                    parenStack = []

                    while (not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0) and l != len(toFunction):

                        curr = toFunction[l]
                        if curr == '(':
                            parenStack.append('(')
                        if curr == ')':
                            if len(parenStack) != 0:
                                parenStack.pop()
                            else:
                                raise ValueError("Parentheses do not match.")
                        l += 1
                        if l == len(toFunction):
                            break     

                    substring = toFunction[k+1:l]
                    pSubstring = '('+substring+')'
                    toReturn = toReturn[:k+1]+pSubstring

                    recurRet = toReturn + toFunction[l:len(toFunction)] 
                    return multDiv(recurRet)

                if i + 1 != len(toFunction) and toFunction[i+1] == '^' and len(mainParen) == 0:
                    l = i + 2
                    parenStack = []
                    
                    while l != len(toFunction) and not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '*' or toFunction[l] == '/' or toFunction[l] == '-') or len(parenStack) != 0:

                        curr = toFunction[l]
                        if curr == '(':
                            parenStack.append('(')
                        if curr == ')':
                            if len(parenStack) != 0:
                                parenStack.pop()
                            else:
                                raise ValueError("Parentheses do not match.")
                        l += 1
                        if l == len(toFunction):
                            break          

                    substring = toFunction[i:l]
                    pSubstring = '('+substring+')'
                    toReturn = toReturn[:i]+pSubstring

                    recurRet = toReturn + toFunction[l:len(toFunction)] 
                    return multDiv(recurRet)

    return toReturn

def multDiv(toFunction):
    toReturn = ""
    l = 0
    mainParen = []
    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            if len(mainParen) != 0:
                mainParen.pop()
            else:
                raise ValueError("Parentheses do not match.")

        if i >= l:
            toReturn += c

            if (c == '*' or c == '/') and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while (not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0) and k >= 0:

                    if(toFunction[k] == '-') and len(parenStack) == 0:
                        if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                            k -= 1

                        break

                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')')
                    if curr == '(':
                        if len(parenStack) != 0:
                            parenStack.pop()
                        else:
                            raise ValueError("Parentheses do not match.")
                    k -= 1
                    if k == -1:
                        break

                while (not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0) and l != len(toFunction):
                    curr = toFunction[l]
                    if curr == '(':
                        parenStack.append('(')
                    if curr == ')':
                        parenStack.pop()
                    l += 1
                    if l == len(toFunction):
                        break

                substring = toFunction[k+1:l]
                pSubstring = '('+substring+')'
                toReturn = toReturn[:k+1]+pSubstring  

                recurRet = toReturn + toFunction[l:len(toFunction)] 
                return multDiv(recurRet)

    return toReturn

def addSub(toFunction):
    if not nDebug:
        print toFunction
    toReturn = ""
    l = 0
    mainParen = []
    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            if len(mainParen) != 0:
                mainParen.pop()
            else:
                raise ValueError("Parentheses do not match.")

        if i >= l:
            toReturn += c

            if c == '+'  and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while (not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0) and k >= 0:

                    if(toFunction[k] == '-') and len(parenStack) == 0:
                        if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                            k -= 1
                        break

                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')')
                    if curr == '(':
                        if len(parenStack) != 0:
                            parenStack.pop()
                        else:
                            raise ValueError("Parentheses do not match.")
                    k -= 1
                    if k == -1:
                        break
                parenStack = []
                while (not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0) and l != len(toFunction):

                    curr = toFunction[l]
                    if curr == '(':
                        parenStack.append('(')
                    if curr == ')':
                        if len(parenStack) != 0:
                            parenStack.pop()
                        else:
                            raise ValueError("Parentheses do not match.")
                    l += 1
                    if l == len(toFunction):
                        break

                substring = toFunction[k+1:l]
                pSubstring = '('+substring+')'
                toReturn = toReturn[:k+1]+pSubstring

                recurRet = toReturn + toFunction[l:len(toFunction)] 
                return addSub(recurRet)

            if (c == '-' and not(i == 0 or not(toFunction[i-1] == '(' or toFunction[i-1] == '+' or toFunction[i-1] == '-' or toFunction[i-1] == '*' or toFunction[i-1] == '/' or toFunction[i-1] != '^'))) and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while (not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '-' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0) and k >= 0:
                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')')
                    if curr == '(':
                        if len(parenStack) != 0:
                            parenStack.pop()
                        else:
                            raise ValueError("Parentheses do not match.")
                    k -= 1
                    if k == -1:
                        break
                parenStack = []
                while (not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0) and l != len(toFunction):
                    curr = toFunction[l]
                    if curr == '(':
                        parenStack.append('(')
                    if curr == ')':
                        if len(parenStack) != 0:
                            parenStack.pop()
                        else:
                            raise ValueError("Parentheses do not match.")
                    l += 1
                    if l == len(toFunction):
                        break

                substring = toFunction[k+1:l]
                pSubstring = '('+substring+')'
                toReturn = toReturn[:k+1]+pSubstring

                recurRet = toReturn + toFunction[l:len(toFunction)] 
                return addSub(recurRet)

    return toReturn

if( len(sys.argv) > 1 ):
    print(stringToFunction(sys.argv[1]))
    


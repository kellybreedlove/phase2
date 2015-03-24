from PyCamellia import *
from PyCamellia import Function
from SolutionFns import *
import sys
import math

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
        context.currState.changeImp(reject())
    def div(self,context):
        context.currState.changeImp(reject())
    def mult(self,context):
        context.currState.changeImp(reject())
    def exp(self,context):
        context.currState.changeImp(reject())
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
        context.currState.changeImp(reject())

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
        context.currState.changeImp(reject())
    def div(self,context):
        context.currState.changeImp(reject())
    def mult(self,context):
        context.currState.changeImp(reject())
    def exp(self,context):
        context.currState.changeImp(reject())
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
            context.currState.changeImp(reject())
        else:
            context.parenStack.pop()
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
            context.currState.changeImp(reject())
        else:
            context.fnStack.append(Function_constant(float(context.currNum)))
            context.currNum = ''
            operate(context)
            context.parenStack.pop()
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
            context.currState.changeImp(reject())
        else:
            context.fnStack.append(Function_constant(float(context.currNum)))
            context.currNum = ''
            operate(context)
            context.parenStack.pop()
            context.currState.changeImp(rParen()) 


# inX
class inX:
    name = 'inX'
    def num(self,context,d):
        context.currState.changeImp(reject())
    def dec(self,context):
        context.currState.changeImp(reject())
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
        context.currState.changeImp(reject())
    def y(self,context):
        preFn = context.fnStack.pop()
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
            context.currState.changeImp(reject())
        else:
            operate(context)
            context.parenStack.pop()
            context.currState.changeImp(rParen()) 

# inY
class inY:
    name = 'inY'
    def num(self,context,d):
        context.currState.changeImp(reject())
    def dec(self,context):
        context.currState.changeImp(reject())
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
        context.currState.changeImp(reject())
    def y(self,context):
        context.currState.changeImp(reject())
    def lp(self,context):
        context.opStack.append('*')
        context.parenStack.append('(')
        context.currState.changeImp(lParen())       
    def rp(self,context):
        if len(context.parenStack) == 0:
            context.currState.changeImp(reject())
        else:
            operate(context)
            context.parenStack.pop()
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
        context.currState.changeImp(reject())
    def div(self,context):
        context.currState.changeImp(reject())
    def mult(self,context):
        context.currState.changeImp(reject())
    def exp(self,context):
        context.currState.changeImp(reject())
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
        context.currState.changeImp(reject())

class rParen:
    name = 'rParen'
    def num(self,context,d):
        context.currState.changeImp(reject())
    def dec(self,context):
        context.currState.changeImp(reject())
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
        preFn = context.fnStack.pop()
        x1 = Function_xn(1)
        fn = x1*preFn
        context.fnStack.append(fn)
        context.currState.changeImp(inX())
    def y(self,context):
        preFn = context.fnStack.pop()
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
            context.currState.changeImp(reject())
        else:
            operate(context)           
            context.parenStack.pop()
            context.currState.changeImp(rParen()) 

    
# set to reject string
class reject:
    name = 'reject'
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
    oper = context.opStack.pop()
    print oper
    fn2 = context.fnStack.pop()
    print fn2
    fn1 = context.fnStack.pop()
    print fn1
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
            currContext.currState.changeImpt(reject())
        
    fn = currContext.fnStack.pop()
    if len(currContext.parenStack) != 0:
        return "parenStack not empty"
    elif currContext.currState.name == 'reject':
        return "in reject state"
    return fn

def addParen(toFunction):
    toReturn = ""
    l = 0
    for i,c in enumerate(toFunction):

        if i >= l:
            toReturn += c

            if c == '(':
                l = i
                parenStack = []

                while toFunction[l] != ')' and len(parenStack) == 0:
                    curr = toFunction[l]
                    if curr == '(':
                        parenStack.append('(')
                    if curr == ')':
                        parenStack.pop()
                    l += 1
                    if l == len(toFunction):
                        break

                substring = toFunction[i+1:l]
                inside = addParen(substring)
                toReturn += inside[1:-1]     #get rid of extra parens

    toReturn = expon(toReturn)
            
    toReturn = multDiv(toReturn)

    toReturn = addSub(toReturn)            
            
    print toReturn
    return toReturn

def expon(toFunction):
    print toFunction
    toReturn = ""
    l = 0
    mainParen = []
    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            mainParen.pop()

        if i >= l:
            toReturn += c

            if c == '^' and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0:
                    if(toFunction[k] == '-'):
                        if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                            k -= 1
                            
                        break

                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')',k)
                    if curr == '(':
                        parenStack.pop()
                        
                    k -= 1
                    if k == -1:
                        break
                if toFunction[l] != '(':
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



def multDiv(toFunction):
    toReturn = ""
    l = 0
    mainParen = []
    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            mainParen.pop()

        if i >= l:
            toReturn += c

            if (c.isdigit() or c == '.' or c == 'x' or c == 'y')  and len(mainParen) == 0:
                if i + 1 != len(toFunction) and toFunction[i+1] == '(':
                    k = i - 1
                    l = i + 1
                    parenStack = []
                    while not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0:

                        if(toFunction[k] == '-'):
                            if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                                k -= 1
                                
                                break

                        curr = toFunction[k]
                        if curr == ')':
                            parenStack.append(')')
                        if curr == '(':
                            parenStack.pop()
                        k -= 1
                        if k == -1:
                            break   

                    parenStack = []

                    while not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0:

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

                if i + 1 != len(toFunction) and toFunction[i+1] == '^' and len(mainParen) == 0:
                    l = i + 2
                    parenStack = []
                    
                    while l != len(toFunction) and not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '*' or toFunction[l] == '/' or toFunction[l] == '-') or len(parenStack) != 0:

                        curr = toFunction[l]
                        if curr == '(':
                            parenStack.append('(')
                        if curr == ')':
                            parenStack.pop()
                        l += 1
                        if l == len(toFunction):
                            break          

                    substring = toFunction[i:l]
                    pSubstring = '('+substring+')'
                    toReturn = toReturn[:i]+pSubstring

                    recurRet = toReturn + toFunction[l:len(toFunction)] 
                    return multDiv(recurRet)
                    

            if c == '*' or c == '/' and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0:

                    if(toFunction[k] == '-'):
                        if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                            k -= 1

                        break

                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')')
                    if curr == '(':
                        parenStack.pop()
                    k -= 1
                    if k == -1:
                        break

                while not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0:
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
    toReturn = ""
    l = 0
    mainParen = []
    for i,c in enumerate(toFunction):

        if c == '(':
            mainParen.append('(')

        if c == ')':
            mainParen.pop()

        if i >= l:
            toReturn += c

            if c == '+'  and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0:

                    if(toFunction[k] == '-'):
                        if(k == 0 or (toFunction[k-1] == '(' or toFunction[k-1] == '+' or toFunction[k-1] == '-' or toFunction[k-1] == '*' or toFunction[k-1] == '/' or toFunction[k-1] == '^')):
                            k -= 1

                        break

                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')')
                    if curr == '(':
                        parenStack.pop()
                    k -= 1
                    if k == -1:
                        break

                while not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0:

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
                return addSub(recurRet)

            if (c == '-' and not(i == 0 or (toFunction[i-1] != '(' and toFunction[i-1] != '+' and toFunction[i-1] != '-' and toFunction[i-1] != '*' and toFunction[i-1] != '/' and toFunction[i-1] != '^'))) and len(mainParen) == 0:
                k = i - 1
                l = i + 1
                parenStack = []
                while not(toFunction[k] == '(' or toFunction[k] == '+' or toFunction[k] == '-' or toFunction[k] == '*' or toFunction[k] == '/') or len(parenStack) != 0:
                    curr = toFunction[k]
                    if curr == ')':
                        parenStack.append(')')
                    if curr == '(':
                        parenStack.pop()
                    k -= 1
                    if k == -1:
                        break

                while not(toFunction[l] == ')' or toFunction[l] == '+' or toFunction[l] == '-' or toFunction[l] == '*' or toFunction[l] == '/') or len(parenStack) != 0:
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
                return addSub(recurRet)

    return toReturn

if( len(sys.argv) > 1 ):
    print(stringToFunction(sys.argv[1]))
    

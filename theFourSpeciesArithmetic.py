#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Jon Zhang 
@contact: zj.fly100@gmail.com
@site: 
@version: 1.0
@license: 
@file: calculator.py
@time: 2017/3/18 9:04
Calculator
    实现加减乘除及括号优先级解析
    用户输入四则运算公式后，必须自己解析里面的(),+,-,*,/符号和公式，运算后得出结果，结果必须与真实的计算器所得出的结果一致
"""
import re

def dealPlusOrMinusSign(num):
    if num.count('+') > 1:
        num = "%s" % num.replace("+", "")
    if (num.count('-') % 2) == 1:
        num = "-%s" % num.replace("-", "")
    else:
        num = num.replace("-", "")
    return num

def theMultiplyDivideOperation(theEquation):
    theREPattern = re.compile("\d+\.*\d*[\*\/][\+\-]*\d+\.*\d*")
    matchOrNot = theREPattern.search(theEquation)
    if not matchOrNot:
        return theEquation
    matchResult = matchOrNot.group()
    if '*' in matchResult:
        before, after = matchResult.split("*")
        before = dealPlusOrMinusSign(before)
        after = dealPlusOrMinusSign(after)
        newValue = float(before) * float(after)
    if "/" in matchResult:
        before, after = matchResult.split("/")
        before = dealPlusOrMinusSign(before)
        after = dealPlusOrMinusSign(after)
        newValue = float(before) / float(after)
    before, after = theREPattern.split(theEquation, 1)
    newEquation = "%s%s%s" % (before, newValue, after)
    return theMultiplyDivideOperation(newEquation)

def thePlusMinusOperation(theEquation):
    # 匹配：两个数（正或负）相加或相减
    theREPattern = re.compile("[\+\-]?\d+\.*\d*[\+\-]+\d+\.*\d*")
    matchOrNot = theREPattern.search(theEquation)
    if not matchOrNot:
        return theEquation
    matchResult = matchOrNot.group()
    # 首位为数字
    if matchResult[0].isdigit():
        for i in range(len(matchResult)):
            if not matchResult[i].isdigit():
                if matchResult[i] == "+":
                    # 以加号分割方程式为两部分
                    before, after = re.split("\+", matchResult, 1)
                    before = dealPlusOrMinusSign(before)
                    after = dealPlusOrMinusSign(after)
                    newValue = float(before) + float(after)
                    break
                elif matchResult[i] == "-":
                    # 以减号分割方程式为两部分
                    before, after = re.split("\-", matchResult, 1)
                    before = dealPlusOrMinusSign(before)
                    after = dealPlusOrMinusSign(after)
                    newValue = float(before) - float(after)
                    break
    # 首位为加号或减号
    else:
        for i in range(1, len(matchResult)):
            # 算出除首位的第二个符号的位置
            if not matchResult[i].isdigit():
                if matchResult[i] == "+":
                    # 第二个符号的为加号的计算方式
                    signIndex = matchResult[1:].index("+")
                    before = matchResult[:(signIndex + 1)]
                    before = dealPlusOrMinusSign(before)
                    after = matchResult[(signIndex + 2):]
                    after = dealPlusOrMinusSign(after)
                    newValue = float(before) + float(after)
                    break
                elif matchResult[i] == "-":
                    # 第二个符号的为减号的计算方式
                    signIndex = matchResult[1:].index("-")
                    before = matchResult[:(signIndex + 1)]
                    before = dealPlusOrMinusSign(before)
                    after = matchResult[(signIndex + 2):]
                    after = dealPlusOrMinusSign(after)
                    newValue = float(before) - float(after)
                    break
    before, after = theREPattern.split(theEquation, 1)
    newEquation = "%s%s%s" % (before, newValue, after)
    return thePlusMinusOperation(newEquation)

def begingCalcOperation(theEquation):
    newEquation = theEquation.strip("()")    # 移除方程式两边的括号
    # 方程式已经是一个计算结果 （除了小数点和正负号以外都是数字）,直接返回结果
    if (not newEquation.startswith('-') and newEquation.replace('.','').isdigit()) or (newEquation.startswith('-') and newEquation[1:].replace('.','').isdigit()):
        return newEquation
    # 如果 乘号和除号 在方程式里面
    if "*" in newEquation or "/" in newEquation:
        # 调用乘除函数进行乘除运算，完成得到一个结果
        newEquation = theMultiplyDivideOperation(newEquation)
    # 如果 加号和减号 在方程式里面
    if ("+" in newEquation or "-" in newEquation):
        #print('****************>',newEquation)
        newEquation = thePlusMinusOperation(newEquation)
        #print("==================>", newEquation)
        newEquation = dealPlusOrMinusSign(newEquation)
    return newEquation

def matchEquationInTheParentheses(theEquation):
    theREPattern = re.compile("\([^()]+\)")
    matchOrNot = theREPattern.search(theEquation)                               # 先找出括号里面的，但是在括号里面不能再包含括号
    if matchOrNot:
        matchResult = matchOrNot.group()
        calcResult = begingCalcOperation(matchResult)                           # 计算匹配出的方程式结果
        before,after = theREPattern.split(theEquation,1)                        # 以找出的方程式和前后括号作为分割点进行切割，把原来的分成两部分（匹配出的被删除）
        newEquation = "%s%s%s"%(before,calcResult,after)                       # 重新拼接方程式，上面得出的两部分和匹配出方程的计算结果
        return matchEquationInTheParentheses(newEquation)                       # 继续匹配运算，直到没有括号为止
    else:
        return begingCalcOperation(theEquation)

def checkOutMultiplyAndDivide(theEquation,n):
    if theEquation[-1].isdigit():
        i = theEquation.find(n)
        if i != -1:
            if ((theEquation[i-1].isdigit()) and (i != (len(theEquation)-1))):
                theEquation = theEquation[i+1:]
                return checkOutMultiplyAndDivide(theEquation,n)
            else:return 0
        else:return 1

def beginTheCalc():
    while True:
            theEquationNeedCalculating = input("输入计算方程式:").strip()
            if len(theEquationNeedCalculating) == 0:
                continue
            if theEquationNeedCalculating == "q":
                break
            else:
                theEquationRemoveBlankSpace = re.sub('\s*','',theEquationNeedCalculating) # replace the spacing : remove the blank space
                if (not checkOutMultiplyAndDivide(theEquationRemoveBlankSpace, "*")) or (not checkOutMultiplyAndDivide(theEquationRemoveBlankSpace, "/")):
                    print("SyntaxError: invalid syntax")
                    continue
                theFinallyResult = matchEquationInTheParentheses(theEquationRemoveBlankSpace)
                return (theFinallyResult)

if __name__ == "__main__":
    theFinallyResult = beginTheCalc()
    print(theFinallyResult)
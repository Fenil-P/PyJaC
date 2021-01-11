""" 
PyJaC Competition Submission

Prompts: Create a mathematical-operations-guesser
possibly, combine with web scraping later

Valid operations include; +, -, /, *, ()

We'll just consider the (4): +, -, /, * (for now)

Challenges:
 - Implementing a class so that it follows BEDMAS, (executes the
 combination of mathematical operations in the correct order)
 - Really inefficient and slow as running time is ~ O(n^n)
 (Efficiency can be increased by DP, I believe)
 - Generating combinations of operations with brackets involved,
 since brackets require another operation 
 
 Ideas:
 - A PriorityQueue seems ideal since we go LEFT-RIGHT if the
 operations are of the same order. We should only need {3} classifying
 priorities for e.g. {1, 2, 3}
 (1 for add, subtract/ 2 for multiply, div/3 for brackets)
 and we ensure that the Queue simplifies all the operations with
 the highest priority first. 

 Brackets can be "", "OPEN", "CLOSED" since have to evaluate every
 open, closed pair and there will be brackets between brackets and 
 they don't have to  be between 2 adjacent elements can anywhere from
 a[0] to a[n-1]
 
 Approaches:
 
 _A1, 
 A class that can execute the following properly: 
 a: '4 / 4 + 8 - 9 * 6 + (9 + 1)' = -35
 b: '((4/4) + 8 - 9) * 6 + (9 + 1)' = 10
 
 and then basically get all list combinations of operations, 
 
 make a function to convert the input <List[int]> + all combs
 <List[str]> into a format similar to the above one
 
 evaluate all combinations until you get <result>
 
 Problem with this approach:
 Knowing how and where to add Brackets would be a CHALLENGE

 Another Approach:
 
 _A2,
 Make a class that executes:
 a) '4 / 4 + 8 - 9 * 4' in 4*4! ways, so try 
 all orders, i.e. 
 
 ai) '4 / ((4+8) - 9) * 4' [4+8 -> 12-9 -> 4/3 -> (4/3)*4]
 aii) '4 / 4 + 8 - 9 * 4' [4/4 -> -9*4 -> 1+8 -> 9-36]
 
 ... Doing (4+8) first, or (8-9) first, or (9*4) first or (4/4) first,
 ...
 and then assign brackets in the order we evaluated in as the output
 
 - Find all combinations of operations
 - Apply them all one by one and check if they work <- 
"""

from itertools import permutations, combinations
import re

def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
 
def peek(stack):
    return stack[-1] if stack else None
 
def apply_operator(operators, values):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    values.append(eval("{0}{1}{2}".format(left, operator, right)))
 
def greater_precedence(op1, op2):
    precedences = {'+' : 0, '-' : 0, '*' : 1, '/' : 1}
    return precedences[op1] > precedences[op2]
 
def evaluate(expression):
    tokens = re.findall("[+/*()-]|\d+", expression)
    print(tokens)
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(int(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values)
                top = peek(operators)
            operators.pop() # Discard the '('
        else:
            # Operator
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values)
 
    return values[0]

if __name__ == '__main__':
    
    exp = '((20 - 10 ) * (30 - 20) / 10 + 10 ) * 2'
    print("Shunting Yard Algorithm: {0}".format(evaluate(exp)))
    print("Python: {0}".format(eval(exp)))
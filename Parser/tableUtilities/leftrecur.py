from bnf import *


def EliminateDirectLeftRecursion(name, rules: Rules):
    leftRecursiveRules = [deepcopy(rule) for rule in rules if rule[0] == name]
    otherRules = [deepcopy(rule) for rule in rules if rule not in leftRecursiveRules]

    if not leftRecursiveRules:
        return [(name, Rules.FromList(otherRules)),]
    
    newName = name.rstrip('>') + '\'>'
    for rule in leftRecursiveRules:
        rule.pop(0)
        rule.append(newName)
    leftRecursiveRules.append(['""',])

    for rule in otherRules:
        rule.append(newName)

    return [(name, Rules.FromList(otherRules)), (newName, Rules.FromList(leftRecursiveRules))]


def EliminateLeftRecursion(nts):
    nts = [(name, rules) for (name, rules) in nts]
    anotherntset = []

    for i in range(len(nts)):
        for j in range(i):
            for k in range(len(nts[i][1])):
                if nts[i][1][k][0] == nts[j][0]:
                    for h in range(len(nts[j][1])):
                        modifiedRule = deepcopy(nts[j][1][h])
                        for l in range(1, len(nts[i][1][k])):
                            modifiedRule.append(nts[i][1][k][l])
                        nts[i][1].Append(modifiedRule)
                    del nts[i][1][k]
        # print(f'before: \n{str(nts[i][1])}')
        anotherntset.extend(EliminateDirectLeftRecursion(*nts[i]))

    newNts = NonTerminals()
    for (name, key) in anotherntset:
        newNts[name] = key
    return newNts


if __name__ == '__main__':
    grammar = ParseBNF('new.txt').Build()
    # print(str(grammar))
    nts = EliminateLeftRecursion(grammar)
    print(str(nts))

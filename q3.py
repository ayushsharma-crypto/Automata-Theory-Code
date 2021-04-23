from copy import deepcopy
import sys
import json

def objectFA(s,l,tm,ss,fs):
    return {
        'states': s,
        'letters': l,
        'transition_matrix': tm,
        'start_states': ss,
        'final_states':fs
    }

def makeGNFA(DFA):
    deltaFunction = {}
    new_start_state = 'START'
    new_final_state = 'FINAL'
    deltaFunction[new_start_state] = {}
    deltaFunction[new_final_state] = {}
    deltaFunction[new_start_state][new_final_state] = None

    for st in DFA['states']:
        deltaFunction[st] = {}

        for st1 in DFA['states']:
            deltaFunction[st][st1] = None
        
        deltaFunction[new_start_state][st] = None if (st not in DFA['start_states']) else '$'
        deltaFunction[st][new_final_state] = None if (st not in DFA['final_states']) else '$'
        
    for arc in DFA['transition_matrix']:
        [ss, l, fs] = arc
        deltaFunction[ss][fs] = l if (deltaFunction[ss][fs]==None) else deltaFunction[ss][fs] + "+" + str(l)
    
    return new_start_state, new_final_state, deltaFunction

def getParentChildren(ripState, deltaFunction):
    parent = []
    children = []
    for childKey in deltaFunction[ripState]:
        label = deltaFunction[ripState][childKey]
        if (label==None) or (childKey==ripState):
            continue
        children.append(childKey)
    
    for stateKey in deltaFunction:
        if stateKey != ripState:
            childrenDict = deltaFunction[stateKey]
            if ripState not in childrenDict:
                continue
            elif childrenDict[ripState]==None:
                continue
            else:
                parent.append(stateKey)

    return parent, children

def updateArc(delPR, delRR, delRC, delPC):
    R1 = '' if (delPR==None) else '('+str(delPR)+')'
    R2 = '' if (delRR==None) else '('+str(delRR)+')*'
    R3 = '' if (delRC==None) else '('+str(delRC)+')'
    R4 = '' if (delPC==None) else '+('+str(delPC)+')'
    return R1+R2+R3+R4

def updateStateTransition(deltaFunction, parents, children, ripState):
    updatedDeltaFunction = deepcopy(deltaFunction)
    for child in children:
        for parent in parents:
            delPR = deltaFunction[parent][ripState]
            delRR = deltaFunction[ripState][ripState]
            delRC = deltaFunction[ripState][child]
            delPC = deltaFunction[parent][child]
            updatedDeltaFunction[parent][child] = updateArc(delPR, delRR, delRC, delPC)
    return updatedDeltaFunction

def eliminateState(ripState, updatedDeltaFunction):
    retDeltaFunction = {}
    for stateKey in updatedDeltaFunction:
        if stateKey != ripState:
            retDeltaFunction[stateKey] = {}
            for child in updatedDeltaFunction[stateKey]:
                if child != ripState:
                    val = updatedDeltaFunction[stateKey][child]
                    retDeltaFunction[stateKey][child] = val
    return retDeltaFunction

def stateElimination(new_start_state, new_final_state, deltaFunction, dfaStates):
    for ripState in dfaStates:
        parents, children = getParentChildren(ripState, deltaFunction)
        updatedDeltaFunction = updateStateTransition(deltaFunction, parents, children, ripState)
        deltaFunction = eliminateState(ripState, updatedDeltaFunction)
    return deltaFunction[new_start_state][new_final_state]

def convertDFAToRegex(DFA):  
    new_start_state, new_final_state, deltaFunction = makeGNFA(DFA)
    finalRegex = stateElimination(new_start_state, new_final_state, deltaFunction, DFA['states'])
    return finalRegex

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Unexceptable Format!")
        quit()

    try:
        input_file = open(sys.argv[1])
        rawDFA = json.load(input_file)
        s = rawDFA['states']
        l = rawDFA['letters']
        tm = rawDFA['transition_function']
        ss = rawDFA['start_states']
        fs = rawDFA['final_states']
        myDFA = objectFA(s, l, tm, ss, fs)
    except:
        print("Error accessing `input_file`")
        quit()
    
    finalRegex = convertDFAToRegex(myDFA)

    with open(sys.argv[2], "w+") as outfile: 
        json.dump({'regex': finalRegex}, outfile, indent=4)

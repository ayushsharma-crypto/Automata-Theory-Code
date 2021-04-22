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
    new_start_state = 'S'
    new_final_state = 'F'
    deltaFunction[new_start_state] = {}
    deltaFunction[new_final_state] = {}

    for st in DFA['states']:
        deltaFunction[st] = {}

        for st1 in DFA['states']:
            deltaFunction[st][st1] = None
        
        deltaFunction[new_start_state][st] = None
        deltaFunction[st][new_final_state] = None
        if st in DFA['start_states']:
            deltaFunction[new_start_state][st] = '$'
        if st in DFA['final_states']:
            deltaFunction[st][new_final_state] = '$'
        
    
    for arc in DFA['transition_matrix']:
        [ss, l, fs] = arc
        if deltaFunction[ss][fs] != None:
            deltaFunction[ss][fs] += f"+{l}"
        else:
            deltaFunction[ss][fs] = l
    
    return new_start_state, new_final_state, deltaFunction


def stateElimination(new_start_state, new_final_state, deltaFunction, DFA):
    pass


def convertDFAToRegex(DFA):  
    new_start_state, new_final_state, deltaFunction = makeGNFA(DFA)
    finalRegex = stateElimination(new_start_state, new_final_state, deltaFunction, DFA)
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
        tm = rawDFA['transition_matrix']
        ss = rawDFA['start_states']
        fs = rawDFA['final_states']
        myDFA = objectFA(s, l, tm, ss, fs)
    except:
        print("Error accessing `input_file`")
        quit()
    
    finalRegex = convertDFAToRegex(myDFA)

    with open(sys.argv[2], "w+") as outfile: 
        json.dump({'regex': finalRegex}, outfile, indent=4)

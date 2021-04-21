import sys
import json
import itertools


def objectFA(s,l,tm,ss,fs):
    return {
        'states': s,
        'letters': l,
        'transition_matrix': tm,
        'start_states': ss,
        'final_states':fs
    }


def epsilonClosure(nfaTransitionMatrix, nfaStartStateList):
    returnState = []
    for sst in nfaStartStateList:
        returnState.append(sst)
        for arc in nfaTransitionMatrix:
            [ss, l, fs] = arc
            if (l != '$') or (ss != sst):
                continue
            returnState.append(fs)
    return returnState


def allStatesCombination(nfaSTATES):
    return_state = []
    for i in range(len(nfaSTATES)+1):
        combination = [ list(tup) for tup in list(itertools.combinations(nfaSTATES,i))]
        return_state += combination
    return return_state


def getFinalState(nfaFinalStates,dfaStates):
    returnState = []
    for st in dfaStates:
        for fst in nfaFinalStates:
            if fst in st:
                returnState += st
    return returnState


def getTransitionedState(nfaTransitionMatrix, state, letter):
    pass


def formTransitionMatrix(nfaTransitionMatrix, dfaStates, dfaLetters):
    tm = []
    for st in dfaStates:
        for l in dfaLetters:
            transitionedState = getTransitionedState(nfaTransitionMatrix, st, l)
            tm.append(epsilonClosure(transitionedState))
    return tm


def convertNFAToDFA(NFA):
    DFA_L = NFA['letters'][:]
    DFA_S = allStatesCombination(NFA['states'])
    DFA_FS = getFinalState(NFA['final_states'],DFA_S)
    DFA_SS = epsilonClosure(NFA['transition_matrix'],NFA['start_states'])
    DFA_TM = formTransitionMatrix(NFA['transition_matrix'], DFA_S, DFA_L)

    return objectFA(DFA_S,DFA_L,DFA_TM,DFA_SS,DFA_FS)


if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Unexceptable Format!")
        quit()

    try:
        input_file = open(sys.argv[1])
        rawNFA = json.load(input_file)
        s = rawNFA['states']
        l = rawNFA['letters']
        tm = rawNFA['transition_matrix']
        ss = rawNFA['start_states']
        fs = rawNFA['final_states']
        myNFA = objectFA(s, l, tm, ss, fs)
    except:
        print("Error accessing `input_file`")
        quit()
    
    finalDFA = convertNFAToDFA(myNFA)

    with open(sys.argv[2], "w+") as outfile: 
        json.dump(finalDFA, outfile, indent=4)
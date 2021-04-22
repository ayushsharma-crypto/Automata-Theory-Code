import sys
import json


def objectDFA(s,l,tm,ss,fs):
    return {
        'states': s,
        'letters': l,
        'transition_matrix': tm,
        'start_states': ss,
        'final_states':fs
    }


def minimizeDFA(DFA):
    total_state = len(DFA['states'])
    table = [ [ False for _ in range(total_state) ] for _ in range(total_state) ]
    
    state_index = {}
    index_state = {}
    for i in range(total_state):
        state_index[DFA['states'][i]] = i
        index_state[i] = DFA['states'][i]
    
    for r in range(total_state):
        for c in range(total_state):
            s1 = DFA['states'][r]
            s2 = DFA['states'][c]
            if (s1 in DFA['final_states']) and (s2 not in DFA['final_states']):
                table[r][c]=True
            elif (s1 not in DFA['final_states']) and (s2 in DFA['final_states']):
                table[r][c]=True
    
    letterDict = {}
    for l in DFA['letters']:
        letterDict[l]=""
    deltaFunction = [ letterDict.copy() for _ in range(total_state) ]
    
    for arc in DFA['transition_matrix']:
        [ss, l, fs] = arc
        deltaFunction[state_index[ss]][l] = fs
    
    flag = True
    while flag:
        for r in range(total_state):
            for c in range(total_state):
                pass


            
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
        myDFA = objectDFA(s, l, tm, ss, fs)
    except:
        print("Error accessing `input_file`")
        quit()
    
    answer = minimizeDFA(myDFA)

    with open(sys.argv[2], "w+") as outfile: 
        json.dump(answer, outfile, indent=4)


import sys
import json
import re as regx

def objectNFA(s,l,tm,ss,fs):
    return {
        'states': s,
        'letters': l,
        'transition_matrix': tm,
        'start_states': ss,
        'final_states':fs
    }


def unitLenRegexToNFA(alphabet):
    s = ["Q0","Q1"]
    a = [alphabet]
    tm = [
        ["Q0",alphabet,"Q1"],
    ]
    ss = ["Q0"]
    fs = ["Q1"]
    return objectNFA(s, a, tm, ss, fs)



def concatenationNFA(NFA1, NFA2):
    # Making `a` array
    a = [ alphabet for alphabet in NFA1['letters']]
    for l in NFA2['letters']:
        if l not in a:
            a.append(l)

    # Making `s, ss and fs` array
    s = []
    ss = []
    fs = []
    tm = []
    for i in range(len(NFA1['states'])):
        current_state = NFA1['states'][i]
        s.append(current_state)
        if current_state in NFA1['start_state']:
            ss.append(current_state)

    for i in range(len(NFA2['states'])):
        current_state = NFA2['states'][i]
        effective_state = "Q"+str(i+len(NFA1['states']))
        s.append(effective_state)
        if current_state in NFA2['final_state']:
            fs.append(effective_state)
        for nfa1_final_state in NFA1['final_state']:
            tm.append([nfa1_final_state,'$',effective_state])

    # Making `tm` array
    for arc in NFA1['transition_matrix']:
        tm.append(arc)
    
    for arc in NFA2['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(int(os[1:])+len(NFA1['states']))
        n_ns = 'Q'+ str(int(ns[1:])+len(NFA1['states']))
        tm.append([n_os, il, n_ns ])
    
    return objectNFA(s, l ,tm, ss, fs)


def unionNFA(NFA1, NFA2):
    # Making `a` array
    a = [ alphabet for alphabet in NFA1['letters']]
    for l in NFA2['letters']:
        if l not in a:
            a.append(l)

    # Making `s, ss and fs` array
    s = ["Q0"]
    ss = ["Q0"]
    fs = []
    tm = []

    for i in range(len(NFA1['states'])):

        current_state = NFA1['states'][i]
        effective_state = 'Q'+str(i+1)
        s.append(effective_state)

        if current_state in NFA1['final_states']:
            fs.append(effective_state)
        if current_state in NFA1['start_states']:
            tm.append(['Q0','$',effective_state])


    for i in range(len(NFA2['states'])):

        current_state = NFA2['states'][i]
        effective_state = "Q"+str(i+1+len(NFA1['states']))
        s.append(effective_state)

        if current_state in NFA2['final_states']:
            fs.append(effective_state)
        if current_state in NFA2['start_states']:
            tm.append(['Q0','$',effective_state])
    
    # Making `tm` array
    for arc in NFA1['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(1+int(os[1:]))
        n_ns = 'Q'+ str(1+int(ns[1:]))
        tm.append([n_os, il, n_ns ])
    
    for arc in NFA2['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(1+int(os[1:])+len(NFA1['states']))
        n_ns = 'Q'+ str(1+int(ns[1:])+len(NFA1['states']))
        tm.append([n_os, il, n_ns ])
    
    return objectNFA(s, l, tm, ss, fs)





def starNFA(NFA):
    s = ['Q0']
    for i in range(len(NFA['states'])):
        effective_state = 'Q'+str(i+1)
        s.append(effective_state)
    
    only_final_state = f"Q{1+len(NFA['states'])}"
    s.append(only_final_state)

    l = [ letter for letter in NFA['letters'] ]
    ss = ['Q0']
    fs = [only_final_state]

    tm = []
    for arc in NFA['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(1+int(os[1:]))
        n_ns = 'Q'+ str(1+int(ns[1:]))
        tm.append([n_os, il, n_ns ])
    
    for st_state in NFA['start_states']:
        tm.append(['Q0','$','Q'+ str(1+int(st_state[1:]))])
    tm.append(['Q0','$',only_final_state])

    for fn_state in NFA['final_states']:
        tm.append(['Q'+ str(1+int(fn_state[1:])),'$',only_final_state])
        for st_state in NFA['start_states']:
            tm.append(['Q'+ str(1+int(fn_state[1:])),'$','Q'+ str(1+int(st_state[1:]))])
    
    return objectNFA(s, l, tm, ss, fs)



def convertToNFA(regular_expression):
    pass


if __name__=='__main__':
    if len(sys.argv) != 3:
        print("Unexceptable Format!")
        quit()
    

    try:
        input_file = open(sys.argv[1])
        regular_expression = json.load(input_file)
    except:
        print("Error accessing `input_file`")
        quit()
    
    convertToNFA(regular_expression)
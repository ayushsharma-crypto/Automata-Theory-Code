import json


def read_file(filename):
    '''
    This function will read the filename
    and return it's content.
    '''
    with open(filename,'r') as read_file:
        data=json.load(read_file)
        read_file.close()
    return data

def write_file(filename,data):
    '''
    This function will write data in the filename
    and return final content of it.
    '''
    with open(filename,'w+') as write_file:
        json.dump(data, write_file, indent = 4)
        write_file.close()
    return read_file(filename)


def objectFA(s,l,tm,ss,fs):
    return {
        'states': s,
        'letters': l,
        'transition_function': tm,
        'start_states': ss,
        'final_states':fs
    }

s1 = [ 'Q0', 'Q1', 'Q2']
l1 = ['a','b']
tm1 = [
    ['Q0','a','Q1'],
    ['Q0','b','Q1'],
    ['Q1','a','Q0'],
    ['Q1','b','Q2'],
]
ss1 = ['Q0']
fs1 = ['Q2']

s2 = [ 'Q0']
l2 = ['0','1']
tm2 = [
    ['Q0','0','Q0'],
    ['Q0','1','Q0'],
]
ss2 = ['Q0']
fs2 = ['Q0']


s3 = [ 'Q0', 'Q1', 'Q2']
l3 = ['a','b']
tm3 = [
    ['Q0','a','Q1'],
    ['Q0','b','Q2'],
    ['Q1','a','Q0'],
    ['Q1','b','Q1'],
    ['Q2','a','Q1'],
    ['Q2','b','Q0'],
]
ss3 = ['Q0']
fs3 = ['Q1','Q2']


s4 = [ 'Q0']
l4 = []
tm4 = []
ss4 = ['Q0']
fs4 = ['Q0']


all_dfa = [
    objectFA(s1,l1,tm1,ss1,fs1),
    objectFA(s2,l2,tm2,ss2,fs2),
    objectFA(s3,l3,tm3,ss3,fs3),
    objectFA(s4,l4,tm4,ss4,fs4),
]


for i in range(len(all_dfa)):
    cd = all_dfa[i]
    write_file(f"./q3-test-cases/{i}.txt",cd)
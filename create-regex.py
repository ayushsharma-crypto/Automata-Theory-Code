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
    with open(filename,'w') as write_file:
        json.dump(data, write_file, indent = 4)
        write_file.close()
    return read_file(filename)

all_regex = [
    {"regex":"a*b*"},
    {"regex":"$"},
    {"regex":"qwz*+y"},
    {"regex":"028+(99*+85)"},
    {"regex":"((2*)*)*"},
    {"regex":"$"},
    {"regex":"0*"},
    {"regex":"0*+1*"},
    {"regex":"b*a"},
    {"regex":"(1+1)"},
    {"regex":"1+1"},
    {"regex":"1"},
    {"regex":"0"},
    {"regex":"b"},
    {"regex":"a"},
    {"regex":""},
    {"regex":"(a+b)*+ba+c*"},
    {"regex":"(1+0*0(1+0))*1+0"},
]


for i in range(len(all_regex)):
    cd = all_regex[i]
    write_file(f"./regular-expression/{i}.txt",cd)
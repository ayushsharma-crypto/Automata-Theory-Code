import sys
import json

class MinimizeDFA():
    def __init__(self, rawDFA, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.s = rawDFA['states']
        self.l = rawDFA['letters']
        self.tm = rawDFA['transition_function']
        self.ss = rawDFA['start_states']
        self.fs = rawDFA['final_states']
        self.nfs = []
        self.table = [ [ 0 for _ in range(len(self.s)) ] for _ in range(len(self.s)) ]
        self.__nonAcceptStates()
        self.__SIMAP()
        self.__LIMAP()
        self.deltaFunction = self.__makeDeltaFunction()
        self.__initializeTable()
        self.__updateTm()
        self.newStates = self.__updateStates()
        self.finalAcceptStates = self.__getFinalStates()
        self.finalStartStates = self.__getFinalStartStates()
        self.finalTm = self.__getFinalTm()
        self.__saveDFA()
    
    def __nonAcceptStates(self):
        for st in self.s:
            if st not in self.fs:
                self.nfs.append(st)
    
    def __SIMAP(self):
        state_index = {}
        index_state = {}
        for i in range(len(self.s)):
            state_index[self.s[i]] = i
            index_state[i] = self.s[i]
        self.siMap = state_index
        self.isMap = index_state

    def __LIMAP(self):
        letters_index = {}
        index_letters = {}
        for i in range(len(self.l)):
            letters_index[self.l[i]] = i
            index_letters[i] = self.l[i]
        self.liMap = letters_index
        self.ilMap = index_letters

    def __makeDeltaFunction(self):
        letterDict = []
        for _ in range(len(self.l)):
            letterDict.append("")
        deltaFunction = [ letterDict.copy() for _ in range(len(self.s)) ]
        for arc in self.tm:
            [ss, l, fs] = arc
            deltaFunction[self.siMap[ss]][self.liMap[l]] = fs
        return deltaFunction

    def __initializeTable(self):
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if self.isMap[i] in self.fs and self.isMap[j] in self.nfs or self.isMap[i] in self.nfs and self.isMap[j] in self.fs:
                        self.table[i][j] = 1
                if self.isMap[i] in self.fs and self.isMap[j] in self.nfs or self.isMap[i] in self.nfs and self.isMap[j] in self.fs:
                        self.table[j][i] = 1

    def __updateTm(self):
        while True:
            exitLoop = False
            lengthTm = len(self.table)
            for i in range(lengthTm):
                lengthTmi = len(self.table[i])
                for j in range(lengthTmi):
                    if i==j:
                        continue
                    else:
                        if not self.table[i][j]:
                            for k in self.l:
                                if self.deltaFunction[i][self.liMap[k]] != "":
                                    if self.deltaFunction[j][self.liMap[k]] != "":
                                        x = self.deltaFunction[i][self.liMap[k]] 
                                        y = self.deltaFunction[j][self.liMap[k]]
                                        if self.table[self.siMap[x]][self.siMap[y]]:
                                            self.table[i][j] = 1
                                            exitLoop = True
                                            break
            if not exitLoop:
                break
    
    def __updateStates(self):
        newStates = []
        lengthTm = len(self.table)
        for i in range(lengthTm):
            lengthTmi = len(self.table[i])
            for j in range(lengthTmi):
                if i==j:
                    continue
                else:
                    if not self.table[i][j]:
                        if len(newStates)==0:
                            newStates.append([self.isMap[i],self.isMap[j]])
                        elif len(newStates) > 0:
                            temp = False
                            lengthNewStates = len(newStates)
                            for k in range(lengthNewStates):
                                if self.isMap[i] in newStates[k] or self.isMap[j] in newStates[k]:
                                    newStates[k].append(self.isMap[i])
                                    newStates[k].append(self.isMap[j])
                                    newStates[k] = list(dict.fromkeys(newStates[k]))
                                    temp = True
                                    break
                            if temp == False:
                                newStates.append([self.isMap[i],self.isMap[j]])

        for state in self.s:
            appendVar = False
            for i in newStates:
                if state in i:
                    appendVar = True
                    break
            if appendVar == False:
                newStates.append([state])

        return newStates
    
    def __getFinalStates(self):
        final_states = []
        flag = False
        for i in self.newStates:
            flag = False
            for states in i:
                for k in self.fs:
                    if states in k:
                        flag = True
                        break
                if flag:
                    break
            if flag:
                final_states.append(i)
        
        return final_states

    def __getFinalStartStates(self):
        final_states = []
        for i in self.newStates:
            for states in self.ss:
                if states in i:
                    final_states.append(i)
                    break
        
        return final_states
    
    def __getFinalTm(self):
        finalTm = []
        for state in self.newStates:
            for letters in self.l:
                new = self.deltaFunction[self.siMap[state[0]]][self.liMap[letters]]
                for j in self.newStates:
                    if new in j:
                        new = j
                        break
                finalTm.append([state, letters, new])

        return finalTm

    def __saveDFA(self):
        newDFA = self.__objectDFA()
        json.dump(newDFA, self.output_file, indent=4)

    def __objectDFA(self):
        return {
            'states': self.newStates,
            'letters': self.l,
            'transition_matrix': self.finalTm,
            'start_states': self.finalStartStates,
            'final_states':self.finalAcceptStates
        }
                

            
if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Unexceptable Format!")
        quit()

    try:
        input_file = open(sys.argv[1])
        output_file = open(sys.argv[2],"w+")
        rawDFA = json.load(input_file)
    except:
        print("Error accessing `input_file` or `output file`")
        quit()
    
    dfaInstance = MinimizeDFA(rawDFA,input_file,output_file)
    
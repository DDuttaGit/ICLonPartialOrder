import json, random, os, time
random.seed(10)

class LinearOrder:
    def __init__(self, j, k, file=''):
        if k < j:
            print("Query term must be greater than number of instances.")
            exit(1)
        self.instanceupto = j
        self.queryupto = k
        self.f = file
        self.problem_key = str(j)+'_'+str(k)
        if os.path.isfile(file):
            with open(self.f) as f:
                self.problems = json.load(f)
            self.problems['enumeration'].append(self.problem_key)
            self.problems[self.problem_key] = {}
        else:
            self.problems = dict({'enumeration': [], self.problem_key:{}})
            self.problems['enumeration'].append(self.problem_key)
        self.problems[self.problem_key]['queryUpto'] = k
        
    def pluginInstruction(self):
        self.problems[self.problem_key]['Relation Description'] = '''There is a relation less than "<" between strings made of decimal digits "0", "1", "2", "3", "4","5", "6", "7", "8" and "9".
                Given such strings x, y, and z, the relation has the following properties:
                (a) if x<y is true, then y<x is false,
                (b) if both x<y and y<z are true, then x<z is true, and
                (c) x<x is always false, for any x.'''
        self.problems[self.problem_key]['Task Description'] = '''Given the above information, determine if {string 1}<{string 2} is true.
                If it is true, your answer must be "{string 1}<{string 2}: true".
                If it is false, your answer must be "{string 1}<{string 2}: false".
                If you do not know if it is true or false, you answer must be "{string 1}<{string 2} : unknown".
                ''' 

        
    def examples(self):
        self.universe = [i for i in range(self.instanceupto+1)]
        self.problems[self.problem_key]['examples'] = []
        for i in range(self.instanceupto):
            a = str(self.universe[i]) + '<' + str(self.universe[i+1])
            self.problems[self.problem_key]['examples'].append(a)
    
    def generate_test(self):
        self.testuniverse = []
        p = random.randint(0, self.instanceupto//2)
        for i in range(self.instanceupto - p, self.instanceupto):
            for j in range(self.instanceupto, self.queryupto+1):
                taketheTupple = random.randint(0, 1)
                trueFalse = random.randint(0, 1)
                (a, b) = (i, j)
                if taketheTupple:
                    if trueFalse:
                        self.testuniverse.append({str(a) + '<' + str(b) : True})
                    else:
                        self.testuniverse.append({str(b) + '<' + str(a) : False})
        for i in range(self.instanceupto, self.queryupto):
            for j in range(i+1, self.queryupto+1):
                taketheTupple = random.randint(0, 1)
                trueFalse = random.randint(0, 1)
                (a, b) = (i, j)
                if taketheTupple:
                    if trueFalse:
                        self.testuniverse.append({str(a) + '<' + str(b) : True})
                    else:
                        self.testuniverse.append({str(b) + '<' + str(a) : False})
        self.problems[self.problem_key]['test'] = self.testuniverse

    def generate_test2(self):
        self.testuniverse = []
        p = random.randint(0, self.instanceupto//2)
        start_time = time.time()
        while len(self.testuniverse) <= 25:
            if (time.time() - start_time >= 3):
                break
            a = random.randint(self.instanceupto - p, self.instanceupto)
            b = random.randint(self.instanceupto, self.queryupto + 1)
            if a > b:
                (a, b) = (b, a)
            trueFalse = random.randint(0, 1)
            if trueFalse:
                if {str(b) + '<' + str(a) : False} not in self.testuniverse:
                    self.testuniverse.append({str(a) + '<' + str(b)  : True})
            else:
                if {str(b) + '<' + str(a) : False} not in self.testuniverse:
                    self.testuniverse.append({str(b) + '<' + str(a) : False})
        while len(self.testuniverse) <= 50:
            if (time.time() - start_time >= 3):
                break
            a = random.randint(self.instanceupto, self.queryupto)
            b = random.randint(self.instanceupto, self.queryupto)
            if a > b:
                (a, b) = (b, a)
            trueFalse = random.randint(0, 1)
            if trueFalse:
                if {str(b) + '<' + str(a) : False} not in self.testuniverse:
                    self.testuniverse.append({str(a) + '<' + str(b) : True})
            else:
                if {str(b) + '<' + str(a) : False} not in self.testuniverse:
                    self.testuniverse.append({str(b) + '<' + str(a) : False})
        self.problems[self.problem_key]['test'] = self.testuniverse
        
        
        
    def exit(self):
        # print(self.problems)
        if self.f != '':
            with open(self.f, 'w') as f:
                json.dump(self.problems, f)
        else:
            with open(self.f, 'w') as f:
                json.dump(self.problems, f)
                
def cook(shot, complexity):
    filename = 'LinearOrderDec_50.json'
    if os.path.exists(filename):
        os.remove(filename)
    listofproblems = []
    for i in range(1, shot+1):
        for j in range(1, complexity+1):
            listofproblems.append((i, i+j))
        
    for base, query in listofproblems:
        L1 = LinearOrder(j=base, k=query, file=filename)
        L1.pluginInstruction()
        L1.examples()
        L1.generate_test2()
        L1.exit()
        print(f'\rCooked %d-shot %d-complex data.'%(base, query-base), end='')

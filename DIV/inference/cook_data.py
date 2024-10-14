import json, random, time
random.seed(10)

prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

def get_n_divisors(p, n):
    divisors, res = [], []

    # Check all numbers from 1 to p
    for i in range(1, p + 1):
        if p % i == 0:  # If i divides p evenly
            divisors.append(i)
    random.shuffle(divisors)
    for d in divisors[:n]:
        res.append({f"%d | %d" % (d, p): True})
    return res

class DivisiblityPreparation:
    def __init__(self, base, skip, file):
        self.bases, self.skips = base+1, skip+1
        self.problems = {'enumeration': []}
        self.file = file

    def make_samples(self):
        for base in range(1, self.bases):
            examples = self.genExamples(base)[1:]
            for skip in range(1, self.skips):
                p = f"%d_%d"%(base, base+skip)
                self.problems['enumeration'].append(p)
                self.make_sample(p, base, base+skip, examples)
        with open(self.file, 'w') as f:
            json.dump(self.problems, f)

    def make_sample(self, p, base, query, examples):
        self.problems[p] = {'queryUpto': query}
        self.problems[p]['Relation Description'] = '''
        There is a relation divides '|' between decimal integers composed of digits "0", "1", "2", "3", "4", "5", "6", "7", "8" and "9".
        Given such integers x, y, and z, the relation has the following properties:
        (a) if x|y is true, then y|x is false,
        (b) if both x|y and y|z are true, then x|z is true, and
        (c) x|x is always true, for any x.
        '''
        self.problems[p]['Task Description'] = '''
        Given the above information, determine if {integer 1}|{integer 2} is true.
        If it is true, your answer must be "{integer 1}|{integer 2}: true".
        If it is false, your answer must be "{integer 1}|{integer 2}: false".
        If you do not know if it is true or false, you answer must be "{integer 1}|{integer 2} : unknown".
        '''
        self.problems[p]['examples'] = examples
        self.problems[p]['test'] = self.generateTest(p, query)

    def genExamples(self, base):
        res = []
        for i in range(1, base + 1):
#            cnt = 0
            for p in prime_list:
                if i % p == 0:
                    d = f"%d | %d" % (i//p, i)
                    res.append(d)
#                    cnt += 1
#                if cnt >= 2:
#                    break
            if len(res) == 0:
                res.append(f"%d | %d" % (1, i))
            res.append("%d | %d" % (i, i))

        return res

    def generateTest(self, p, query):
        test = []
        t0 = time.time()
        for _ in range(10):
            t = time.time()
            i, j = random.randint(1, query), random.randint(1, query)
            (i, j) = (i, j) if i <=j else (j, i)
            d = {f"%d | %d" %(i, j): True} if j % i == 0 else {f"%d | %d" % (i, j): False}
            if d not in test:
                test.append(d)
            if t - t0 > 2:
                break

        appeared = []
        for _ in range(25):
            t = time.time()
            i, j = random.randint(1, 3), random.randint(1,query)
            if j not in appeared:
                test += get_n_divisors(j, i)
                appeared.append(j)
            if t - t0 > 5:
                break

        random.shuffle(test)
        test = test[:30]
        base = int(p.split('_')[0])
        print("\rCooked %d-shot %d complex data."%(base, query-base), end='')
        return test

def cook(shot, complexity):
    Div = DivisiblityPreparation(shot, complexity, file='./DIV_30.json')
    Div.make_samples()
import pandas as pd, random, time

prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
random.seed(10)

def get_n_divisors(p, n):
    divisors, res = [], []

    # Check all numbers from 1 to p
    for i in range(1, p + 1):
        if p % i == 0:  # If i divides p evenly
            divisors.append(i)
    random.shuffle(divisors)
    for d in divisors[:n]:
        res.append([f"%d | %d" % (d, p), 1])
    return res


class DF:
    def __init__(self, base, fact_skip):
        self.train_df, self.eval_df, self.Eval_df, self.eval_train_df = [], [], [], []
        self.create_train_df(base)
        self.create_eval_df(base, fact_skip)
        self.create_eval_train_df(base)

    def create_train_df(self, base):
        for i in range(1, base + 1):
#             cnt = 0
            for p in prime_list:
                tf = random.randint(0, 1)
                if i % p == 0:
                    d = [f"%d | %d" % (i//p, i), 1] if tf else [f"%d | %d" % (i, i//p), 0]
                    self.train_df.append(d)
#                     cnt += 1
#                 if cnt >= 2:
#                     break
            if len(self.train_df) == 0:
                self.train_df.append([f"%d | %d" % (1, i), 1])
            self.train_df.append([f"%d | %d" % (i, i), 1])
        self.train_df = pd.DataFrame(self.train_df)
        self.train_df.columns = ["text", "labels"]

    def create_eval_df(self, base, fact_skip):
        t0 = time.time()
        skip = fact_skip * base
        for _ in range(25):
            t = time.time()
            i, j = random.randint(1, skip), random.randint(base, skip)
            D = [f"%d | %d" % (j, i), 1] if (i % j == 0) else [f"%d | %d" % (j, i), 0]
            if D not in self.Eval_df:
                self.Eval_df.append(D)
            d = [f"%d | %d" % (j, i), 1] if (i % j == 0) else [f"%d | %d" % (j, i), 0]
            self.eval_df.append(d)
            if t - t0 >= 2:
                break
        for _ in range(25):
            t = time.time()
            i, j = random.randint(1, 3), random.randint(base, skip)
            self.Eval_df = self.Eval_df + get_n_divisors(j, i)
            if t - t0 > 5:
                break
        random.shuffle(self.Eval_df)
        self.Eval_df = pd.DataFrame(self.Eval_df)
        self.Eval_df.columns = ["text", "labels"]
        self.eval_df = pd.DataFrame(self.eval_df)

    def create_eval_train_df(self, base):
        t0 = time.time()
        for _ in range(25):
            t = time.time()
            i, j = random.randint(1, base), random.randint(1, base)
            (i, j) = (j, i) if (i % j == 0) else (i, j)
            tf = random.randint(0, 1)
            D = [f"%d | %d" % (i, j), 1] if tf else [f"%d | %d" % (j, i), 0]
            if D not in self.eval_train_df:
                self.eval_train_df.append(D)
            if t - t0 >= 2:
                break
        for _ in range(25):
            t = time.time()
            i, j = random.randint(1, 3), random.randint(1, base)
            self.eval_train_df = self.eval_train_df + get_n_divisors(j, i)
            if t - t0 > 5:
                break
        random.shuffle(self.eval_train_df)
        self.eval_train_df = pd.DataFrame(self.eval_train_df)
        self.eval_train_df.columns = ["text", "labels"]
        train_df_texts = set(self.train_df["text"].tolist())
        self.eval_train_df = self.eval_train_df[~self.eval_train_df["text"].isin(train_df_texts)]

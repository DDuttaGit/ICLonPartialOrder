import pandas as pd, random, time


class DF:
    def __init__(self, base, fact_skip):
        self.train_df, self.eval_df, self.Eval_df, self.eval_train_df = [], [], [], []
        self.create_train_df(base)
        self.create_eval_df(base, fact_skip)
        self.create_eval_train_df(base)

    def create_train_df(self, base):
        for i in range(1, base - 1):
            tf = random.randint(0, 1)
            d = [f"%d < %d" % (i, i + 1), 1] if tf else [f"%d < %d" % (i + 1, i), 0]
            self.train_df.append(d)
        self.train_df = pd.DataFrame(self.train_df)
        self.train_df.columns = ["text", "labels"]

    def create_eval_df(self, base, fact_skip):
        skip = fact_skip * base
        t0 = time.time()
        for _ in range(50):
            t  = time.time()
            i, j = random.randint(1, skip), random.randint(base, skip)
            (i, j) = (i, j) if i < j else (j, i)
            tf = random.randint(0, 1)
            D = [f"%d < %d" % (i, j), 1] if tf else [f"%d < %d" % (j, i), 0]
            d = [f"%d < %d" % (i, j)] if tf else [f"%d < %d" % (j, i)]
            if D not in self.Eval_df:
                self.Eval_df.append(D)
            self.eval_df.append(d)
            if t - t0 >= 2:
                break
        self.Eval_df = pd.DataFrame(self.Eval_df)
        self.Eval_df.columns = ["text", "labels"]
        self.eval_df = pd.DataFrame(self.eval_df)

    def create_eval_train_df(self, base):
        t0 = time.time()
        for _ in range(50):
            t  = time.time()
            i, j = random.randint(1, base), random.randint(1, base)
            (i, j) = (i, j) if i < j else (j, i)
            tf = random.randint(0, 1)
            D = [f"%d < %d" % (i, j), 1] if tf else [f"%d < %d" % (j, i), 0]
            if D not in self.eval_train_df:
                self.eval_train_df.append(D)
            if t - t0 >= 2:
                break
        self.eval_train_df = pd.DataFrame(self.eval_train_df)
        self.eval_train_df.columns = ["text", "labels"]
        train_df_texts = set(self.train_df["text"].tolist())
        self.eval_train_df = self.eval_train_df[~self.eval_train_df["text"].isin(train_df_texts)]

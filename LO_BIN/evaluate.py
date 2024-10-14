import json, numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.size'] = 8

filename = 'LinearOrderBin_50_op'
models = ['gemma2', 'llama3', 'mathstral']


def evaluate_mismatch():
    with open('./OP/' + filename + '.json') as f:
        problems = json.load(f)
    for p in problems['enumeration']:
        test_values = []
        for t in problems[p]['test']:
            test_values.append(list(t.values())[0])
        for model in models:
            problems[p]['answer'][model + '_mismatch'] = []
            answer = problems[p]['answer'][model].replace('\n', ' ').replace('*', '')
            op = []
            # print(answer)
            try:
                for word in answer.split(' '):
                    if word.lower() == 'true':
                        op.append(True)
                    elif word.lower() == 'false':
                        op.append(False)
                    elif word.lower() == 'unknown':
                        op.append(False)
                m = 0
                if len(op) == len(test_values):
                    for i in range(len(op)):
                        tf = (1 - int(op[i] == test_values[i]))
                        m += tf
                        problems[p]['answer'][model + '_mismatch'].append(tf)
                    problems[p]['answer'][model + '_mismatch'].append(m)
                else:
                    problems[p]['answer'][model + '_mismatch'].append(len(test_values))
            except:
                problems[p]['answer'][model + '_mismatch'].append(str(len(test_values)) + '-FLD')
    with open('./OP/' + filename + '_eval.json', 'w') as f:
        json.dump(problems, f)


def compare(shot, complexity):
    with open('./OP/' + filename + '_eval.json') as f:
        problems = json.load(f)
    mismatch_matrix = np.zeros((shot, complexity, 4))

    for p in problems['enumeration']:
        base, query = int(p.split('_')[0]), int(p.split('_')[1]) - int(p.split('_')[0])
        for cnt, model in enumerate(models):
            mismatch_matrix[base - 1][query - 1][cnt] = problems[p]['answer'][model + '_mismatch'][-1]
        mismatch_matrix[base - 1][query - 1][3] = len(problems[p]['test']) if len(problems[p]['test']) != 0 else 1


    np.save('./OP/' + filename, mismatch_matrix)
    return mismatch_matrix


def showPlotsRow(shot, complexity):
    mismatch_matrix = np.load('./OP/' + filename + '.npy')

    G, L, M, T = np.ones((shot, complexity)), np.ones((shot, complexity)), np.ones((shot, complexity)), np.ones(
        (shot, complexity))
    for i in range(shot):
        for j in range(complexity):
            if j == 0:
                G[i, j] = mismatch_matrix[i, j, 0]
                L[i, j] = mismatch_matrix[i, j, 1]
                M[i, j] = mismatch_matrix[i, j, 2]
                T[i, j] = mismatch_matrix[i, j, 3]
            else:
                G[i, j] = G[i, j - 1] + mismatch_matrix[i, j, 0]
                L[i, j] = L[i, j - 1] + mismatch_matrix[i, j, 1]
                M[i, j] = M[i, j - 1] + mismatch_matrix[i, j, 2]
                T[i, j] = T[i, j - 1] + mismatch_matrix[i, j, 3]
    GM, LM, MM = np.mean(1 - G / T, axis=0), np.mean(1 - L / T, axis=0), np.mean(1 - M / T, axis=0)
    GS, LS, MS = np.std(1 - G / T, axis=0), np.std(1 - L / T, axis=0), np.std(1 - M / T, axis=0)

    plt.fill_between(range(1, shot + 1), GM - GS, GM + GS, alpha=.3, color='blue', label='Gemma2')
    plt.plot(range(1, shot + 1), GM, color='blue')
    plt.fill_between(range(1, shot + 1), LM - LS, LM + LS, alpha=.3, color='red', label='Llama3')
    plt.plot(range(1, shot + 1), LM, color='red')
    plt.fill_between(range(1, shot + 1), MM - MS, MM + MS, alpha=.3, color='green', label='Mathstral')
    plt.plot(range(1, shot + 1), MM, color='green')
    plt.title('(x, y) denotes Along Row accuracy.')
    plt.legend()
    plt.tight_layout()
    plt.savefig('./OP/LOBinAlongRow.png')
    plt.show()
    plt.close()


def showPlotsCol(shot, complexity):
    mismatch_matrix = np.load('./OP/' + filename + '.npy')
    G, L, M, T = np.ones((shot, complexity)), np.ones((shot, complexity)), np.ones((shot, complexity)), np.ones(
        (shot, complexity))
    for j in range(complexity):
        for i in range(shot):
            if i == 0:
                G[i, j] = mismatch_matrix[i, j, 0]
                L[i, j] = mismatch_matrix[i, j, 1]
                M[i, j] = mismatch_matrix[i, j, 2]
                T[i, j] = mismatch_matrix[i, j, 3]
            else:
                G[i, j] = G[i - 1, j] + mismatch_matrix[i, j, 0]
                L[i, j] = L[i - 1, j] + mismatch_matrix[i, j, 1]
                M[i, j] = M[i - 1, j] + mismatch_matrix[i, j, 2]
                T[i, j] = T[i - 1, j] + mismatch_matrix[i, j, 3]

    GM, LM, MM = np.mean(1 - G / T, axis=1), np.mean(1 - L / T, axis=1), np.mean(1 - M / T, axis=1)
    GS, LS, MS = np.std(1 - G / T, axis=1), np.std(1 - L / T, axis=1), np.std(1 - M / T, axis=1)
    plt.fill_between(range(1, complexity + 1), GM - GS, GM + GS, alpha=.3, color='blue', label='Gemma2')
    plt.plot(range(1, complexity + 1), GM, color='blue')
    plt.fill_between(range(1, complexity + 1), LM - LS, LM + LS, alpha=.3, color='red', label='Llama3')
    plt.plot(range(1, complexity + 1), LM, color='red')
    plt.fill_between(range(1, complexity + 1), MM - MS, MM + MS, alpha=.3, color='green', label='Mathstral')
    plt.plot(range(1, complexity + 1), MM, color='green')
    plt.title('(x, y) denotes Along Column accuracy.')
    plt.legend()
    plt.tight_layout()
    plt.savefig('./OP/LOBinAlongColumn.png')
    plt.show()
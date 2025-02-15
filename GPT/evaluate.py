import json, numpy as np
import matplotlib.pyplot as plt


plt.rcParams['text.usetex'] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.size'] = 12


def evaluate_mismatch(model, task, filename):
    with open('./OP_'+task+'/' + filename + '.json') as f:
        problems = json.load(f)
    exception, less, equal, exact, total = 0, 0, 0, 0, 0
    for p in problems['enumeration']:
        test_values = []
        for t in problems[p]['test']:
            test_values.append(list(t.values())[0])

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

    with open('./OP_'+task+'/'+ filename + '_eval.json', 'w') as f:
        json.dump(problems, f)


def compare(shot, complexity, task, filename):
    with open('./OP_'+task+'/' + '_eval.json') as f:
        problems = json.load(f)
    mismatch_matrix = np.zeros((shot, complexity, 2))  # First 10 rows are blank and the last one too

    for p in problems['enumeration']:
        base, query = int(p.split('_')[0]), int(p.split('_')[1]) - int(p.split('_')[0])
        for cnt, model in enumerate(models):
            mismatch_matrix[base-1][query - 1][cnt] = problems[p]['answer'][model + '_mismatch'][-1]
        mismatch_matrix[base-1][query - 1][-1] = len(problems[p]['test'])

    np.save('./OP_'+task+'/' + filename, mismatch_matrix)
    return mismatch_matrix


def showPlotsRow(shot, complexity, task, filename):
    mismatch_matrix = np.load('./OP_'+task+'/' + filename + '.npy')
    gm = np.mean(1 - mismatch_matrix[:, :, 0] / mismatch_matrix[:, :, -1], axis=0)
    gs = np.std(1 - mismatch_matrix[:, :, 0] / mismatch_matrix[:, :, -1], axis=0)

    G, T = np.ones((shot, complexity)), np.ones((shot, complexity))
    for i in range(shot):
        for j in range(complexity):
            if j == 0:
                G[i, j] = mismatch_matrix[i, j, 0]
                T[i, j] = mismatch_matrix[i, j, -1]
            else:
                G[i, j] = G[i, j - 1] + mismatch_matrix[i, j, 0]
                T[i, j] = T[i, j - 1] + mismatch_matrix[i, j, -1]
    GM = np.mean(1 - G / T, axis=0)
    GS = np.std(1 - G / T, axis=0)

    np.save('./OP_'+task+'/RG', np.asarray([GM-GS, GM+GS]))


def showPlotsCol(shot, complexity, task, filename):
    mismatch_matrix = np.load('./OP_'+task+'/' + filename + '.npy')

    gm = np.mean(1 - mismatch_matrix[:, :, 0] / mismatch_matrix[:, :, -1], axis=1)
    gs = np.std(1 - mismatch_matrix[:, :, 0] / mismatch_matrix[:, :, -1], axis=1)
  
    G, L, T = np.ones((shot,complexity)), np.ones((shot,complexity)), np.ones((shot,complexity))
    for j in range(complexity):
        for i in range(shot):
            if i == 0:
                G[i,j] = mismatch_matrix[i,j,0]
                T[i,j] = mismatch_matrix[i,j,-1]
            else:
                G[i,j] = G[i-1,j] + mismatch_matrix[i,j,0]
                T[i,j] = T[i-1,j] + mismatch_matrix[i,j,-1]
    GM = np.mean(1-G/T, axis=1)
    GS = np.std(1-G/T, axis=1)
    np.save('./OP_'+task+'/CG', np.asarray([GM-GS, GM+GS]))


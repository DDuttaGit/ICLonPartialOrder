import json, numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.size'] = 12
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsfonts}'

def plot():
    RG_LO, CG_LO = np.load('./OP_LO/RG' + '.npy'), np.load('./OP_LO/CG' + '.npy')
    RG_LOBIN, CG_LOBIN = np.load('./OP_LO_BIN/RG' + '.npy'), np.load('./OP_LO_BIN/CG' + '.npy')
    RG_DIV, CG_DIV = np.load('./OP_DIV/RG' + '.npy'), np.load('./OP_DIV/CG' + '.npy')

    plt.fill_between(range(1, complexity+1), RG_LO[0], RG_LO[1], alpha=.3, color='red',label=r'$(\mathbb{N}, <)$')
    plt.plot(range(1, complexity+1), (RG_LO[0]+RG_LO[1])/2, color='red')
    plt.fill_between(range(1, complexity+1), RG_LOBIN[0], RG_LOBIN[1], alpha=.3, color='green',label=r'$(\{0,1\}^*, <)$')
    plt.plot(range(1, complexity+1), (RG_LOBIN[0]+RG_LOBIN[1])/2, color='green')
    plt.fill_between(range(1, complexity+1), RG_DIV[0], RG_DIV[1], alpha=.3, color='blue',label=r'$(\mathbb{N}, |)$')
    plt.plot(range(1, complexity+1), (RG_DIV[0]+RG_DIV[1])/2, color='blue')
    plt.xlabel(r'Complexity ($c$)')
    plt.ylabel(r'Mean Cumulative Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.savefig('ROW.pdf')
    plt.close()

    plt.fill_between(range(1, shots+1), CG_LO[0], CG_LO[1], alpha=.3, color='red',label=r'$(\mathbb{N}, <)$')
    plt.plot(range(1, shots+1), (CG_LO[0]+CG_LO[1])/2, color='red')
    plt.fill_between(range(1, shots+1), CG_LOBIN[0], CG_LOBIN[1], alpha=.3, color='green',label=r'$(\{0,1\}^*, <)$')
    plt.plot(range(1, shots+1), (CG_LOBIN[0]+CG_LOBIN[1])/2, color='green')
    plt.fill_between(range(1, shots+1), CG_DIV[0], CG_DIV[1], alpha=.3, color='blue',label=r'$(\mathbb{N}, |)$')
    plt.plot(range(1, shots+1), (CG_DIV[0]+CG_DIV[1])/2, color='blue')
    plt.xlabel(r'Shots ($k$)')
    plt.ylabel(r'Mean Cumulative Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.savefig('COLUMN.pdf')
    plt.close()

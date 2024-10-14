import pickle
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams['font.size'] = 10

models = ["bert", "roberta", "xlnet"]


def check_saturation(base):
    MCA_test, MCA_range_acc = [], []
    for model in models:
        file = 'OP/ResultsLO_' + model + '.pkl'
        with open(file, 'rb') as f:
            result = pickle.load(f)
        test_acc, train_range_acc = result[0], result[1]
        accs1, accs2 = [], []
        Accs1, Accs2 = [], []
        i, a1, a2 = 1, 0, 0
        for i1, i2 in zip(test_acc, train_range_acc):
            accs1.append(i1['accuracy']), accs2.append(i2['accuracy'])
            a1 += i1['accuracy']
            a2 += i2['accuracy']
            Accs1.append(a1 / i), Accs2.append(a2 / i)
            i += 1
        MCA_test.append(Accs1), MCA_range_acc.append(Accs2)
    colors = ["red", "green", "blue"]
    ax = plt.gca()
    ax.set_ylim([0, 1])
    plt.plot(range(10, base+5, 5), MCA_test[0], color=colors[0], label=models[0])
    plt.plot(range(10, base+5, 5), MCA_range_acc[0], color=colors[0], alpha=0.5)

    plt.plot(range(10, base+5, 5), MCA_test[1], color=colors[1], label=models[1])
    plt.plot(range(10, base+5, 5), MCA_range_acc[1], color=colors[1], alpha=0.5)

    plt.plot(range(10, base+5, 5), MCA_test[2], color=colors[2], label=models[2])
    plt.plot(range(10, base+5, 5), MCA_range_acc[2], color=colors[2], alpha=0.5)

    plt.legend()
    plt.tight_layout()
    plt.savefig("OP/LO10Finetuned.png")
    plt.show()


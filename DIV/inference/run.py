import argparse
from cook_data import cook
from infer import infer
from evaluate import evaluate_mismatch, compare, showPlotsRow, showPlotsCol

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--shot', type=int, required=True, help="Maximum shots to be provided. In case of inferece it is inductive.")
    parser.add_argument('--complexity', type=int, help="Maximum Complexity to be added, in case of inference it is inductive.")
    parser.add_argument('--eval', required=True, choices=['yes', 'no'], help="Evaluate or no Evaluate the result.")
    args = parser.parse_args()

    cook(args.shot, args.complexity)

    infer()

    if args.eval == 'yes':
        evaluate_mismatch()
        compare(args.shot, args.complexity)
        showPlotsRow(args.shot, args.complexity)
        showPlotsCol(args.shot, args.complexity)

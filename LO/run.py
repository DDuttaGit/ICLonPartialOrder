import os, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=["inference", "finetune"], required=True, help="Either inference or finetuning.")
    parser.add_argument('--shot', type=int, required=True, help="Maximum shots to be provided. In case of inferece it is inductive, else it moves in interval of 10.")
    parser.add_argument('--complexity', type=int, help="Maximum Complexity to be added, in case of inference it is inductive, else it is considered as single complexity point.")
    parser.add_argument('--complexity_fact', type=int, help="Complexity to be added, in case of finetuning.")
    parser.add_argument('--eval', required=True, choices=['yes', 'no'], help="Evaluate or no Evaluate the result.")
    args = parser.parse_args()

    if args.type == 'inference':
        os.system("python3 LO/%s/run.py --shot %d --complexity %d --eval %s"%(args.type, args.shot, args.complexity, args.eval))
    elif args.type == 'finetune':
        os.system("python3 LO/%s/run.py --shot %d --complexity_fact %d --eval %s"%(args.type, args.shot, args.complexity_fact, args.eval))

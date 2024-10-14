import os, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', choices=["LO", "LO_BIN", "DIV"], required=True, help="Choose LO for linear order, LO for linear order in binary or DIV for division.")
    parser.add_argument('--type', choices=["inference", "finetune"], required=True, help="Either inference or finetuning.")
    parser.add_argument('--shot', type=int, required=True, help="Maximum shots to be provided. In case of inferece it is inductive, else it moves in interval of 10.")
    parser.add_argument('--complexity', type=int, help="Maximum Complexity to be added, in case of inference it is inductive, else it is considered as single complexity point.")
    parser.add_argument('--complexity_fact', type=int, help="Complexity to be added, in case of finetuning.")
    parser.add_argument('--eval', required=True, choices=['yes', 'no'], help="Evaluate or no Evaluate the result.")
    args = parser.parse_args()
    
    if args.task == "LO_BIN" and args.type == "finetune":
        print("We have not implemented this combination.")
        exit()
    if args.type == 'inference':
        args.complexity_fact = 0
    elif args.type == 'finetune':
        args.complexity = 0
    os.system("python3 ./%s/run.py --type %s --shot %d --complexity %d --complexity_fact %d --eval %s"%(args.task, args.type, args.shot, args.complexity, args.complexity_fact, args.eval))

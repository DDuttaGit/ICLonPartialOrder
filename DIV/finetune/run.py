import os, argparse
# os.system("python3 LO/%s/run.py --shot %d --complexity_fact %d --eval %s"%(args.type, args.shot, args.complexity_fact, args.eval))
from dataset import DF
import pickle
from model import ModelTrainer
from eval import check_saturation

if not os.path.exists('OP'):
    os.makedirs('OP')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--shot', type=int, required=True, help="Maximum shots to be provided. In case of inferece it skips by 5.")
    parser.add_argument('--complexity_fact', type=int, help="Maximum Complexity to be added, in case of finetune it is a factor like 2,3,...")
    parser.add_argument('--eval', required=True, choices=['yes', 'no'], help="Evaluate or no Evaluate the result.")
    args = parser.parse_args()

    for model in ["bert", "roberta", "xlnet"]:
        Result_eval, Result = [], []

        for base in range(10, args.shot+5, 5):
            print("BASE==================: ", base, model)
            df = DF(base, args.complexity_fact)
            trainer = ModelTrainer(df.train_df, df.Eval_df, df.eval_train_df, model)
            trained_model, result_eval, result = trainer.train_and_evaluate()
            Result_eval.append(result_eval)
            Result.append(result)

        with open("./OP/ResultsDIV_" + model + '.pkl', "wb") as fp:
            pickle.dump([Result_eval, Result], fp)

    if args.eval == 'yes':
        check_saturation(args.shot)
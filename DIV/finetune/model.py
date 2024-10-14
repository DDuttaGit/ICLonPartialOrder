from simpletransformers.classification import ClassificationModel, ClassificationArgs
import torch


class ModelTrainer:
    def __init__(self, train_df, eval_df, eval_train_df, model = None):
        self.train_df = train_df
        self.eval_df = eval_df
        self.eval_train_df = eval_train_df
        self.cuda_available = torch.cuda.is_available()

        self.model_args = ClassificationArgs()
        self.model_args.num_train_epochs = 250
        self.model_args.save_steps = -1
        self.model_args.save_model_every_epoch = False
        self.model_args.use_multiprocessing = False
        self.model_args.use_multiprocessing_for_evaluation = False
        self.model_args.overwrite_output_dir = True
        multiplier = 2 if self.train_df.shape[0] >= 500 else 1
        self.model_args.train_batch_size = 64 * multiplier
        self.model_args.eval_batch_size = 64
        if model == "roberta":
            self.model = ClassificationModel(
                "roberta", "roberta-base", use_cuda=self.cuda_available, args=self.model_args
            )  #"roberta", "roberta-base"; "bert", "bert-base-cased"; "xlnet", "xlnet-base-cased"

        elif model == "bert":
            self.model = ClassificationModel(
                "bert", "bert-base-cased", use_cuda=self.cuda_available, args=self.model_args
            )  # "roberta", "roberta-base"; "bert", "bert-base-cased"; "xlnet", "xlnet-base-cased"

        elif model == "xlnet":
            self.model = ClassificationModel(
                "xlnet", "xlnet-base-cased", use_cuda=self.cuda_available, args=self.model_args
            )  # "roberta", "roberta-base"; "bert", "bert-base-cased"; "xlnet", "xlnet-base-cased"
    def train_and_evaluate(self):
        self.model.train_model(self.train_df)
        result_eval, model_outputs, wrong_predictions = self.model.eval_model(self.eval_df)
        print(result_eval)

        result, model_outputs, wrong_predictions = self.model.eval_model(self.eval_train_df)
        print(result)

        return self.model, result_eval, result

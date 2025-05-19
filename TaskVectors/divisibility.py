import json
import os
import random
from typing import List, Any, Optional, Iterable

from core import config
from core.data.datasets.few_shot_dataset import FewShotDataset
from core.data.tasks.task import Task
from transformers import PreTrainedTokenizer


class DivisionTask(Task):
    def __init__(self, tokenizer: PreTrainedTokenizer, num_examples: int, no_prompts: int,
                 complexity: int = None):
        super().__init__(tokenizer)
        file = os.path.join(config.DATA_DIR, 'divisibility', "Divisibility3.json")
        with open(file) as f:
            self.problems = json.load(f)
        self.start, self.end = num_examples*150-1, num_examples*150
        p = self.problems["enumeration"][self.end-1]
        self.mapping = self.problems[p]['examples']
        self.no_prompts = no_prompts
        if complexity != None:
            self.complexity = complexity
            self.start, self.end = num_examples*150 - 1 + self.complexity, num_examples*150 + self.complexity

    def calc_output(self, inp: Any) -> Any:
        pass

    def sample_inputs(self, num_inputs: int, exclude: Optional[Iterable[Any]] = ()) -> List[Any]:
        input_space = self.mapping
        return random.sample(list(set(input_space) - set(exclude)), num_inputs)

    def num_examples(self) -> int:
        return len(self.mapping)

    def compare_outputs(self, output1: str, output2: str) -> bool:
        tf_dict = {"True": True, "true": True, "TRUE": True,
                   "False": False, "false": False, "FALSE": False}
        if output1 in tf_dict.keys():
            return tf_dict[output1] == output2
        return False

    def create_datasets(self, num_datasets: int, num_examples: int) -> List[FewShotDataset]:
        Datasets = []
        for p in self.problems['enumeration'][self.start:self.end]:
            train_inputs, train_outputs = [], []
            instruction = self.problems[p]['Relation Description']
            for e in self.problems[p]['examples']:
                [a, b] = list(map(int, e.split(' | ')))
                if random.choice([True, False]):
                    train_inputs.append(e), train_outputs.append('True')
                else:
                    e = str(b) + " | " + str(a)
                    train_inputs.append(e), train_outputs.append('False')
            for q in self.problems[p]['test'][:self.no_prompts]:
                test_input, test_output = list(q.keys())[0], list(q.values())[0]
                Datasets.append(
                    FewShotDataset(
                        train_inputs,
                        train_outputs,
                        test_input,
                        test_output,
                        instruction + "\nBased on the examples below, answer the last query."
                    )
                )
        return Datasets

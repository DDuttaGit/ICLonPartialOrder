import string
from typing import Dict

from core.data.tasks.increment_task import IncrementTask
from core.data.tasks.list_operation_task import ListOperationTask
from core.data.tasks.token_operation_task import TokenOprationTask
from core.data.tasks.mapping_task import MappingTask
from core.data.tasks.translation_task import TranslationTask
from core.data.tasks.divisibility import DivisionTask
from core.data.tasks.linearorder import LinearOrderTask
from core.data.tasks.task import Task

from transformers import PreTrainedTokenizer

TASK_TYPE_TO_CLASS = {
    "increment": IncrementTask,
    "list_operation": ListOperationTask,
    "token_operation": TokenOprationTask,
    "mapping": MappingTask,
    "translation": TranslationTask,
    # "sentiment": SentimentTask,
    "division": DivisionTask,
    "linearorder": LinearOrderTask
}


ALL_TASKS = {
    # Algorithmic
    "algorithmic_next_letter": {
        "task_type": "increment",
        "task_kwargs": {"increment": +1},
    },
    "algorithmic_prev_letter": {
        "task_type": "increment",
        "task_kwargs": {"increment": -1},
    },
    "algorithmic_list_first": {
        "task_type": "list_operation",
        "task_kwargs": {"operation": "first", "list_lenghts": range(2, 5)},
    },
    "algorithmic_list_last": {
        "task_type": "list_operation",
        "task_kwargs": {"operation": "last", "list_lenghts": range(2, 5)},
    },
    "algorithmic_list_min": {
        "task_type": "list_operation",
        "task_kwargs": {"operation": "min", "list_lenghts": range(2, 5), "elements_space": list(string.digits)},
    },
    "algorithmic_list_max": {
        "task_type": "list_operation",
        "task_kwargs": {"operation": "max", "list_lenghts": range(2, 5), "elements_space": list(string.digits)},
    },
    "algorithmic_list_length": {
        "task_type": "list_operation",
        "task_kwargs": {"operation": "length", "list_lenghts": range(1, 4)},
    },
    "algorithmic_to_upper": {
        "task_type": "token_operation",
        "task_kwargs": {"operation": "to_upper", "input_space": list(string.ascii_lowercase)},
    },
    "algorithmic_to_lower": {
        "task_type": "token_operation",
        "task_kwargs": {"operation": "to_lower", "input_space": list(string.ascii_uppercase)},
    },
    "algorithmic_char_to_int": {
        "task_type": "token_operation",
        "task_kwargs": {"operation": "char_to_int", "input_space": list(string.ascii_lowercase[:9])},
    },  # low performance
    "algorithmic_int_to_char": {
        "task_type": "token_operation",
        "task_kwargs": {"operation": "int_to_char", "input_space": list(string.digits[1:])},
    },
    # Translation
    "translation_fr_en": {
        "task_type": "translation",
        "task_kwargs": {"mapping_type": "translation", "mapping_name": "fr_en"},
    },
    "translation_it_en": {
        "task_type": "translation",
        "task_kwargs": {"mapping_type": "translation", "mapping_name": "it_en"},
    },
    "translation_es_en": {
        "task_type": "translation",
        "task_kwargs": {"mapping_type": "translation", "mapping_name": "es_en"},
    },
    "translation_en_fr": {
        "task_type": "translation",
        "task_kwargs": {"mapping_type": "translation", "mapping_name": "en_fr"},
    },
    "translation_en_it": {
        "task_type": "translation",
        "task_kwargs": {"mapping_type": "translation", "mapping_name": "en_it"},
    },
    "translation_en_es": {
        "task_type": "translation",
        "task_kwargs": {"mapping_type": "translation", "mapping_name": "en_es"},
    },
    # Linguistic
    "linguistic_present_simple_gerund": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "linguistic", "mapping_name": "present_simple_gerund"},
    },
    "linguistic_present_simple_past_simple": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "linguistic", "mapping_name": "present_simple_past_simple"},
    },
    "linguistic_present_simple_past_perfect": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "linguistic", "mapping_name": "present_simple_past_perfect"},
    },
    "linguistic_singular_plural": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "linguistic", "mapping_name": "singular_plural"},
    },
    "linguistic_plural_singular": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "linguistic", "mapping_name": "plural_singular"},
    },
    "linguistic_antonyms": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "linguistic", "mapping_name": "antonyms"},
    },
    # Knowledge
    "knowledge_country_capital": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "knowledge", "mapping_name": "country_capital", "allow_prefix": True},
    },
    "knowledge_person_language": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "knowledge", "mapping_name": "person_language", "allow_prefix": True},
    },
    "knowledge_location_continent": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "knowledge", "mapping_name": "location_continent", "allow_prefix": True},
    },
    "knowledge_location_religion": {
        "task_type": "mapping",
        "task_kwargs": {"mapping_type": "knowledge", "mapping_name": "location_religion", "allow_prefix": True},
    },
    # "sentiment": {
    #     "task_type": "sentiment",
    #     "task_kwargs": {"allow_prefix": True},
    # },
    # Division
    "division_10_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10},
    },
    "division_20_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 10, "no_prompts": 10},
    },
    "division_25_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 12, "no_prompts": 10},
    },
    "division_30_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 14, "no_prompts": 10},
    },
    "division_40_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 14, "no_prompts": 10},
    },
    "division_50_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 21, "no_prompts": 10},
    },
    "division_60_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 14, "no_prompts": 10},
    },
    "division_70_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 14, "no_prompts": 10},
    },
    "division_75_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 31, "no_prompts": 10},
    },
    "division_80_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 33, "no_prompts": 10},
    },
    "division_90_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 36, "no_prompts": 10},
    },
    "division_100_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 40, "no_prompts": 10},
    },
    "division_10_10_10": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 10},
    },
    "division_10_10_20": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 20},
    },
    "division_10_10_25": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 25},
    },
    "division_10_10_30": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 30},
    },
    "division_10_10_40": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 40},
    },
    "division_10_10_50": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 50},
    },
    "division_10_10_60": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 60},
    },
    "division_10_10_70": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 70},
    },
    "division_10_10_75": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 75},
    },
    "division_10_10_80": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 80},
    },
    "division_10_10_90": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 90},
    },
    "division_10_10_100": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 5, "no_prompts": 10, "complexity": 100},
    },
    "division_80_5": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 33, "no_prompts": 5},
    },
    "division_100_3": {
        "task_type": "division",
        "task_kwargs": {"num_examples": 40, "no_prompts": 3},
    },
    "linearorder_10_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10},
    },
    "linearorder_10_10_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 10},
    },
    "linearorder_10_10_20": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 20},
    },
    "linearorder_10_10_25": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 25},
    },
    "linearorder_10_10_30": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 30},
    },
    "linearorder_10_10_40": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 40},
    },
    "linearorder_10_10_50": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 50},
    },
    "linearorder_10_10_60": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 60},
    },
    "linearorder_10_10_70": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 70},
    },
    "linearorder_10_10_75": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 75},
    },
    "linearorder_10_10_80": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 80},
    },
    "linearorder_10_10_90": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 90},
    },
    "linearorder_10_10_100": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 100},
    },
    "linearorder_20_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 11, "no_prompts": 10},
    },
    "linearorder_25_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 16, "no_prompts": 10},
    },
    "linearorder_30_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 21, "no_prompts": 10},
    },
    "linearorder_40_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 31, "no_prompts": 10},
    },
    "linearorder_50_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 41, "no_prompts": 10},
    },
    "linearorder_60_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 51, "no_prompts": 10},
    },
    "linearorder_70_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 61, "no_prompts": 10},
    },
    "linearorder_75_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 66, "no_prompts": 10},
    },
    "linearorder_80_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 71, "no_prompts": 10},
    },
    "linearorder_90_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 81, "no_prompts": 10},
    },
    "linearorder_100_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 91, "no_prompts": 10},
    },
    "linearorderbin_10_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_20_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 11, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_25_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 16, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_30_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 21, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_40_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 31, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_50_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 41, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_60_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 51, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_70_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 61, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_75_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 66, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_80_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 71, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_90_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 81, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_100_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 91, "no_prompts": 10, "bin": True},
    },
    "linearorderbin_10_10_10": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 10, "bin": True},
    },
    "linearorderbin_10_10_20": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 20, "bin": True},
    },
    "linearorderbin_10_10_25": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 25, "bin": True},
    },
    "linearorderbin_10_10_30": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 30, "bin": True},
    },
    "linearorderbin_10_10_40": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 40, "bin": True},
    },
    "linearorderbin_10_10_50": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 50, "bin": True},
    },
    "linearorderbin_10_10_60": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 60, "bin": True},
    },
    "linearorderbin_10_10_70": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 70, "bin": True},
    },
    "linearorderbin_10_10_75": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 75, "bin": True},
    },
    "linearorderbin_10_10_80": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 80, "bin": True},
    },
    "linearorderbin_10_10_90": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 90, "bin": True},
    },
    "linearorderbin_10_10_100": {
        "task_type": "linearorder",
        "task_kwargs": {"num_examples": 1, "no_prompts": 10, "complexity": 100, "bin": True},
    },
}


def get_task(task_type: str, task_kwargs: Dict[str, str], tokenizer: PreTrainedTokenizer) -> Task:
    task = TASK_TYPE_TO_CLASS[task_type](**task_kwargs, tokenizer=tokenizer)
    return task


def get_task_by_name(tokenizer: PreTrainedTokenizer, task_name: str) -> Task:
    task_args = ALL_TASKS[task_name]
    task = get_task(task_args["task_type"], task_args["task_kwargs"], tokenizer)
    return task


def get_all_tasks(tokenizer: PreTrainedTokenizer) -> Dict[str, Task]:
    tasks = {task_name: get_task_by_name(tokenizer, task_name) for task_name in ALL_TASKS}
    return tasks

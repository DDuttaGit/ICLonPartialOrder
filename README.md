
# Assessing the Limits of In-Context Learning Beyond Functions Using Partially Ordered Sets
## Anonymous 

This is the codebase to reproduce the result.


### Install Dependecies
`$ sh ./requirement.sh`

### Infer using prompt (Local LLMs)
`$ python3 run.py --task DIV --type inference --shot 4 --complexity 4 --eval yes`

### Finetune
`$ python3 run.py --task DIV --type finetune --shot 25 --complexity_fact 2 --eval yes`

---

### Details about the options

|       Option      |    Values it can take   | Use[^1] |                                                                                                                                                                                          Description                                                                                                                                                                                          |
|:-----------------:|:-----------------------:|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|       `task`      |  `LO`, `LO_BIN`, `DIV`  |    M    | The task to be performed - Linear order, Linear Order Binary or Division respectively.                                                                                                                                                                                                                                                                                                        |
|       `type`      | `inference`, `finetune` |    M    | The type of experiment to be conducted.                                                                                                                                                                                                                                                                                                                                                       |
|       `shot`      |       $\mathbb{Z}$      |    M    | In the case when `type` is `finetune` assign `shot` with value greater than $10$, to exclude pathelogical cases.                                                                                                                                                                                                                                                                              |
|    `complexity`   |       $\mathbb{Z}$      |    C    | Works when `type` is `inference`. In this case, say if `shot` is $12$  and `complexity` is $5$ then there will be computations on prompts $P_{1,2}, ... ,P_{1,6}, ..., P_{12,13}, ... ,P_{12,17}$ as defined in the paper.                                                                                                                                                                    |
| `complexity_fact` |       $\mathbb{Z}$      |    C    | Works when `type` is `finetune`. In this case, say if `shot` is $25$  and `complexity_fact` is $2$ then there will be three separate training will be on points sampled from $(1, 10), (1, 15)$ and $(1, 20)$ satisfying the minimal example structure of partial order. And for these case the test points will sampled from range $(1, 2\times 10), (1, 2\times 15)$ and $(1, 2\times 20)$. |
|       `eval`      |       `yes`, `no`       |    M    | Whether evaluation will be petformed [^2].                                                                                                                                                                                                                                                                                                                                                    |


### Infer using prompt (GPT)

- Fix values for shots and complexity, say $K$, $C$.
- Prepare Three Datasets (LO, LO_BIN, DIV) using the `cook` method from `cook_data.py` of respective task directories. Keep the arguments `shot` and `complexity` in method `cook` as $K$ and $C$ for _all three tasks_.
- Place the data files to the directory `GPT`.
- Change line 23, 24 and 25 of `GPT.py` with your OpenAI API key, preferred `model_name` and $K$, $C$ respectively.
- Execute `$ python3 GPT.py` from the directory `GPT`.
- After successful execution two plots `ROW.pdf` and `COLUMN.pdf` wil be produced with self-explanatory labels on them.


### Task Vectors
To reproduce the tSNE plots, we suggest to clone the orginal [source-code](https://github.com/roeehendel/icl_task_vectors) [^3]. And after a successful exceution of the orginal project:
- Add the files `TaskVectors/divisibility.py` and `TaskVectors/linearorder.py` to `core/data/tasks/` of the cloned repo.
- Replace the conent of file `core/data/task_helpers.py` with that of `TaskVectors/task_helpers.py`.
- Store the data (For `LO` (also `LO_BIN`) and `DIV`) produced from first experiment in new directories `data/linearorder` and `data/divisibility` repectively.
- run `run_script.sh experiments.task_vectors_robustness`.

[^1]: M: Mandatory, C: Conditional.
[^2]: Results and evaluated figures will be stored in directory  `OP` with self-explanatory names.
[^3]: https://github.com/roeehendel/icl_task_vectors

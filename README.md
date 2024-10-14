
# Understanding In-Context Learning in LLMs on Partially Ordered Set

This is the codebase to reproduce the result


### Install Dependecies
`$ sh ./requirement.sh`

### Infer using prompt
`$ python3 run.py --task DIV --type inference --shot 4 --complexity 4 --eval yes`

### Finetune
`$ python3 run.py --task DIV --type finetune --shot 25 --complexity_fact 2 --eval yes`

---

### Details about the options

The `task` option can take value `LO`, `LO_BIN` or `DIV` depending upon the task is Linear order, Linear Order Binary or Division.

The `type` option can take `inference` or `finetune`.

In the case when `type` is `finetune` assign `shot` with value greater than `10`, to exclude pathelogical cases.

The `complexity` is used with `type` `inference`. In this case, say if `shot` is `12`  and `complexity` is `5` then there will be computations on prompts $P_{1,2}, ... P_{1,6}, ..., P_{12,13}, .. P_{12,17}$ as defined in the paper.


The `complexity_fact` is used with `type` `finetune`. In this case, say if `shot` is `25`  and `complexity_fact` is `2` then there will be three separate training will be on points sampled from `(1, 10)`, `(1, 15)` and `(1, 20)` satisfying the minimal example structure of partial order. And for these case the test points will sampled from range `(1, 2\*10)`, `(1, 2\*15)` and `(1, 2\*20)`.

Evaluation resluts will be saved in directory `OP` with self-explanatory names. 

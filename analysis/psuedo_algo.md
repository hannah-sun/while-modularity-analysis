# Analysis Algorithm

Our goal is to find "snippets" of code that use the same variables, and output these sections of code as suggestions for possible more modular structures through refactoring.

###### Graph generation

* For each "level" of code, take `ASSIGN`, `IF`, and `WHILE` blocks of AST and make them nodes. 
* Assign weighted, directed edges that correspond to variable usage similarity between each pair of variables. (If they share `n` many variables, then the weight of the edge is `n`, so the weight could be 0). Each edge always originates from the node that is sequentially earlier in the original code, and goes to the node that comes later sequentially between the pair.
* Do step 1 and 2 for each level of code (within every `IF` and `WHILE` block).


###### Analysis

* Find connected components -- those are the "snippets".


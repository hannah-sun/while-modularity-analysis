# Analysis Algorithm

Our goal is to find "snippets" of code that use the same variables, and output these sections of code as suggestions for possible more modular structures through refactoring.

#### Graph generation

#TODO explain each levels and how to use recursion
* For each "level" of code, take `ASSIGN`, `IF`, and `WHILE` blocks of AST and make them nodes. 
* At each node, there is will be a map and two sets: read and write. The map is of key-value pairs where the key represents a variable and the value represents the last line at which the variable was assigned. The read set represents all variables that are read from within the node; for an `IF` or `WHILE` block, any variables read in statements inside the block will be in the read set of the block node. The write set represents all variables that are assigned to inside the block.
  * For instance, this if node will have a write set containing the elements {y, z, w} and a read set containing the elements {r, b, z}.
  ```
  if (x  < 0) {
    y = 5;
    z = r + b;
  }
  else {
    w = z / b;
  }
  ```
* Once each level has all of its nodes labeled with a map and two sets, we will create a two sets of edges: write-to, and read-from. 

#### Analysis

* Build and merge snippets appropriately.


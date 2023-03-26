Planned result:

REST API web service which is able to index several local repositories and to answer a simple question whether or not a given file with code is similar to something inside these repositories.

### 2 parts of the task are done:
#### Part 1
The program bypasses all files in repositories and makes an inverted index based on Token.Names from these files.

The inverted index is saved to file `"inverted_index.json"`

As an example of repository [a game project](https://github.com/JuliaKud/kitchen_garden) that contains files with `.cpp` and `.h` extension was chosen

#### Part 2
Interaction with user is carried out through the console.

The user should run the program with `"python3 main.py"` and then input their code ending with `ctrl+D`. 

The input is saved into auxiliary file `"file_to_check.cpp"`.

The result is either `"OK"` or `"The code has {percentage} similarity with {file_name}"`
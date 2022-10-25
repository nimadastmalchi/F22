# CS 131 - Brewin Project Testcase Crowd-Sourcing

Hello! This is a fork from the official CS 131 autograder repository, with some additional testcases. Feel free to just use it -- but I ***strongly*** encourage that you create a pull request and provide your own testcases to the repository. 

Note: the following instructions are adapted from the official repo.

## Usage

First, clone this repository and make it your working directory:

```sh
$ git clone
# or, with SSH
$ git clone git@github.com:UCLA-CS-131/fall-22-autograder.git
...
cd fall-22-autograder
```

### Running Brewin Scripts

To run the Brewin interpreter with a given file, simply run `./brewin.sh <FILE>`. 

### Local Auto-testing

To test locally, you will additionally need a **working implementation** of the project; the minimum example is an `interpreterv1.py` that implements the `Interpreter` class. Place this in the same directory as `tester.py`; or alternatively, link it (and other supporting files) to this directory:

```sh
ln -s <PATH_TO_PROJECT_DIR>/interpreterv1.py interpreterv1.py
```

Then to test project 1, simply run `python3 tester.py 1`. Similarly, you can test other versions with `python3 tester.py <VER>`. 

Note: we also output the results of the terminal output to `results.json`.

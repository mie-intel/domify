# Domify

Tcframe Problem Package to Domjudge Problem Package Converter

## What is Domify and Why?

Domify is a python script used to convert Tcframe (by IA TOKI) Problem Package Format into DOMJudge Problem Package Format. Fyi, Tcframe is a Test Case Generator Framework use to develop some competitive programming problem. Usually, Tcframe's problem package directories structure will be like this

```
<problem-name>/
    tc/
        <problem-name>_x.in
        <problem-name>_x.out
        ...
        <problem-name>_sample_x.in
        <problem-name>_sample_x.out
    spec.cpp
    solution.cpp
    scorer.cpp (optional)
    communicator.cpp (optional)
```

But DOMJudge's problem package directories structure will be like this

```
<folder-name>/
    data/
        sample
            file-sample_1.in
            file-sample_1.ans
            ...
            file-sample-x.in
            file-sample-x.ans
        secret
            file_1.in
            file_1.ans
            ...
            file_x.in
            file_x.ans

    domjudge-problem.ini
    problem.yaml
    problem.pdf (.md or else)
```

Which I found out exhausting to construct the domjudge problem package by hand.

So I create the script to aid my works.

## Prerequisites

1. Python 3 (as simple as that)
2. A complete Tcframe folder to convert (it must have the same directory structure as above)

## How to use it?

1. Build the spec.cpp file using `tcframe build`
2. Compile your solution.cpp into an executable file
3. Run `./runner` program to generate all testcases
4. Go to the parent folder of your tcframe problem package folder.
5. Then, run the python script with the following format
   ```
    python3 domify.py <tcframe-directory>
   ```
   For the example, if the tcframe directories' name `problems`, then type this following command
   ```
    python3 domify.py problems
   ```
   You can also run the script using `Py`. But the main thing is, you should run it with Python interpreter that supports Python3.
6. Then, input all necessary data for your problem, such as
   - problem's name
   - problem's code
   - time limit (in second)
   - memory limit (in kb)
   - problem's color
7. After that, the script will generate `package/` folder inside the tcframe directory. Inside that folder, you will find the domjudge problem package directory already has already been made just for you ❤️

# HeavyLifter Usage

## Intro

This is a CLI program to do heavy lifting based on an instructions. The stacks of boxes and instructions are in the same file.

The definition and example of HeavyLifter is available [here](docs/MANUAL.md), as well as an example of a correct input [file](docs/instruction_example.txt).

## Usage

The program has a positional argument which is the path of the file with the instructions and the starting state of the boxes.
If the file cannot be opened, an error is thrown.

Two different versions _(v1, v2)_ are available, by default _v1_ will be used.

## HOW TO

### Requirements

- Python3.13

#### For running tests
- UV package manager

### Command
```
python main.py filepath [--version {v1,v2}]
```

## Validation

Following validations apply:

1. There must be exactly one _bottom_ in the input file
2. Stack IDs (any valid number) must be provided under the stacks, before the _bottom_
3. There cannot be more than 10 stacks
4. There must be at least 1 valid box to move (eg. `|A|`)
5. Empty boxes are not allowed (eg. `||`, `| |`)
6. All the movement instructions must match the following format: `move #1 from #2 to #3`
7. Source and destination stack IDs in movement instructions must be present in the stack ID row

> [!TIP]
> - If an instruction wants to move more boxes than the source stack actually has, a warning is logged and all the boxes in the source stack are moved to the destination.
> - If there are no movement instructions provided, the result stacks will match the input.

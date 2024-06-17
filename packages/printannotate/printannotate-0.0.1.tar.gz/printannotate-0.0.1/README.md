# printannotate

A Python package to annotate print statements with encoded information about the calling script and line number.

![CI](https://github.com/saikotek/printannotate/actions/workflows/ci.yml/badge.svg)
![Latest Release](https://img.shields.io/github/v/release/saikotek/printannotate)

## Example
### Input
```py
print(f"i: {i:_}")
print(f"f: {f:.2f}")
print(f"f: {f:.0f}")
print(f"f: {f:_.2f}")
```
### Output
```py
# number formatting
print(f"i: {i:_}") # i: 1_000_000_000
print(f"f: {f:.2f}") # f: 10123.14
print(f"f: {f:.0f}") # f: 10123
print(f"f: {f:_.2f}") # f: 10_123.14
```

## Installation

You can install the package using pip:

pip install printannotate

## Usage

`py -m printannotate <script_path>`<br>
or<br>
`printannotate <script_path>`

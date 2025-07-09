# ndrwahltexte

A command-line tool to process election data from JSON files and output relevant information as a string.

---

## Installation

You can install the package directly from GitHub using pip:

```bash
pip install git+https://github.com/NorddeutscherRundfunk/ndrwahltexte.git
```

Or clone the repo and install locally:

```bash
git clone https://github.com/NorddeutscherRundfunk/ndrwahltexte.git
cd ndrwahltexte
pip install .
```

## Usage

Run the command-line tool ndrwahltexte with the required -f (or --file) option to specify the JSON file to process:

```bash
ndrwahltexte -f path/to/election.json
```

Enable verbose output with the -v flag:

```bash
ndrwahltexte -f path/to/election.json -v
```

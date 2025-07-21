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

This tool reads a JSON object from standard input (stdin) and prints processed output to the console (stdout). Errors are printed to stderr

You can use it by piping JSON data into the command:
```bash
echo '{"wahl": "" }}' | ndrwahltexte
```

Or by piping data from a file:
```bash
cat wahl.json | ndrwahltexte
```

Outputs are written as JSON data with generated text under:

{
  "wahl": {
    "ergebnis": {
      "texte": {
        "Titel": ""
      }
    }
  }
}

Errors are output to stderr as:

{
  "error": {
    "type": "",
    "message": ")",
    "traceback": ""
  }
}

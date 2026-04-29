########################
#
# NDR Wahltexte - Election Text Generator Controller
# Main entry point for election text generation
# -> l.sander.fm@ndr.de
#
#########################

import json
import sys
from .election import parse_election_data
from .text_generator import generate_election_text
from .utils import write_error


def main():
    """
    Main entry point for election text generation.
    Reads JSON from stdin, generates text, writes to stdout.
    """
    # Read input
    try:
        raw_data = json.load(sys.stdin)
    except Exception as e:
        write_error(e)
        sys.exit(1)

    # Parse election data
    variables = parse_election_data(raw_data)

    # Generate text
    output = generate_election_text(variables)

    # Handle errors
    if 'error' in output:
        error_obj = {
            "error": {
                "type": "ValidationError",
                "message": output['error'],
                "traceback": ""
            }
        }
        print(json.dumps(error_obj, indent=2), file=sys.stderr)
        sys.exit(1)

    # Write output
    json.dump(output, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
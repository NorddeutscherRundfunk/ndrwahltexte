"""
Shared utility functions for ndrwahltexte
"""

import json
import sys
import traceback


def write_error(e):
    """Gibt Fehler als JSON auf stderr aus."""
    error_obj = {
        "error": {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }
    }
    print(json.dumps(error_obj, indent=2), file=sys.stderr)
#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sandbox.settings")
    sys.path[:0] = [str(Path(__file__).resolve().parent.parent)]

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

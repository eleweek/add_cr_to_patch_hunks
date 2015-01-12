#!/usr/bin/env python
import argparse
import re

parser = argparse.ArgumentParser(description='Adds CR to patch')
parser.add_argument('--extra_cr', dest='extra_cr', action='store_true', default=False, help="Terminate hunk lines with CRCRLF. Sounds weird, but this is a workaround for gist.github.com, because it replaces CRLF -> LF(so CRCRLF becomes CRLF)")
parser.add_argument('input_diff_filename', help='diff_to_modify')
parser.add_argument('output_diff_filename', help='diff_to_modify')

args = parser.parse_args()

hunk_line_terminator = '\r\r\n' if args.extra_cr else '\r\n'

with open(args.input_diff_filename, 'r') as f:
    lines = f.readlines()

modified_lines = []
in_hunk = False
for line in lines:
    if not re.match(r'^[ +-]', line):
        in_hunk = False
    modified_lines.append(line.replace('\n', hunk_line_terminator) if in_hunk else line)
    if line.startswith("@@"):
        in_hunk = True

with open(args.output_diff_filename, 'w') as f:
    f.write(''.join(modified_lines))

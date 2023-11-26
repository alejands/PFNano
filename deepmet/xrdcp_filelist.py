#!/usr/bin/env python3
import sys, subprocess

# Expected file format (ignores empty lines):

# ### DatasetA                <--- Will save inputs below in directory NanoAOD/DatasetA
# /store/user/.../file1.root
# ...
# /store/user/.../fileN.root
#
# ### DatasetB
# /store/user/...

# Note: '#' and '##' are still treated as commented out lines,
# but a line starting with '###' will be treated as a new
# directory name.

input_list = 'xrootd_filenames.txt'

def main():
    with open(input_list) as f:
        output_directory = ''
        for line in f.readlines():
            filename = line.lstrip().replace('\n', '')  # remove newlines and leading whitespace
            if filename[0] == '':                       # skip empty lines
                continue

            # New directory/save location
            # Lines starting with '###' make a new directory for the files below that line
            if filename[:3] == '###':
                output_directory = 'NanoAOD/' + filename[4:].lstrip()
                cmd_mkdir = f'mkdir -p {output_directory}'
                run_cmd(cmd_mkdir)
                continue

            # Check for other commented out lines ('#' or '##')
            if filename[:1] == '#':                     # True for both cases
                continue

            # Run 'xrdcp'
            cmd_xrdcp = f'xrdcp root://cms-xrd-global.cern.ch:/{filename} {output_directory}'
            run_cmd(cmd_xrdcp)

def run_cmd(cmd):
    try:
        print('Running command:', cmd)
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1) # Suppress noisy exception message. Print statements are clear enough

if __name__ == '__main__':
    if sys.version_info.major < 3 or sys.version_info.minor < 6:
        msg =  '\nThis script is written for python>=3.6\n'
        msg += 'You can adapt it for earlier python versions fairly easily but that\'s on you.'
        raise SystemError(msg)
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\tNo it's fine, I didn't want to finish running anyway. >_>\n")


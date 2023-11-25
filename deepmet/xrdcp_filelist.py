#!/usr/bin/env python3
import sys, subprocess

# Note: This script does not check formatting on input list
# Expected file format (ignores empty lines):

# ### DatasetA                <--- will save inputs below in directory NanoAOD/DatasetA
# /store/user/.../file1.root
# ...
# /store/user/.../fileN.root
#
# ### DatasetB
# /store/user/...

input_list = 'xrootd_filenames.txt'

def main():
    print('Make sure you ran "voms-proxy-init ..." first')

    with open(input_list) as f:
        output_directory = ''
        for line in f.readlines():
            filename = line.lstrip().replace('\n', '') # remove newlines and leading whitespace
            if filename[0] == '':                      # skip empty lines
                continue

            # New directory/save location
            # Lines starting with '###' make a new directory for the files below that line
            if filename[:3] == '###':
                output_directory = 'NanoAOD/' + filename[4:].lstrip()
                subprocess.run(['mkdir', '-p', output_directory], check=True)
                continue

            # Run 'xrdcp'
            cmd = f'xrdcp root://cms-xrd-global.cern.ch:/{filename} {output_directory}'
            print('Running command:', cmd)
            run_cmd(cmd)

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1) # Suppress noisy exception message. Print statements are clear enough

if __name__ == '__main__':
    if sys.version_info.major < 3 or sys.version_info.minor < 7:
        msg =  '\nThis script is written for python>=3.7\n'
        msg += 'You can adapt it for earlier python versions fairly easily but that\'s on you.'
        raise SystemError(msg)
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\tWow you didn't let me finish running. Rude.\n")


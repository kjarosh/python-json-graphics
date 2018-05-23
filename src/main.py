#!/usr/bin/env python3

'''
@author: Kamil Jarosz
'''

import argparse
import sys

from json_graphics import GraphicsFile, InvalidFormatException


def main(prog=None):
    parser = argparse.ArgumentParser(description='Render JSON graphics.')
    parser.add_argument('infile')
    parser.add_argument('-o', '--output', required=False, metavar='outfile',
                        type=str, help='specify output file')
    if prog != None: parser.prog = prog
    parsed = parser.parse_args(sys.argv[1:])
    
    input_file = parsed.infile
    output_file = parsed.output
    
    try:
        gf = GraphicsFile.from_file(input_file)
    except FileNotFoundError:
        print('File \'' + input_file + '\' not found', file=sys.stderr)
        sys.exit(1)
    except InvalidFormatException as ife:
        print('Invalid file format: ' + str(ife), file=sys.stderr)
        sys.exit(1)
    
    img = gf.to_image()
    
    if output_file == None:
        img.show()
    else:
        try:
            img.save(output_file)
        except ValueError as ve:
            print('Invalid output file name: ' + str(ve), file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()


#!/usr/bin/env python3

'''
@author: Kamil Jarosz
'''

import argparse
import sys

from json_graphics import GraphicsFile, InvalidFormatException


def main():
    parser = argparse.ArgumentParser(description='Render JSON graphics.')
    parser.add_argument('file')
    parser.add_argument('-o', '--output', required=False, metavar='file',
                        type=str, help='specify output file')
    parsed = parser.parse_args(sys.argv[1:])
    
    input_file = parsed.file
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

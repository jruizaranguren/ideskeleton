"""Build IDE required files from python folder structure

This utility creates the required files needed to manage a python
 package or module for a particular IDE from folder structure.

Note:
    Currently only Visual Studio 2015 and python projects are supported

"""
import argparse
from ideskeleton.builder import build

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source_path",
                        help="root path of the folder structure used to generate the IDE skeleton",
                        type=str)
    parser.add_argument("-f",
                        "--force",
                        help="force overwrite existing solution and project files",
                        action="store_true")
    parser.add_argument("-i",
                        "--ide",
                        help="choose IDE",
                        type=str,
                        choices=["vstudio"])

    args = parser.parse_args()

    if not args.ide:
        args.ide = "vstudio"

    build(args.source_path, args.force, args.ide)

main()



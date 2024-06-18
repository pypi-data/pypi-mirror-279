import argparse
from .converter import to_num, to_jac

def main():
    parser = argparse.ArgumentParser(description="Convert symbolic functions to Numba functions and Jacobians")
    parser.add_argument("mode", choices=["num", "jac"], help="Mode to run: 'num' for numerical functions, 'jac' for Jacobian functions")
    parser.add_argument("--folder_name", type=str, default="sym_files", help="Folder name for files to be converted")
    parser.add_argument("--output_folder", type=str, default="output_files", help="Folder name to save the results")
    
    args = parser.parse_args()
    
    if args.mode == "num":
        to_num(args.folder_name, args.output_folder)
    elif args.mode == "jac":
        to_jac(args.folder_name, args.output_folder)

if __name__ == "__main__":
    main()

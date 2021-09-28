import argparse

from create_antisemitic_subset import SubsetCreator
from fill_subset import Filler


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The main labeling tool. Decide for the filler, which only inserts non antisemitic comments or the normal creator which inserts depending on your decision.\n'
                                                 'The filler shows only comments without keywords, and the normal creator only those witch appearing keywords.')

    parser.add_argument('--filler', dest='feature', action='store_false',help="Select this argument if you want to use the filler functionality.")
    parser.add_argument('--normal_creator', dest='feature', action='store_true',help="Select this argument if you want to use the normal creator functionality.")
    parser.set_defaults(feature="")

    args = parser.parse_args()

    if isinstance(args.feature, str):
        print("Type -h for help. You have to chose an option\nExiting...")
        print("#"*50)
        quit()

    if args.feature:
        creator = SubsetCreator()
        creator.create_subset()
    else:
        filler = Filler()
        filler.fill()


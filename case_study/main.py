import argparse
from classify_comments import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify the comments and get some metrics.\n'
                                                 'This tool is based on the previous use of the youtube_api.py file\n'
                                                 'and therefore the download and creation of the data.')

    parser.add_argument('--plotting', dest='plot', action='store_false',help="Select this argument if you want to use the plotting functionality.")
    parser.set_defaults(feature="")

    args = parser.parse_args()

    if isinstance(args.plot, str):
        print("Type -h for help. You have to chose an option\nExiting...")
        print("#"*50)
        quit()

    if args.plot:
        main(True)
    else:
        main(False)
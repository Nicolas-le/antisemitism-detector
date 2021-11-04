import argparse
from classify_comments import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Classify the comments and get some metrics.\n'
                                                 'This tool is based on the previous use of the youtube_api.py file\n'
                                                 'and therefore the download and creation of the data.')

    parser.add_argument("--plotting",dest="plot",action="store_true", help="Select this argument if you want to use the plotting functionality.")
    parser.set_defaults(plot=False)
    args, _ = parser.parse_known_args()

    if args.plot is True:
        print("Plotting activated...",flush=True)
        main(True)
    else:
        print("Plotting deactivated...",flush=True)
        main(False)

import sys

from printannotate.traced_annotate import main


def entrypoint():
    if len(sys.argv) < 2:
        print("Please provide a script path as an argument")
    else:
        script_path = sys.argv[1]
        main(script_path)


if __name__ == "__main__":
    entrypoint()
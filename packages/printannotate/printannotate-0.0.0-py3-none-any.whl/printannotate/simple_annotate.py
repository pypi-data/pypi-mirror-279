import subprocess
import sys

def run_and_annotate(script_path):
    # Run the script and capture the output
    result = subprocess.run(['python', script_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running script: {result.stderr}")
        return

    # Split the output into lines
    output_lines = result.stdout.splitlines()

    # Read the original script
    with open(script_path, 'r') as file:
        script_lines = file.readlines()

    # Create a mapping of print statement outputs to script lines
    annotated_lines = []
    output_index = 0

    for line in script_lines:
        stripped_line = line.strip()
        if stripped_line.startswith('print(') and output_index < len(output_lines):
            output = output_lines[output_index]
            annotated_lines.append(f"{line.rstrip()}  # {output}\n")
            output_index += 1
        else:
            annotated_lines.append(line)

    # Write the annotated script to a new file
    annotated_script_path = script_path.replace('.py', '_annotated.py')
    with open(annotated_script_path, 'w') as file:
        file.writelines(annotated_lines)

    print(f"Annotated script saved to {annotated_script_path}")


if __name__ == '__main__':
    # get path from CLI argument
    if len(sys.argv) < 2:
        print("Please provide a script path as an argument")
    else:
        script_path = sys.argv[1]
        run_and_annotate(script_path)

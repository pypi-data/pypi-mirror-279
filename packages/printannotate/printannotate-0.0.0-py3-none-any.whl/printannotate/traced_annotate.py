import inspect
import io
import os
import sys

# Capture original print function
original_print = print
output_dict = {}

def get_module_name(file_path):
    return os.path.basename(file_path)

def encode_to_hex(text):
    return text.encode('utf-8').hex()

def decode_from_hex(hex_value):
    return bytes.fromhex(hex_value).decode('utf-8')

def get_stack_text(caller_frame: inspect.FrameInfo, file_name: str):
    line_number = caller_frame.lineno
    function_name = caller_frame.function
    return f"{file_name}:{line_number}:{function_name}"

def run_script(script_path):
    with open(script_path) as script:
        exec(script.read(), globals())

# Custom print function to encode the stack trace
def encoded_print(
    *values: object,
    sep=" ",
    end="\n",
    file=None,
    flush=False
) -> None:
    global global_script_path, output_dict
    caller_frame = inspect.stack()[1]
    stack_text = get_stack_text(caller_frame, get_module_name(global_script_path))
    hex = encode_to_hex(stack_text)
    original_print(f"[{hex}]", *values, sep=sep, end=end, file=file, flush=flush)

# Custom StdoutCapture class
class StdoutCapture(io.StringIO):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._value = self.getvalue()
        sys.stdout = self._stdout

    def get_output_dict(self):
        output = self._value.splitlines()
        output_dict = {}
        for line in output:
            if line.startswith('['):
                hex, value = line.split('] ', 1)
                output_dict[hex[1:]] = value
        return output_dict

def annotate(script_path):
    global print, global_script_path

    global_script_path = script_path

    print = encoded_print
    with StdoutCapture() as output_lines:
        run_script(global_script_path)

    output = output_lines.get_output_dict()

    print = original_print

    with open(global_script_path) as script:
        script_lines = script.readlines()
        for key, value in output.items():
            _, line, _ = decode_from_hex(key).split(':')
            script_lines[int(line) - 1] = script_lines[int(line) - 1].rstrip() + f" # {value}\n"

    return "".join(script_lines)

def main(script_path):
    annotated_script = annotate(script_path)
    print(annotated_script)

    file_name = os.path.basename(script_path).replace('.py', '_annotated.py')

    annotated_script_path = os.path.join(os.getcwd(), file_name)
    with open(annotated_script_path, 'w') as file:
        file.writelines(annotated_script)

    print(f"Annotated script saved to {annotated_script_path}")

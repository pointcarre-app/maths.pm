import asyncio
import argparse
from datetime import datetime
import glob
import os
from pprint import pprint
import sys

sys.path.append(".")

from src.services.backend_executor import backend_executor
from src.services.close_watch import close_watch



async def main():

    # Parse restriction on files
    parser = argparse.ArgumentParser(description='Test subject files')
    parser.add_argument('sujet_number', nargs='?', default='', help='Subject number (1 or 3)')
    parser.add_argument('question_number', nargs='?', default='', help='Filter by question number')
    args = parser.parse_args()

    # Parameters
    root_dir = "src/services/sujets0/"
    suffix = "question"

    # Build glob pattern
    pattern = f"_{args.question_number}_" if args.question_number else ""
    file_pattern = f"spe_sujet{args.sujet_number}*{pattern}*{suffix}.py"

    # Loop
    for filename in glob.glob(file_pattern, root_dir=root_dir):
        if not os.path.isfile(root_dir+ "/" + filename):
            continue
        print("\n" * 3 + f"Running: {filename}" + "\n"*3)

        filename = filename.split("/")[-1]
        script_path = backend_executor.get_script_path(filename)

        # Read and add doctest execution
        code = script_path.read_text(encoding="utf-8")
        code += "\nimport doctest"
        code += "\ndoctest_result = doctest.testmod()"
        code += "\nassert doctest_result[0] == 0"

        result =  await backend_executor.execute_script_code(filename, code)
        result["timestamp"] = datetime.now().isoformat()

        pprint(result)

        assert result["exit_code"] == 0

if __name__ == "__main__":
    asyncio.run(main())
    # main()
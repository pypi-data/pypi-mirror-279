"""Create the usage information string for the CLI."""

import os
from pathlib import Path

from soil_moisture_prediction.pydantic_models import InputParameters

information = """This is a command line interface for the soil moisture prediction module.

The module takes the path to a directory containing a JSON file with input parameters, and all the necessary data files.

This is an example of this directory structure:

soil_moisture_prediction/test_data/
{directory_tree}

The parameters.json file in this example directory contains the following content:

$ cat soil_moisture_prediction/test_data/parameters.json
{parameter_content}

The predictor data looks like this:
$ head -n {head_n} soil_moisture_prediction/test_data/predictor_data.csv
{predictor_data}

The soil moisture data looks like this:
$ head -n {head_n} soil_moisture_prediction/test_data/soil_moisture_data.csv
{soil_moisture_data}

This is a description of the input parameters model:
{pydantic_model_information}"""  # noqa

# Used for tree representation of directory structure:
space = "    "
branch = "│   "
tee = "├── "
last = "└── "

current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_dir, "test_data")

head_n = 5


def tree(dir_path: Path, prefix: str = ""):
    """Like gnu tree.

    Found at https://stackoverflow.com/questions/9727673
    """
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix + extension)


def compile_information():
    """Compile the information string."""
    directory_tree = "\n".join(list(tree(Path(test_data_dir))))

    with open(os.path.join(test_data_dir, "parameters.json"), "r") as f_handle:
        parameter_content = f_handle.read()

    predictor_data = ""
    with open(os.path.join(test_data_dir, "pred_sand.csv"), "r") as f_handle:
        for _ in range(head_n):
            predictor_data += f_handle.readline()

    soil_moisture_data = ""
    with open(os.path.join(test_data_dir, "crn_soil-moisture.csv"), "r") as f_handle:
        for _ in range(head_n):
            soil_moisture_data += f_handle.readline()

    pydantic_model_information = ""
    for field_name, field in InputParameters.model_fields.items():
        pydantic_model_information += f"{field_name}:\n  {field.description}\n\n"
    pydantic_model_information = pydantic_model_information[:-2]

    return information.format(
        directory_tree=directory_tree,
        parameter_content=parameter_content,
        head_n=head_n,
        predictor_data=predictor_data,
        soil_moisture_data=soil_moisture_data,
        pydantic_model_information=pydantic_model_information,
    )

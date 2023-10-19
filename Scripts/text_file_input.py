# import pandas as pd
# import re
#
#
# def split_steps_description(data):
#     # Find the index of the "Steps Description" heading
#     steps_index = data.index("Steps Description:") + 1
#
#     # Get the content under the "Steps Description" heading
#     steps_description = data[steps_index].strip()
#     print('steps_description:',steps_description)
#
#     # Split the content based on commas, "and," or full stops
#     steps = re.split(r',|\sand\s|\.', steps_description)
#
#     # Clean up the steps (remove leading/trailing spaces)
#     steps = [step.strip() for step in steps if step.strip()]
#
#     return steps
#
# def split_steps_description1(data):
#     # Find the index of the "Steps Description" heading
#     steps_index = data.index("Test case / Scenario:")+1
#     test_case_col = data[steps_index].strip()
#     print(test_case_col)
#     # steps_index = re.search(r'\d+', steps_index).group()
#     # print('steps_index',steps_index)
#     # return steps_index
#     return test_case_col
#
#
# def text_input(file):
#     # Read the text data from a file
#     filename = "testing.txt"  # Replace with your actual file name
#     with open(filename, "r") as file:
#         data = file.read().splitlines()
#
#     steps = split_steps_description(data)
#     test_case = split_steps_description1(data)
#
#     # Convert steps to DataFrame
#     df = pd.DataFrame({'Test case / Scenario:':test_case,'Steps':steps})
#
#     return df
#
#
#
# df = text_input('testing.txt')
#
# print(df)





import pandas as pd
import re


def split_steps_description(data):
    # Find the index of the "Steps Description" heading
    steps_index = data.index("Steps Description:") + 1

    # Get the content under the "Steps Description" heading
    steps_description = data[steps_index].strip()

    # Split the content based on commas, "and," or full stops
    steps = re.split(r',|\sand\s|\.', steps_description)

    # Clean up the steps (remove leading/trailing spaces)
    steps = [step.strip() for step in steps if step.strip()]

    return steps


def split_steps_description1(data):
    # Find the index of the "Test case / Scenario" heading
    steps_index = data.index("Test case / Scenario:") + 1
    test_case_col = data[steps_index].strip()

    return test_case_col


def text_input(file):
    # Read the text data from a file
    with open(file, "r") as f:
        data = f.read().splitlines()

    scenarios = []
    current_scenario = {}

    for line in data:
        line = line.strip()

        if line.startswith("Test case / Scenario:"):
            if current_scenario:
                scenarios.append(current_scenario)
                current_scenario = {}

            current_scenario['Test case / Scenario:'] = line.replace("Test case / Scenario:", "").strip()
        elif line.startswith("Steps Description:"):
            steps = split_steps_description(data)

            # Add each split step as a separate row in the DataFrame
            for step in steps:
                current_scenario = {
                    'Test case / Scenario:': current_scenario['Test case / Scenario:'],
                    'Steps': step
                }
                scenarios.append(current_scenario)

        elif line.startswith("Test case / Scenario:"):
            current_scenario['Test case / Scenario:'] = line.replace("Test case / Scenario:", "").strip()

    if current_scenario:
        scenarios.append(current_scenario)

    # Convert scenarios to DataFrame
    df = pd.DataFrame(scenarios)
    df['Test case / Scenario:'] = '2'

    return df

df = text_input(r"C:\Users\abdul\PycharmProjects\Automation_Optimum\All Files\testing.txt")

print(df)




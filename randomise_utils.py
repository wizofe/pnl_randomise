from pathlib import Path
from tabulate import tabulate
from itertools import product
import inquirer


def print_head(heading):
    print()
    print('-'*80)
    print(f'* {heading}')
    print('-'*80)


def print_df(df):
    """Print pandas dataframe using tabulate.

    Used to print outputs when the script is called from the shell
    Key arguments:
        df: pandas dataframe
    """
    print(tabulate(df, headers='keys', tablefmt='psql'))
    print()


def search_and_select_one(name: str, location: str,
                          list_of_patterns: list, depth=1):
    """Search files with given patterns around the location and choose.

    Key arguments:
        title: str, name of the file that is being searched for.
        location: str, location of search.
        patterns: list, regrex patterns.
        depth: int, search parent depth, eg)0, 1, 2
    """
    # list of directories and serach patterns
    location = Path(location)

    # if file location is given as the `location`, set it as the parent
    # directory.
    if location.is_file():
        location = location.parent

    # search directory settings
    if depth == 1:
        list_search_directories = [location, location.parent]
    elif depth == 2:
        list_search_directories = [location, location.parent.parent]
    else:
        list_search_directories = [location]

    # list_of_patters = [
        # f'*all*_{self.modality}[_.]*nii.gz',
        # f'*{self.modality}*merged*.nii.gz'
        # ]

    # get combinations of the two lists
    list_of_dir_pat = list(product(
        list_search_directories,
        list_of_patterns))

    # search files
    matching_files = []
    for s_dir, pat in list_of_dir_pat:
        mf = list(Path(s_dir).glob(pat))
        if len(mf) > 0:
            matching_files += mf
        else:
            pass
    matching_files = list(set(matching_files))

    # check matching_files list
    if len(matching_files) == 1:
        final_file = matching_files[0]
    # if there are more than one merged skeleton files detected
    elif len(matching_files) > 1:
        questions = [
            inquirer.List(
                name,
                message=f"Select correct {name}",
                choices=matching_files,
                )
            ]
        answer = inquirer.prompt(questions)
        final_file = answer[name]
    # if no merged skeleton is detected
    else:
        final_file = 'missing'

    return final_file

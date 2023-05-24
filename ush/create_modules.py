#!/usr/bin/env python3

"""
Read a CSV that contains a table where the rows are the modules and columns are the jobs.
Each entry in that table is whether the job uses the module or not.

The source of the CSV is the following Google Sheet:
https://docs.google.com/spreadsheets/d/1ZJRwKxk5ogay3pidZd18Pi2EUzeSKBM-xWxTUWvP2U0/edit#gid=0
"""

import os
import sys
import pandas as pd
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pprint import pprint

from pygw.yaml_file import save_as_yaml
from pygw.attrdict import AttrDict


def read_csv_into_dataframe(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename, index_col=0, header=0)


def get_modules_and_jobs(df: pd.DataFrame) -> tuple:
    modules = df.columns.tolist()
    jobs = df.index.tolist()
    return (modules, jobs)


def get_list_of_columns_given_row(df: pd.DataFrame, row_name: str) -> list:
    row = df.loc[row_name]
    column = list(row[row.notna()].index)
    return column


def create_modules(yaml_file: str, target: str):
    print(f"Creating modules for {target}")
    yaml = YAMLFile(yaml_file)
    pprint(yaml.jobs.gdasarch)


if __name__ == "__main__":

    description = """
        Create modulefiles for jobs in the global-workflow
        """

    parser = ArgumentParser(description=description,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--csv', help='full path to CSV file containing modules used by jobs on the machine',
                        type=str, default='modules.csv')
    parser.add_argument('--yaml', help='full path to YAML containing modules used by jobs on the machine',
                        type=str, default='modules.yaml')
    parser.add_argument('--machine', help='machine name', type=str,
                        default='wcoss2', choices=['wcoss2', 'hera', 'orion', 'jet'])

    args = parser.parse_args()


    #create_modules(args.yaml, args.machine)

    df = read_csv_into_dataframe(args.csv)
    modules, jobs = get_modules_and_jobs(df)

    print('All jobs:')
    print(', '.join(jobs))
    print()

    print('All modules:')
    print(', '.join(modules))
    print()

    for module in modules:
        job_names = get_list_of_columns_given_row(df.transpose(), module)
        print(f"{module} is used in {len(job_names)}/{len(jobs)} jobs:\n{', '.join(job_names)}")
        print()

    job_dict = AttrDict()

    for job in jobs:
        module_names = get_list_of_columns_given_row(df, job)
        modules = []
        print(f"{job}:")
        for mm in module_names:
            mm_str = "%s/${%s_ver}" % (mm, mm.replace('-', '_'))
            modules.append(mm_str)
        job_dict[job] = modules

    save_as_yaml(job_dict, args.yaml)
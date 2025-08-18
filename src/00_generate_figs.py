import json
import os
from typing import Dict

import pandas as pd

from landing_map import LandingMap
from landing_table import LandingTable
from simple_landing_map import SimpleLandingMap
from simple_landing_table import SimpleLandingTable
from plot_generator import PlotGenerator

RECENT_YEAR = 2023


def get_schools() -> Dict[str,str]:
    # get HEMAC partner schools
    SHEET_ID = '1pbANvK-nxuUVHaD6w2f-01wzDgYwXAYxapSGXsH1VAs'
    SHEET_NAME = 'hemac'
    sheet = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(sheet, dtype=str)
    schools = {
        r['hemac_id']: r['partner_name'] for idx, r in df.iterrows()
    }
    with open(os.path.join('data','hemac_schools.json'),'w') as hmjs:
        json.dump(schools,hmjs,indent=4)
    return schools


def make_map(schls: Dict[str,str]) -> None:
    # make landing page map
    lm = LandingMap(schls,RECENT_YEAR)
    lm.build_data_dicts()
    lm.build_labels()
    lm.build_map()


def make_table(schls: Dict[str,str]) -> None:
    # make landing page table
    lt = LandingTable(schls,RECENT_YEAR)
    lt.build_table()


def make_simple_map(schls: Dict[str,str]) -> None:
    # make simple landing page map
    lm = SimpleLandingMap(schls,RECENT_YEAR)
    lm.build_map()


def make_simple_table(schls: Dict[str,str]) -> None:
    # make simple landing page table
    lt = SimpleLandingTable(schls,RECENT_YEAR)
    lt.build_table()


def make_plots(schls: Dict[str,str]) -> None:
    # make school-specific plots
    pg = PlotGenerator(schls,RECENT_YEAR)
    pg.gen_all_plots()
    

def main(pull_anyway: bool = False,
         simple_only: bool = True):
    # generate landing page map, landing table, and school specific plots
    schools_path = os.path.join('data','hemac_schools.json')

    if os.path.exists(schools_path):
        with open(schools_path,'r') as schlj:
            schools_last_pulled = json.load(schlj)
        new_schools = get_schools()
        if new_schools.keys() == schools_last_pulled.keys() and not pull_anyway:
            return None     # no changes since last pulled, do nothing
        else:
            if simple_only:
                make_simple_map(new_schools)
                make_simple_table(new_schools)
            else:
                make_map(new_schools)
                make_table(new_schools)
                make_plots(new_schools)

    else:
        new_schools = get_schools()
        with open(schools_path,'r') as schlj:
            schls = json.load(schlj)
        if simple_only:
            make_simple_map(new_schools)
            make_simple_table(new_schools)
        else:
            make_map(schls)
            make_table(schls)
            make_plots(schls)


if __name__ == '__main__':
    main(pull_anyway=True, simple_only=True)

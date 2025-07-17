import pandas as pd
import json

def main():
    sheet_id = '1pbANvK-nxuUVHaD6w2f-01wzDgYwXAYxapSGXsH1VAs'
    sheet_name = 'Sheet1'
    sheet = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(sheet)
    schools = df['hemac_ids'].astype(str).str.replace(',','').to_list()
    schools_js = {
        'year': '2023',
        'ids': schools
    }
    with open('hemac_schools.json','w') as hmjs:
        json.dump(schools_js,hmjs,indent=4)

if __name__=='__main__':
    main()

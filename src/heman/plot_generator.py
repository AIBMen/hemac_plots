import plotly.graph_objects as go
import plotly.io as pio
import json
import os
from genpeds import Admissions, Enrollment, Completion, Graduation, Characteristics


from plot_struct import THEME

pio.templates['THEME'] = THEME
pio.templates.default='THEME'

'''
- admit rate by gender
- enrollment numbers by gender
- graduation rates by gender
'''

class PlotGenerator:
    '''generate school-level HEMAC plots'''
    def __init__(self,
                 schools: list,
                 most_recent_year: int = 2023):
        '''HEMAC school plot generator
        
        :param schools: list of HEMAC schools 
        :param most_recent_year: most recent year of data; defaults to 2023
        '''
        short_range = [i for i in range(2003,most_recent_year+1,2)]
        long_range = [i for i in range(1993,most_recent_year+1,2)]

        admit = Admissions(short_range).run(False,True,False)
        
        enroll_undergrad = Enrollment(long_range).run('undergrad',False,True,False)
        enroll_grad = Enrollment(long_range).run('grad',False,True,False)

        grad_two_year = Graduation(short_range).run('assc',False,True,False)
        grad_four_year = Graduation(short_range).run('bach',False,True,False)

        # complete_assc = Completion(most_recent_year).run('assc',False,True,True,False)
        # complete_bach = Completion(most_recent_year).run('bach',False,True,True,False)
        # complete_mast = Completion(most_recent_year).run('mast',False,True,True,False)
        # complete_doct = Completion(most_recent_year).run('doct',False,True,True,False)

        data = {
            'admissions': admit,
            'enrollment_undergrad': enroll_undergrad,
            'enrollment_grad': enroll_grad,
            'graduation_two_year': grad_two_year,
            'graduation_four_year': grad_four_year,
            # 'completion_assc': complete_assc,
            # 'completion_bach': complete_bach,
            # 'completion_mast': complete_mast,
            # 'completion_doct': complete_doct,
        }
        for label,df in data.items():
            data[label] = df.loc[df['id'].isin(schools)]
        
        self.data = data
        self.schools = schools
    
    def gen_admissions(self,
                       school_id: str,
                       out_path_dir: str)->go.Figure:
        '''generates Plotly figure of admissions rates over time'''
        df = self.data['admissions']
        df = df.loc[df['id']==school_id].copy()
        df['women_applied'] = df['tot_applied'] - df['men_applied']
        df['women_admitted'] = df['tot_admitted'] - df['men_admitted']
        df['women_enrolled'] = df['tot_enrolled'] - df['men_enrolled']

        fig = go.Figure(layout=go.Layout(
            title={'text': f'Acceptance Rates over time at {df['name'].unique()[0]}'},
            xaxis={'range': (df['year'].min() - 1, df['year'].max() + 1)},
            yaxis={'range': (0,100)},
            hoverlabel={'bgcolor': '#ffffff',
                        'align': 'left',
                        'bordercolor': 'black',
                        'font': {'color': '#1e4a4a'}}
        ))
        for g in ['men','women']:
            if len(df['men_enrolled']) > 0:
                df[f'accept_rate_{g}_label'] = (
                    '<u><b>' + df['year'].astype(str) + f'</b></u> ({g.title()})<br>' +
                    '<b># Applied</b>: ' + df[f'{g}_applied'].astype(int).astype(str) + '<br>'
                    '<b># Admitted</b>: ' + df[f'{g}_admitted'].astype(int).astype(str) + '<br>'
                    '<b># Enrolled</b>: ' + df[f'{g}_enrolled'].astype(int).astype(str) + '<br>' +
                    '<b>% Acceptance Rate</b>: ' + df[f'accept_rate_{g}'].astype(int).astype(str) + '%<br>' +
                    '<b>% Yield Rate</b>: ' + df[f'yield_rate_{g}'].astype(int).astype(str) + '%' 
                )
                fig.add_trace(go.Scatter(
                    name=f'<b>{g.title()}</b>',
                    x=df['year'],
                    y=df[f'accept_rate_{g}'],
                    mode='lines+markers',
                    text=df[f'accept_rate_{g}_label'],
                    hovertemplate='%{text}<extra></extra>',
                    marker={
                        'size': 15,
                        'color': '#0B8569' if g == 'men' else '#9657A5'
                            },
                    line={
                        'width': 6
                    }))
        outpath_name = os.path.join(out_path_dir,'admissions.html')
        fig.write_html(file=outpath_name,auto_play=False,include_plotlyjs='cdn')
    
    def gen_enrollment(self,
                       level: str,
                       school_id: str,
                       out_path_dir: str)->go.Figure:
        '''generates Plotly figure of enrollment over time
        
        :param level: 'undergrad' or 'grad'
        '''
        
        df = self.data[f'enrollment_{level}']
        df = df.loc[df['id']==school_id].copy()

        fig = go.Figure(layout=go.Layout(
            title={'text': f'{(level + 'uate').title()} Enrollment rates over time at {df['name'].unique()[0]}'},
            xaxis={'range': (df['year'].min() - 1, df['year'].max() + 1)},
            # yaxis={'range': (0,100)},
            hoverlabel={'bgcolor': '#ffffff',
                        'align': 'left',
                        'bordercolor': 'black',
                        'font': {'color': '#1e4a4a'}}
        ))
        for g in ['men','women']:
            if len(df[f'tot{g}']) > 0:
                df[f'tot{g}_label'] = (
                    '<u><b>' + df['year'].astype(str) + f'</b></u> ({g.title()})<br>' +
                    f'<b># Total {g.title()} Enrolled</b>: ' + df[f'tot{g}'].astype(int).astype(str) + '<br>'
                    '<b>% Male Enrollment Share</b>: ' + df[f'totmen_share'].astype(int).astype(str) + '%' 
                )
                fig.add_trace(go.Scatter(
                    name=f'<b>{g.title()}</b>',
                    x=df['year'],
                    y=df[f'tot{g}'],
                    mode='lines+markers',
                    text=df[f'tot{g}_label'],
                    hovertemplate='%{text}<extra></extra>',
                    marker={
                        'size': 15,
                        'color': '#0B8569' if g == 'men' else '#9657A5'
                            },
                    line={
                        'width': 6
                    }))
        outpath_name = os.path.join(out_path_dir,f'enrollment_{level}.html')
        fig.write_html(file=outpath_name,auto_play=False,include_plotlyjs='cdn')

    def gen_enroll_demo(self,
                       level: str,
                       school_id: str,
                       out_path_dir: str)->go.Figure:
        '''generates Plotly figure of enrollment demographics over time
        
        :param level: 'undergrad' or 'grad'
        '''
        df = self.data[f'enrollment_{level}']
        df = df.loc[(df['id']==school_id) & (df['year'] != 2009)].copy()
        df['othermen'] = df['totmen'] - df['wtmen'] - df['bkmen'] - df['hspmen'] - df['asnmen']
        df['otherwomen'] = df['totwomen'] - df['wtwomen'] - df['bkwomen'] - df['hspwomen'] - df['asnwomen']

        demo_dict = {
            'wtmen': ('White Men','#0B8569'), 'wtwomen': ('White Women','#AAC9B8'),
            'bkmen': ('Black Men','#9657A5'), 'bkwomen': ('Black Women','#CFBCD0'),
            'hspmen': ('Hispanic Men','#4575D6'), 'hspwomen': ('Hispanic Women','#C9D3E8'),
            'asnmen': ('Asian Men','#C55300'), 'asnwomen': ('Asian Women','#F4A26B'),
            'othermen': ('Other Men','#d7c015'), 'otherwomen': ('Other Women','#f4ebad')
        }

        fig = go.Figure(layout=go.Layout(
                        title={'text': f'Enrollment demographics over time at {df['name'].unique()[0]}'},
                        xaxis={'range': (df['year'].min() - 1, df['year'].max() + 1)},
                        yaxis={'range': (0,100)},
                        hoverlabel={'bgcolor': '#ffffff',
                                    'align': 'left',
                                    'bordercolor': 'black',
                                    'font': {'color': '#1e4a4a'}},
                        hovermode='x unified'
                    ))

        for demo,lab in demo_dict.items():
            df[f'{lab[0]}_label'] = (
                f'# <b>{lab[0]}</b>: ' + df[demo].astype(int).astype(str)
            )

            fig.add_trace(
                go.Scatter(
                    name=f'<b>{lab[0]}</b>',
                    line_color=lab[1],
                    groupnorm='percent',
                    text=df[f'{lab[0]}_label'],
                    hovertemplate='%{text}<extra></extra>',
                    x=df['year'],
                    y=df[demo],
                    stackgroup='one'
                )
            )
        outpath_name = os.path.join(out_path_dir,f'enrollment_demographics_{level}.html')
        fig.write_html(file=outpath_name,auto_play=False,include_plotlyjs='cdn')
    
    def gen_graduation(self,
                       level: str,
                       school_id: str,
                       out_path_dir: str)->go.Figure:
        '''generates Plotly figure of graduation over time
        
        :param level: 'two_year' or 'four_year'
        '''
        
        df = self.data[f'graduation_{level}']
        df = df.loc[df['id']==school_id].copy()

        fig = go.Figure(layout=go.Layout(
            title={'text': f'{(level + '+Graduate').title()} rates over time at {df['name'].unique()[0]}'},
            xaxis={'range': (df['year'].min() - 1, df['year'].max() + 1)},
            yaxis={'range': (0,100)},
            hoverlabel={'bgcolor': '#ffffff',
                        'align': 'left',
                        'bordercolor': 'black',
                        'font': {'color': '#1e4a4a'}}
        ))
        for g in ['men','women']:
            if len(df[f'tot{g}']) > 0:
                df[f'tot{g}_label'] = (
                    '<u><b>' + df['year'].astype(str) + f'</b></u> ({g.title()})<br>' +
                    f'<b># Total {g.title()} in cohort</b>: ' + df[f'tot{g}'].astype(int).astype(str) + '<br>'
                    f'<b># Total {g.title()} graduated</b>: ' + df[f'tot{g}_graduated'].astype(int).astype(str) + '<br>'
                    f'<b>% {g.title()} grad. rate</b>: ' + df[f'gradrate_tot{g}'].astype(int).astype(str) + '%' 
                )
                fig.add_trace(go.Scatter(
                    name=f'<b>{g.title()}</b>',
                    x=df['year'],
                    y=df[f'gradrate_tot{g}'],
                    mode='lines+markers',
                    text=df[f'tot{g}_label'],
                    hovertemplate='%{text}<extra></extra>',
                    marker={
                        'size': 15,
                        'color': '#0B8569' if g == 'men' else '#9657A5'
                            },
                    line={
                        'width': 6
                    }))
        outpath_name = os.path.join(out_path_dir,f'graduation_{level}.html')
        fig.write_html(file=outpath_name,auto_play=False,include_plotlyjs='cdn')

    def gen_all_plots(self):
        '''generates all applicable plots for each school'''
        func_map = {
            'admissions': {
                'func': self.gen_admissions,
                'spec': None
            },
            'enrollment_undergrad': {
                'func': (self.gen_enrollment,self.gen_enroll_demo),
                'spec': 'undergrad'
            },
            'enrollment_grad': {
                'func': (self.gen_enrollment,self.gen_enroll_demo),
                'spec': 'grad'
            },
            'graduation_two_year': {
                'func': self.gen_graduation,
                'spec': 'two_year'
            },
            'graduation_four_year': {
                'func': self.gen_graduation,
                'spec': 'four_year'
            },
        }
        
        df_len_checker = lambda df,id_: len(df.loc[df['id'] == id_]) > 0

        for schl in self.schools:
            fpath = os.path.join('docs',f'{schl}_plots')
            os.makedirs(fpath,exist_ok=True)
            for sbjct in func_map.keys():
                if df_len_checker(self.data[sbjct],schl):
                    spec = func_map[sbjct]['spec']
                    func = func_map[sbjct]['func']
                    if isinstance(func,tuple) and spec is not None:
                        [f(spec,schl,fpath) for f in func]
                    elif spec is not None:
                        func(spec,schl,fpath)
                    else:
                        func(schl,fpath)
            print(f'{schl} plots completed')
        


if __name__=='__main__':
    with open('data/hemac_schools.json','r') as schlj:
        s = json.load(schlj)
        schls = s['ids']
    pg = PlotGenerator(schls,2023)
    pg.gen_all_plots()
        
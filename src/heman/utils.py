import pandas as pd
import plotly.graph_objects as go
from genpeds import Admissions, Enrollment, Completion, Graduation

PLOTS_DICT = {
    'admissions': {
        'cls': Admissions,
        'cols_to_keep': ['year','id','name','city','state','latitude','longitude',
                         'tot_enrolled','men_enrolled', 'men_admitted',
                         'men_applied', 'men_applied_share', 'men_admitted_share',
                         'accept_rate_men','accept_rate_women',
                         'yield_rate_men','yield_rate_women',
                         'sat_rw_25','sat_rw_75','sat_math_25','sat_math_75',
                         'act_eng_25','act_eng_75','act_math_25','act_math_75',
                         'act_comp_25','act_comp_75']
    },

    'enrollment': {
        'cls': Enrollment,
        'cols_to_keep': ['year','id','name','city','state','studentlevel','latitude','longitude',
                         'totmen','totwomen','totmen_share',
                         'wtmen','wtwomen','bkmen','bkwomen',
                         'asnmen','asnwomen','hspmen','hspwomen']
    },

    'completion': {
        'cls': Completion,
        'cols_to_keep': ['year','id','name','city','state','deglevel','latitude','longitude',
                         'cip','cip_description',
                         'totmen','totwomen','totmen_share',
                         'wtmen','wtwomen','bkmen','bkwomen',
                         'asnmen','asnwomen','hspmen','hspwomen']
    },

    'graduation': {
        'cls': Graduation,
        'cols_to_keep': ['year','id','name','city','state','deglevel','latitude','longitude',
                         'totmen','totwomen', 'totmen_graduated', 'totwomen_graduated',
                         'wtmen','wtwomen','bkmen','bkwomen',
                         'asnmen','asnwomen','hspmen','hspwomen',
                         'gradrate_totmen','gradrate_totwomen',
                         'gradrate_wtmen','gradrate_wtwomen',
                         'gradrate_bkmen','gradrate_bkwomen',
                         'gradrate_asnmen','gradrate_asnwomen',
                         'gradrate_hspmen','gradrate_hspwomen']
    }
}

'''
HEMAC SCHOOLS LIST
'''



'''
CleanForPlot
'''
class CleanForPlotHEMAC:
    '''Data cleaning for plots.'''
    def __init__(self,subject,years):
        '''Data cleaning for plots.
        
        :param subject::
         (*str*) plot subject. options include:<br>['admissions','enrollment','completion','graduation']
        
        :param years::
         (*tuple* or *int*) year range or single year. ranges available vary by subject.
        '''
        self.subject = subject
        self.years = years
        
        self.plot_dict = PLOTS_DICT[self.subject]
        self.cls = self.plot_dict['cls']
        self.c2k = self.plot_dict['cols_to_keep']
        self.viz = go.Figure()
    
    def _run_data(self,**kwargs) -> pd.DataFrame:
        '''runs data and returns dataframe for a subject.
        
        **kwargs are passed onto the  'run' method for each class. 
        '''
        df = self.cls(self.years).run(**kwargs) # get dat

        # filter to schools present in most recent year
        if isinstance(self.years,tuple):
            start,end = self.years
        elif isinstance(self.years,list):
            start,end = sorted(self.years)[0],sorted(self.years)[-1]
        elif isinstance(self.years,int):
            end = self.years
        else:
            raise TypeError('years param should be int or tuple.')
        ids_to_include = df.loc[df['year'] == end, 'id'].unique()
        df = df.loc[df['id'].isin(ids_to_include)] # filter cols

        # return data, with cols to keep
        # some cols may not be in specified dataset though, ie. lon
        cols2keep = [col for col in self.c2k if col in df.columns]
        return df.loc[:, cols2keep]    

    def data_viz(self,render='browser'):
        '''plots current figure.
        
        :param render: form of rendering. Options include:<br>
         ['plotly_mimetype', 'jupyterlab', 'nteract', 'vscode',
         'notebook', 'notebook_connected', 'kaggle', 'azure', 'colab',
         'cocalc', 'databricks', 'json', 'png', 'jpeg', 'jpg', 'svg',
         'pdf', 'browser', 'firefox', 'chrome', 'chromium', 'iframe',
         'iframe_connected', 'sphinx_gallery', 'sphinx_gallery_png']
        '''
        self.viz.show(renderer=render) # shows the plot


LMLABEL_HEAD = (
    '<html><div style="color:#06474D;">' +
    '<div style="font-size:18px;font-family:Georgia, serif;"><b>{name}</b></div>' +
    '<div style="font-size:13px;"><i>{city}, {state}</i></div>' +
    '<div style="font-size:13px;"><a target="_blank" rel="noopener noreferrer" href="{webaddr}">{webaddr}</a></div>'
    '<br>'
)

LMLABEL_ADMISSIONS = (
    '<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Admissions</u></b>:</div>' +
    '<div style="font-size:13px;"><b># Applied</b>: Men - {male_applied} | Women - {female_applied}</div>' +
    '<div style="font-size:13px;"><b># Admitted</b>: Men - {male_admitted} | Women - {female_admitted}</div>' +
    '<div style="font-size:13px;"><b># Enrolled</b>: Men - {male_enrolled} | Women - {female_enrolled}</div>' +
    '<div style="font-size:13px;"><b>% Admitted</b>: Men - {male_accept}% | Women - {female_accept}%</div>' +
    '<div style="font-size:13px;"><b>% Yield</b>: Men - {male_yield}% | Women - {female_yield}%</div>'
)

LMLABEL_ADMISSIONS = '''
<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Admissions</u></b>:</div> 
<div style="color:black;font-size:12px;font-family:Helvetica, Arial, sans-serif;">
<span>{name} recieved  <b>{male_applied} applications from men</b> and <b>{female_applied} applications from women</b>. 
Of these applications, <b>{male_admitted} men</b> and <b>{female_admitted} women were admitted</b>, and 
<b>{male_enrolled} men</b> and <b>{female_enrolled} women ultimately enrolled</b>. Overall, <b>{male_accept}% of men</b> 
were admitted and <b>{male_yield}%</b> ultimately enrolled, compared to <b>{female_accept}% of female</b> applicants being accepted 
and <b>{female_yield}%</b> ultimately enrolling.
</div><br>'''

LMLABEL_ENROLL_UNDERGRAD = '''
<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Enrollment (Undergraduate)</u></b>:</div> 
<div style="color:black;font-size:12px;font-family:Helvetica, Arial, sans-serif;">
<span>At the undergraduate level, a total of <b>{totmen_enroll} men</b> and <b>{totwomen_enroll} women</b> were enrolled, 
meaning a <b>male enrollment share</b> of <b>{totmen_share}%</b>.</span>
</div><br>'''

LMLABEL_ENROLL_GRAD = '''
<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Enrollment (Graduate)</u></b>:</div> 
<div style="color:black;font-size:12px;font-family:Helvetica, Arial, sans-serif;">
<span>At the graduate level, a total of <b>{totmen_enroll} men</b> and <b>{totwomen_enroll} women</b> were enrolled, 
meaning a <b>male enrollment share</b> of <b>{totmen_share}%</b>.</span>
</div><br>'''

LMLABEL_GRADUATION_ASSC = '''
<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Three-Year Graduation (Associate's)</u></b>:</div> 
<div style="color:black;font-size:12px;font-family:Helvetica, Arial, sans-serif;">
<span>Tracking a cohort of <b>{totmen} men</b> and <b>{totwomen} women</b>, three years later,
<b>{totmen_graduated} men</b> and <b>{totwomen_graduated} women graduated</b>, meaning a 
<b>male graduation rate</b> of <b>{gradrate_men}%</b>  and <b>female graduation rate</b> of <b>{gradrate_women}%</b>.</span>
</div><br>'''

LMLABEL_GRADUATION_BACH = '''
<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Six-Year Graduation (Bachelor's)</u></b>:</div> 
<div style="color:black;font-size:12px;font-family:Helvetica, Arial, sans-serif;">
<span>Tracking a cohort of <span style="color:#0B8569";><b>{totmen} men</b></span> and <span style="color:#9657A5";><b>{totwomen} women</b></span>, six years later,
<span style="color:#0B8569";><b>{totmen_graduated} men</b></span> and <span style="color:#9657A5";><b>{totwomen_graduated} women graduated</b></span>, meaning a 
<span style="color:#0B8569";><b>male graduation rate</b></span> of <span style="color:#0B8569";><b>{gradrate_men}%</b></span>  and <span style="color:#9657A5";><b>female graduation rate</b></span> of <span style="color:#9657A5";><b>{gradrate_women}%</b></span>.</span>
</div>'''

# LMLABEL_GRADUATION_BACH1 = (
#     '<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Six-Year Graduation (Bachelor)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Cohort</b>: Men - {totmen} | Women - {totwomen}</div>' +
#     '<div style="font-size:13px;"><b># Graduated within six years</b>: Men - {totmen_graduated} | Women - {totwomen_graduated}</div>'
#     '<div style="font-size:13px;"><b>% Graduation</b>: Men - {gradrate_men}% | Women - {gradrate_women}%</div>'
# )

# LMLABEL_GRADUATION_ASSC1 = (
#     '<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Three-Year Graduation (Associate)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Cohort</b>: Men - {totmen} | Women - {totwomen}</div>' +
#     '<div style="font-size:13px;"><b># Graduated within three years</b>: Men - {totmen_graduated} | Women - {totwomen_graduated}</div>'
#     '<div style="font-size:13px;"><b>% Graduation</b>: Men - {gradrate_men}% | Women - {gradrate_women}%</div>'
# )

# LMLABEL_ENROLL_UNDERGRAD1 = (
#     '<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Enrollment (Undergraduate)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Total Enrollment</b>: Men - {totmen_enroll}% | Women - {totwomen_enroll}%</div>' +    
#     '<div style="font-size:13px;"><b>% Male Enrollment Share</b>: {totmen_share}%</div>' 
# )

# LMLABEL_ENROLL_GRAD1 = (
#     '<div style="font-size:15px;font-family:Georgia, serif;"><b><u>Enrollment (Graduate)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Total Enrollment</b>: Men - {totmen_enroll}% | Women - {totwomen_enroll}%</div>' +    
#     '<div style="font-size:13px;"><b>% Male Enrollment Share</b>: {totmen_share}%</div>' 
# )
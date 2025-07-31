import plotly.graph_objects as go


THEME_LAYOUT = go.Layout(
    # FONT/TEXT
    font={
        'color': '#001A50',
        'family': 'Source Sans Pro'
    },
    title={
        'font': {
            'family': 'Merriweather',
            'size': 24,
            'weight': 'bold'
        },
        'x': .2
    },
    #MAPS
    geo={
        'scope': 'usa',
        'bgcolor': '#ffffff',
        'landcolor': '#ffffff',
        'subunitcolor': '#001A50'
    },
    #NON-GEO PLOTS
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    scattermode='overlay',
    #GENERAL
    showlegend=True

)

THEME = go.layout.Template(layout=THEME_LAYOUT)


LMLABEL_HEAD = (
    '<html><div style="color:#001A50;">' +
    '<div style="font-size:18px;font-family:Source Sans Pro;"><b>{name}</b></div>' +
    '<div style="font-size:13px;"><i>{city}, {state}</i></div>' +
    '<div style="font-size:13px;"><a target="_blank" rel="noopener noreferrer" href="{webaddr}">{webaddr}</a></div>'
    '<br>'
)

LMLABEL_ADMISSIONS = '''
<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Admissions</u></b>:</div> 
<div style="color:black;font-size:13px;font-family:Source Sans Pro;">
<span>{name} recieved  <b>{male_applied} applications from men</b> and <b>{female_applied} applications from women</b>. 
Of these applications, <b>{male_admitted} men</b> and <b>{female_admitted} women were admitted</b>, and 
<b>{male_enrolled} men</b> and <b>{female_enrolled} women ultimately enrolled</b>. Overall, <b>{male_accept}% of men</b> 
were admitted and <b>{male_yield}%</b> ultimately enrolled, compared to <b>{female_accept}% of female</b> applicants being accepted 
and <b>{female_yield}%</b> ultimately enrolling.
</div><br>'''


LMLABEL_ENROLL_UNDERGRAD = '''
<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Enrollment (Undergraduate)</u></b>:</div> 
<div style="color:black;font-size:13px;font-family:Source Sans Pro;">
<span>At the undergraduate level, a total of <b>{totmen_enroll} men</b> and <b>{totwomen_enroll} women</b> were enrolled, 
meaning a <b>male enrollment share</b> of <b>{totmen_share}%</b>.</span>
</div><br>'''


LMLABEL_ENROLL_GRAD = '''
<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Enrollment (Graduate)</u></b>:</div> 
<div style="color:black;font-size:13px;font-family:Source Sans Pro;">
<span>At the graduate level, a total of <b>{totmen_enroll} men</b> and <b>{totwomen_enroll} women</b> were enrolled, 
meaning a <b>male enrollment share</b> of <b>{totmen_share}%</b>.</span>
</div><br>'''


LMLABEL_GRADUATION_ASSC = '''
<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Three-Year Graduation (Associate's)</u></b>:</div> 
<div style="color:black;font-size:13px;font-family:Source Sans Pro;">
<span>Tracking a cohort of <b>{totmen} men</b> and <b>{totwomen} women</b>, three years later,
<b>{totmen_graduated} men</b> and <b>{totwomen_graduated} women graduated</b>, meaning a 
<b>male graduation rate</b> of <b>{gradrate_men}%</b>  and <b>female graduation rate</b> of <b>{gradrate_women}%</b>.</span>
</div><br>'''


LMLABEL_GRADUATION_BACH = '''
<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Six-Year Graduation (Bachelor's)</u></b>:</div> 
<div style="color:black;font-size:13px;font-family:Source Sans Pro;">
<span>Tracking a cohort of <b>{totmen} men</b> and <b>{totwomen} women</b>, six years later,
<b>{totmen_graduated} men</b> and <b>{totwomen_graduated} women graduated</b>, meaning a 
<b>male graduation rate</b> of <b>{gradrate_men}%</b>  and <b>female graduation rate</b> of <b>{gradrate_women}%</b>.</span>
</div>'''


# LMLABEL_ADMISSIONS = (
#     '<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Admissions</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Applied</b>: Men - {male_applied} | Women - {female_applied}</div>' +
#     '<div style="font-size:13px;"><b># Admitted</b>: Men - {male_admitted} | Women - {female_admitted}</div>' +
#     '<div style="font-size:13px;"><b># Enrolled</b>: Men - {male_enrolled} | Women - {female_enrolled}</div>' +
#     '<div style="font-size:13px;"><b>% Admitted</b>: Men - {male_accept}% | Women - {female_accept}%</div>' +
#     '<div style="font-size:13px;"><b>% Yield</b>: Men - {male_yield}% | Women - {female_yield}%</div>'
# )

# LMLABEL_GRADUATION_BACH1 = (
#     '<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Six-Year Graduation (Bachelor)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Cohort</b>: Men - {totmen} | Women - {totwomen}</div>' +
#     '<div style="font-size:13px;"><b># Graduated within six years</b>: Men - {totmen_graduated} | Women - {totwomen_graduated}</div>'
#     '<div style="font-size:13px;"><b>% Graduation</b>: Men - {gradrate_men}% | Women - {gradrate_women}%</div>'
# )

# LMLABEL_GRADUATION_ASSC1 = (
#     '<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Three-Year Graduation (Associate)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Cohort</b>: Men - {totmen} | Women - {totwomen}</div>' +
#     '<div style="font-size:13px;"><b># Graduated within three years</b>: Men - {totmen_graduated} | Women - {totwomen_graduated}</div>'
#     '<div style="font-size:13px;"><b>% Graduation</b>: Men - {gradrate_men}% | Women - {gradrate_women}%</div>'
# )

# LMLABEL_ENROLL_UNDERGRAD1 = (
#     '<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Enrollment (Undergraduate)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Total Enrollment</b>: Men - {totmen_enroll}% | Women - {totwomen_enroll}%</div>' +    
#     '<div style="font-size:13px;"><b>% Male Enrollment Share</b>: {totmen_share}%</div>' 
# )

# LMLABEL_ENROLL_GRAD1 = (
#     '<div style="font-size:15px;font-family:Source Sans Pro;"><b><u>Enrollment (Graduate)</u></b>:</div>' +
#     '<div style="font-size:13px;"><b># Total Enrollment</b>: Men - {totmen_enroll}% | Women - {totwomen_enroll}%</div>' +    
#     '<div style="font-size:13px;"><b>% Male Enrollment Share</b>: {totmen_share}%</div>' 
# )
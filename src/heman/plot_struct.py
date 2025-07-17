import plotly.graph_objects as go

'''
THEME LAYOUT
'''
THEME_LAYOUT = go.Layout(
    # FONT/TEXT
    font={
        'color': '#1e4a4a',
        'family': 'Helvetica'
    },
    title={
        'font': {
            'family': 'Georgia, serif',
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
        'subunitcolor': '#1e4a4a'
    },
    #NON-GEO PLOTS
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    scattermode='overlay',
    #GENERAL
    showlegend=True

)
THEME = go.layout.Template(layout=THEME_LAYOUT)

'''
COLORS
'''
GENDER_SPLIT_SCALE = [
        [0.0, '#30003B'], 
        [0.1, '#6c307b'],
        [0.3, '#9657A5'], 
        [0.4, '#CFBCD0'],
        [0.45, '#fbecfc'], 
        [.5, '#F3F4F3'],
        [0.55, '#d8f7e7'],
        [0.6, '#AAC9B8'], 
        [0.7, '#0B8569'],
        [0.9, '#00573e'], 
        [1.0, '#06474D']
]

ACCEPTANCE_RATE_SCALE = [
    [0.0, "#000004"],
    [0.1, "#1b0c41"],
    [0.2, "#4f0a6d"],
    [0.3, "#781c6d"],
    [0.4, "#a42c60"],
    [0.5, "#cc444c"],
    [0.6, "#ed6925"],
    [0.7, "#fb9a06"],
    [0.8, "#f7d13d"],
    [0.9, "#fcfdbf"],
    [1.0, "#ffffff"]
]

GRADUATION_RATE_SCALE = [
    [0.0, "#fd7f25"],
    [0.2, "#fdae25"],
    [0.35, "#fddd25"],
    [0.5, "#dede2b"],
    [0.55, "#c3de2b"],
    [0.6, "#b5de2b"],
    [0.65, "#6ece58"],
    [0.7, "#58ce7d"],
    [0.75, "#1f9e89"],
    [0.85, "#26748e"],
    [1.0, "#2c4682"]
]

EARNINGS_SCALE = [
    [0.0, "#320404"],
    [0.15, "#750C0C"],
    [0.25, "#8E3D3D"],
    [0.35, "#A75A5A"],
    [0.45, "#CF878E"],
    [0.5, "#CF87A9"],
    [0.55, "#DF9BD3"],
    [0.6, "#DFB8D8"],
    [0.75, "#AAA6F4"],
    [0.80, "#A8BCFE"],
    [1.0, "#CDEAF5"]
]

ORANGE_SCALE = [
        [0.0, "#551d01"],
        [0.4, '#75381e'], 
        [0.5, '#8e4d31'],
        [0.6, '#a56144'], 
        [0.65, '#ba7355'],
        [0.7, '#d08667'], 
        [.75, '#e49878'],
        [0.8, '#f8aa89'],
        [0.85, '#febc9a'], 
        [0.9, '#ffd2ae'],
        [0.95, '#ffe9c3'], 
        [1.0, '#ffffda']
]

MAGMA_SCALE = [
    [0.0, "#000004"],
    [0.1, "#1b0c41"],
    [0.2, "#4f0a6d"],
    [0.3, "#781c6d"],
    [0.4, "#a42c60"],
    [0.5, "#cc444c"],
    [0.6, "#ed6925"],
    [0.7, "#fb9a06"],
    [0.8, "#f7d13d"],
    [0.9, "#fcfdbf"],
    [1.0, "#ffffff"]
]

BLUE_SCALE = [
        [0.0, "#002d80"],
        [0.4, '#0047a0'], 
        [0.5, '#185bb9'],
        [0.6, '#4575D6'], 
        [0.65, '#5682e5'],
        [0.7, '#6c95f9'], 
        [.75, '#80a7ff'],
        [0.8, '#95bbff'],
        [0.85, '#a9cfff'], 
        [0.9, '#bae4ff'],
        [0.95, '#cdf5ff'], 
        [1.0, '#e2ffff']
]


'''
BUTTON TEMP
'''
BUTTON_TEMPLATE = {
        'label': 'Play',
        'method': 'animate',
        'args': [
            None,
            {
                'frame': {
                    'duration': 250,
                    'redraw': True,
                    'mode': 'next'
                },
                'fromcurrent': True
            }
        ]
    }

'''
MAJORS_RENAME (will be used for plots involving college majors):
'''
MAJORS_RENAME = {
    'Construction Trades': 'Construction Trades',
    'Precision Production': 'Precision Production',
    'Mechanic And Repair Technologies/Technicians': 'Mechanic And Repair',
    'Culinary, Entertainment, And Personal Services': 'Culinary/Entertainment/Personal Services',
    'Social Sciences': 'Social Sciences',
    'Agricultural/Animal/Plant/Veterinary Science And Related Fields': 'Agr./Animal/Plant/Vet. Sciences',
    'Engineering': 'Engineering',
    'Multi-/Interdisciplinary Studies': 'Multi/Interdisc. Studies',
    'Physical Sciences': 'Physical Sciences',
    'Education': 'Education',
    'Health Professions And Related Clinical Sciences': 'Health',
    'Family And Consumer Sciences/Human Sciences': 'Family & Consumer/Human Sciences',
    'Architecture And Related Services': 'Architecture',
    'Biological And Biomedical Sciences': 'Biological/Biomedical Sciences',
    'Engineering/Engineering-Related Technologies/Technicians': 'Engineering Technologies',
    'Homeland Security, Law Enforcement, Firefighting And Related Protective Services': 'Homeland Sec./Law Enf./Firefight.',
    'Communication, Journalism, And Related Programs': 'Communications/Journalism',
    'Business, Management, Marketing, And Related Support Services': 'Business/Management/Marketing',
    'Parks, Recreation, Leisure, Fitness, And Kinesiology': 'Parks/Fitness/Kinesiology',
    'Theology And Religious Vocations': 'Theology/Religious Vocations',
    'Computer And Information Sciences And Support Services': 'Computer Sciences',
    'Science Technologies/Technicians': 'Science Technologies',
    'Foreign Languages, Literatures, And Linguistics': 'Foreign Lang./Lit.',
    'Legal Professions And Studies': 'Legal Professions/Studies',
    'Philosophy And Religious Studies': 'Philosophy & Religious Studies',
    'Psychology': 'Psychology',
    'Visual And Performing Arts': 'Visual/Performing Arts',
    'Natural Resources And Conservation': 'Natural Resources & Conservation',
    'Public Administration And Social Service Professions': 'Public Adminin. & Social Service',
    'English Language And Literature/Letters': 'English Lang./Lit.',
    'Mathematics And Statistics': 'Mathematics & Statistics',
    'Communications Technologies/Technicians And Support Services': 'Communications Technologies',
    'Transportation And Materials Moving': 'Transportation & Materials Moving',
    'Library Scienc': 'Library Science',
    'Area, Ethnic, Cultural, Gender, And Group Studies': 'Cultural/Gender Studies',
    'Military Technologies And Applied Sciences': 'Military Technologies/Sciences'
}

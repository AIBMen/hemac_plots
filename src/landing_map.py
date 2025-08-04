import re
import os
from typing import Dict

import folium
import folium.plugins
from genpeds import (
    Admissions, 
    Enrollment, 
    Graduation, 
    Characteristics
)

from utils import (
    LMLABEL_HEAD, 
    LMLABEL_ADMISSIONS, 
    LMLABEL_ENROLL_UNDERGRAD, 
    LMLABEL_ENROLL_GRAD, 
    LMLABEL_GRADUATION_ASSC, 
    LMLABEL_GRADUATION_BACH
)


# MAP
_map = folium.Map(location=(39.8097343, -98.5556199),
                  zoom_control='topright',
                  tiles='Cartodb voyager',
                  zoom_start=5)
# full screen
_fullscreen = folium.plugins.Fullscreen(position='topright')
_fullscreen.add_to(_map)

# rm leaflet attr, cleaner attribution line
# Note that Leaflet creator himself says this is okay: https://groups.google.com/g/leaflet-js/c/fA6M7fbchOs/m/JTNVhqdc7JcJ
map_id = _map.get_name()
remove_leaflet_text_js = f'''
<script>
    setTimeout(function() {{
        if (typeof {map_id} !== 'undefined' && {map_id}.attributionControl && {map_id}.attributionControl.setPrefix) {{
            {map_id}.attributionControl.setPrefix('');
        }}
    }}, 50);
</script>
'''
_map.get_root().html.add_child(folium.Element(remove_leaflet_text_js))


class LandingMap:
    '''HEMAC Landing Map'''
    def __init__(self,
                 schools: Dict[str,str],
                 most_recent_year: int = 2023):
        '''
        Build HEMAC landing page map of partner schools
        
        :param schools: dict of partner school "ID: Name" key-value pairs
        :param most_recent_year: most recent year of data; defaults to 2023
        '''
        char = Characteristics(most_recent_year).run(False,False).query('year == @most_recent_year') # fix this

        admit = Admissions(most_recent_year).run(False,True,False).query('year == @most_recent_year') # fix this
        
        enroll_undergrad = Enrollment(most_recent_year).run('undergrad',False,True,False).query('year == @most_recent_year') # fix this
        enroll_grad = Enrollment(most_recent_year).run('grad',False,True,False).query('year == @most_recent_year') # fix this

        grad_two_year = Graduation(most_recent_year).run('assc',False,True,False).query('year == @most_recent_year') # fix this
        grad_four_year = Graduation(most_recent_year).run('bach',False,True,False).query('year == @most_recent_year') # fix this

        data = {
            'characteristics': char,
            'admissions': admit,
            'enrollment_undergrad': enroll_undergrad,
            'enrollment_grad': enroll_grad,
            'graduation_two_year': grad_two_year,
            'graduation_four_year': grad_four_year
        }
        for label,df in data.items():
            data[label] = df.loc[df['id'].isin(schools.keys())]
        
        self.data = data
        self.schools = schools
        self.map = _map
        self.data_dicts = {}
        self.labels = {}

    
    def build_data_dicts(self) -> None:
        '''builds school data'''
        for schl in self.schools.keys():
            # Header info
            schl_char = self.data['characteristics']
            schl_char = schl_char.loc[schl_char['id'] == schl]
            lat = schl_char['latitude'].unique()[0]
            lon = schl_char['longitude'].unique()[0]
            name = schl_char['id'].map(self.schools).unique()[0]    # get custom names from google sheet
            city = schl_char['city'].unique()[0]
            state = schl_char['state'].unique()[0]
            webaddr = schl_char['webaddress'].astype(str).unique()[0]
            if not re.search(r'^https\:\/\/',webaddr):
                webaddr = 'https://' + webaddr
            # Admissions info
            schl_admit = self.data['admissions'].loc[self.data['admissions']['id'] == schl]
            if len(schl_admit) > 0:
                schl_admit['female_applied'] = schl_admit['tot_applied'] - schl_admit['men_applied']
                schl_admit['female_admitted'] = schl_admit['tot_admitted'] - schl_admit['men_admitted']
                schl_admit['female_enrolled'] = schl_admit['tot_enrolled'] - schl_admit['men_enrolled']
                male_applied = schl_admit['men_applied'].astype(int).unique()[0]
                male_admitted = schl_admit['men_admitted'].astype(int).unique()[0]
                male_enrolled = schl_admit['men_enrolled'].astype(int).unique()[0]
                female_applied = schl_admit['female_applied'].astype(int).unique()[0]
                female_admitted = schl_admit['female_admitted'].astype(int).unique()[0]
                female_enrolled = schl_admit['female_enrolled'].astype(int).unique()[0]
                male_accept = schl_admit['accept_rate_men'].astype(int).unique()[0]
                male_yield = schl_admit['yield_rate_men'].astype(int).unique()[0]
                try:
                    female_accept = schl_admit['accept_rate_women'].astype(int).unique()[0]
                    female_yield = schl_admit['yield_rate_women'].astype(int).unique()[0]
                except Exception:
                    female_accept = 'NA'
                    female_yield = 'NA'
            else:
                male_applied = male_admitted = male_enrolled = None
                male_accept = male_yield = female_accept = female_yield = None
            # Enrollment (UNDERGRAD) info
            schl_enroll_ug = self.data['enrollment_undergrad'].loc[self.data['enrollment_undergrad']['id'] == schl]
            if len(schl_enroll_ug) > 0:
                totmen_enroll_ug = schl_enroll_ug['totmen'].astype(int).unique()[0]
                totwomen_enroll_ug = schl_enroll_ug['totwomen'].astype(int).unique()[0]
                totmen_share_ug = schl_enroll_ug['totmen_share'].astype(int).unique()[0]
            else:
                totmen_enroll_ug = totwomen_enroll_ug = totmen_share_ug = None
            # Enrollment (GRAD) info
            schl_enroll_g = self.data['enrollment_grad'].loc[self.data['enrollment_grad']['id'] == schl]
            if len(schl_enroll_g) > 0:
                totmen_enroll_g = schl_enroll_g['totmen'].astype(int).unique()[0]
                totwomen_enroll_g = schl_enroll_g['totwomen'].astype(int).unique()[0]
                totmen_share_g = schl_enroll_g['totmen_share'].astype(int).unique()[0]
            else:
                totmen_enroll_g = totwomen_enroll_g = totmen_share_g = None
            # Graduation (ASSC) info
            grad_2yr = self.data['graduation_two_year'].loc[self.data['graduation_two_year']['id'] == schl]
            if len(grad_2yr) > 0:
                totmen_grad_2yr = grad_2yr['totmen'].astype(int).unique()[0]
                totmen_graduated_grad_2yr = grad_2yr['totmen_graduated'].astype(int).unique()[0]
                totmen_grad_rate_2yr = grad_2yr['gradrate_totmen'].astype(int).unique()[0]
                try:
                    totwomen_grad_2yr = grad_2yr['totwomen'].astype(int).unique()[0]
                    totwomen_graduated_grad_2yr = grad_2yr['totwomen_graduated'].astype(int).unique()[0]
                    totwomen_grad_rate_2yr = grad_2yr['gradrate_totwomen'].astype(int).unique()[0]
                except Exception:
                    totwomen_grad_2yr = totwomen_graduated_grad_2yr = totwomen_grad_rate_2yr = 'NA'
            else:
                totmen_grad_2yr = totmen_graduated_grad_2yr = totmen_grad_rate_2yr = None
                totwomen_grad_2yr = totwomen_graduated_grad_2yr = totwomen_grad_rate_2yr = None
            # Graduation (BACH) info
            grad_4yr = self.data['graduation_four_year'].loc[self.data['graduation_four_year']['id'] == schl]
            if len(grad_4yr) > 0:
                totmen_grad_4yr = grad_4yr['totmen'].astype(int).unique()[0]
                totmen_graduated_grad_4yr = grad_4yr['totmen_graduated'].astype(int).unique()[0]
                totmen_grad_rate_4yr = grad_4yr['gradrate_totmen'].astype(int).unique()[0]
                try:
                    totwomen_grad_4yr = grad_4yr['totwomen'].astype(int).unique()[0]
                    totwomen_graduated_grad_4yr = grad_4yr['totwomen_graduated'].astype(int).unique()[0]
                    totwomen_grad_rate_4yr = grad_4yr['gradrate_totwomen'].astype(int).unique()[0]
                except Exception:
                    totwomen_grad_4yr = totwomen_graduated_grad_4yr = totwomen_grad_rate_4yr = 'NA'
            else:
                totmen_grad_4yr = totmen_graduated_grad_4yr = totmen_grad_rate_4yr = None
                totwomen_grad_4yr = totwomen_graduated_grad_4yr = totwomen_grad_rate_4yr = None
            
            self.data_dicts[schl] = {
                'lat': lat,
                'lon': lon,
                'name': name,
                'city': city,
                'state': state,
                'webaddr': webaddr,
                'admit_men_app': male_applied, 'admit_men_admit': male_admitted, 'admit_men_enroll': male_enrolled,
                'admit_women_app': female_applied, 'admit_women_admit': female_admitted, 'admit_women_enroll': female_enrolled,
                'admit_accept_men': male_accept, 'admit_yield_men': male_yield, 'admit_accept_women': female_accept, 'admit_yield_women': female_yield,
                'enroll_ug_men': totmen_enroll_ug, 'enroll_ug_women': totwomen_enroll_ug, 'enroll_ug_share': totmen_share_ug,
                'enroll_g_men': totmen_enroll_g, 'enroll_g_women': totwomen_enroll_g, 'enroll_g_share': totmen_share_g,
                'grad_2yr_men': totmen_grad_2yr, 'grad_2yr_mengrad': totmen_graduated_grad_2yr, 'grad_2yr_menrate': totmen_grad_rate_2yr, 
                'grad_2yr_women': totwomen_grad_2yr, 'grad_2yr_womengrad': totwomen_graduated_grad_2yr, 'grad_2yr_womenrate': totwomen_grad_rate_2yr, 
                'grad_4yr_men': totmen_grad_4yr, 'grad_4yr_mengrad': totmen_graduated_grad_4yr, 'grad_4yr_menrate': totmen_grad_rate_4yr,
                'grad_4yr_women': totwomen_grad_4yr, 'grad_4yr_womengrad': totwomen_graduated_grad_4yr, 'grad_4yr_womenrate': totwomen_grad_rate_4yr
            }
    
    def build_labels(self) -> None:
        '''build school labels'''
        for schl,data in self.data_dicts.items():
            lab = ''
            lab += LMLABEL_HEAD.format(name=data['name'],
                                       city=data['city'],
                                       state=data['state'],
                                       webaddr=data['webaddr'])
            if data['admit_men_app']:
                lab += LMLABEL_ADMISSIONS.format(name=data['name'],
                                                 male_applied=data['admit_men_app'],
                                                 male_admitted=data['admit_men_admit'],
                                                 male_enrolled=data['admit_men_enroll'],
                                                 female_applied=data['admit_women_app'],
                                                 female_admitted=data['admit_women_admit'],
                                                 female_enrolled=data['admit_women_enroll'],
                                                 male_accept=data['admit_accept_men'],
                                                 male_yield=data['admit_yield_men'],
                                                 female_accept=data['admit_accept_women'],
                                                 female_yield=data['admit_yield_women'])
            if data['enroll_ug_men']:
                lab += LMLABEL_ENROLL_UNDERGRAD.format(totmen_enroll=data['enroll_ug_men'],
                                                       totwomen_enroll=data['enroll_ug_women'],
                                                       totmen_share=data['enroll_ug_share'])
            if data['enroll_g_men']:
                lab += LMLABEL_ENROLL_GRAD.format(totmen_enroll=data['enroll_g_men'],
                                                       totwomen_enroll=data['enroll_g_women'],
                                                       totmen_share=data['enroll_g_share'])
            if data['grad_2yr_men']:
                lab += LMLABEL_GRADUATION_ASSC.format(totmen=data['grad_2yr_men'],
                                                      totmen_graduated=data['grad_2yr_mengrad'],
                                                      gradrate_men=data['grad_2yr_menrate'],
                                                      totwomen=data['grad_2yr_women'],
                                                      totwomen_graduated=data['grad_2yr_womengrad'],
                                                      gradrate_women=data['grad_2yr_womenrate'])
            if data['grad_4yr_men']:
                lab += LMLABEL_GRADUATION_BACH.format(totmen=data['grad_4yr_men'],
                                                      totmen_graduated=data['grad_4yr_mengrad'],
                                                      gradrate_men=data['grad_4yr_menrate'],
                                                      totwomen=data['grad_4yr_women'],
                                                      totwomen_graduated=data['grad_4yr_womengrad'],
                                                      gradrate_women=data['grad_4yr_womenrate'])
            lab += '<div style="font-size:14px;color:white">_____________________________________________________________________</div></div></html>'
            self.labels[schl] = lab
    
    def build_map(self) -> None:
        '''builds folium map'''
        fg = folium.FeatureGroup()
        fg.add_to(self.map)
        search_bar = folium.plugins.Search(layer=fg,
                                           search_label='name',
                                           placeholder='Search by HEMAC school name/location',
                                           color='#06474D')
        search_bar.add_to(self.map)
        for schl in self.schools.keys():
            lab = self.labels[schl]
            dat = self.data_dicts[schl]
            mkr = folium.Marker(
                location=[dat['lat'],dat['lon']],
                popup=lab,
                tooltip=folium.Tooltip(text=f"<b>{dat['name']}</b><br>({dat['city']}, {dat['state']})",
                                       style='color:#001A50;font-family:Source Sans Pro;font-size:13px;text-align:center;'),
                icon=folium.plugins.BeautifyIcon(icon_shape='marker',
                                       icon='institution',
                                       text_color="white",
                                       border_width=0,
                                       background_color="#001950B1"),
                name=dat['name']
            )
            mkr.add_to(fg)
        self.map.save(os.path.join('docs','map','landing_map.html'))
    




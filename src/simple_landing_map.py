import os
from typing import Dict

import folium
import folium.plugins
from genpeds import Characteristics


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


class SimpleLandingMap:
    '''simplified version of HEMAC landing page map'''
    def __init__(self,
                 schools: Dict[str,str],
                 most_recent_year: int = 2023):
        '''
        Build HEMAC landing page map of partner schools
        
        :param schools: dict of partner school "ID: Name" key-value pairs
        :param most_recent_year: most recent year of data; defaults to 2023
        '''
        dat = Characteristics(year_range=most_recent_year).run()
        dat = dat.loc[dat['id'].isin(schools.keys())]
        dat['name'] = dat['id'].map(schools)
        
        self.schools = schools
        self.dat = dat
        self.map = _map
    

    def build_map(self) -> None:
        '''builds folium map'''
        fg = folium.FeatureGroup()
        fg.add_to(self.map)
        search_bar = folium.plugins.Search(layer=fg,
                                           search_label='name',
                                           placeholder='Search by HEMAC school name/location',
                                           color='#06474D')
        search_bar.add_to(self.map)
        
        for idx, r in self.dat.iterrows():
            popup = (
                '<html><div style="color:#001A50;">' +
                f'<div style="font-size:18px;font-family:Source Sans Pro;"><b>{r['name']}</b></div>' +
                f'<div style="font-size:13px;"><i>{r['city']}, {r['state']}</i></div>' +
                f'<div style="font-size:13px;"><a target="_blank" rel="noopener noreferrer" href="{r['webaddress']}">{r['webaddress']}</a></div>'
                '<br>'
            )
            mkr = folium.Marker(
                location=[r['latitude'], r['longitude']],
                popup=popup,
                tooltip=folium.Tooltip(text=f"<b>{r['name']}</b><br>({r['city']}, {r['state']})",
                                       style='color:#001A50;font-family:Source Sans Pro;font-size:13px;text-align:center;'),
                icon=folium.plugins.BeautifyIcon(icon_shape='marker',
                                       icon='institution',
                                       text_color="white",
                                       border_width=0,
                                       background_color="#001950B1"),
                name=r['name']
            )
            mkr.add_to(fg)
        
        self.map.save(os.path.join('docs','map','simple_landing_map.html'))

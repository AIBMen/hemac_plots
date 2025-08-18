import os
from typing import Dict

from genpeds import Characteristics


class SimpleLandingTable:
    '''HEMAC partners landing table'''
    def __init__(self,
                 schools: Dict[str,str],
                 most_recent_year: int = 2023):
        '''
        Build HEMAC landing page table of partner schools
        
        :param schools: dict of partner school "ID: Name" key-value pairs
        :param most_recent_year: most recent year of data; defaults to 2023
        '''
        dat = Characteristics(year_range=most_recent_year).run()
        dat = dat.loc[dat['id'].isin(schools.keys())]
        dat['name'] = dat['id'].map(schools)
        
        self.schools = schools
        self.dat = dat
    

    def build_table(self) -> None:
        '''generate landing table'''
        COLS2KEEP = {
            'name': 'School',
            'city': 'City',
            'state': 'State'
        }
        tab_dat = self.dat.copy().reindex(columns=COLS2KEEP.keys())
        tab_dat = tab_dat.rename(columns=COLS2KEEP)

        dat_html = tab_dat.to_html(index=False,
                                   table_id='hemac_schools',
                                   classes='cell-border display compact hover table table-striped')

        dataTable = f'''
                    <!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <meta charset="UTF-8">
                        <title>HEMAC Schools</title>

                        <!-- Bootstrap CSS -->
                        <link
                            href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/css/bootstrap.min.css"
                            rel="stylesheet"
                            integrity="sha384-…"
                            crossorigin="anonymous"
                        />

                        <!-- DataTables + Buttons CSS -->
                        <link
                            href="https://cdn.datatables.net/v/bs5/dt-2.3.1/r-3.0.4/b-3.2.3/b-html5-3.2.3/b-print-3.2.3/datatables.min.css"
                            rel="stylesheet"
                        />
                        <style>
                            /* ==== Pagination ==== */
                            .dataTables_wrapper .dataTables_paginate .pagination .page-item.active .page-link {{
                            background-color: #001A50 !important;
                            border-color:     #001A50 !important;
                            color:            #fff     !important;
                            }}
                            .dataTables_wrapper .dataTables_paginate .pagination .page-item .page-link:hover {{
                            background-color: #05292C !important;
                            border-color:     #05292C !important;
                            color:            #fff     !important;
                            }}

                            /* ==== Export Buttons ==== */
                            .btn-dt-teal {{
                            background-color: #001A50 !important;
                            border-color:     #001A50 !important;
                            color:            #fff     !important;
                            }}
                            .btn-dt-teal:hover,
                            .btn-dt-teal:focus {{
                            background-color: #05292C !important;  
                            border-color:     #05292C !important;
                            color:            #fff     !important;
                            }}

                            /* ==== Table styling ==== */
                            table.dataTable th,
                            table.dataTable td {{
                            font-family: 'Helvetica';
                            color:        #000000 ;
                            }}
                            table.dataTable th:first-child,

                            table.dataTable td:first-child {{
                            position: sticky;
                            left: 0;
                            z-index: 2; 
                            }}
                            /* Override Bootstrap pagination styling */
                            .pagination .page-item .page-link {{
                                background-color: #001A50 !important;
                                border-color: #333333 !important;
                                color: #ffffff !important;
                            }}

                            .pagination .page-item.active .page-link {{
                                background-color: #001A50 !important;
                                border-color: #333333 !important;
                                color: #AAC9B8 !important;
                                z-index: 3;
                            }}

                            .pagination .page-item .page-link:hover {{
                                background-color: #001A50 !important;
                                border-color: #333333 !important;
                                color: #ffffff !important;
                            }}

                            .pagination .page-item.disabled .page-link {{
                                background-color: #001A50 !important;
                                border-color: #333333 !important;
                                color: #666666 !important;
                            }}
                        </style>
                        </head>
                        <body class="p-4">
                        {dat_html}

                        <!-- JS dependencies at end for faster load -->
                        <script
                            src="https://code.jquery.com/jquery-3.7.0.min.js"
                            integrity="sha256-…"
                            crossorigin="anonymous">
                        </script>
                        <script
                            src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.3.0/js/bootstrap.bundle.min.js"
                            integrity="sha384-…"
                            crossorigin="anonymous">
                        </script>
                        <script
                            src="https://cdn.datatables.net/v/bs5/dt-2.3.1/b-3.2.3/b-html5-3.2.3/b-print-3.2.3/datatables.min.js">
                        </script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

                        <script>
                        $(function () {{
                            $('#hemac_schools').DataTable({{
                                dom: 'Bfrtip',
                                language: {{
                                        search: "",                       
                                        searchPlaceholder: "Search a school",
                                    }},
                                buttons: [
                                            {{ extend: 'copy',  className: 'btn btn-sm btn-dt-teal' }},
                                            {{ extend: 'csv',   className: 'btn btn-sm btn-dt-teal' }},
                                            {{ extend: 'excel', className: 'btn btn-sm btn-dt-teal' }}
                                        ],
                                responsive: true,
                                scrollY: true
                            }});
                            }});
                        </script>
                        </body>
                    </html>
'''
        with open(os.path.join('docs','table','simple_landing_table.html'),'w') as lt_html:
            lt_html.write(dataTable)
        
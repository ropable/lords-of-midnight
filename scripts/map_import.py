import BeautifulSoup
import os

map_list = []
soup = BeautifulSoup.BeautifulSoup(open('map_htm', 'r'))
for row in soup.findAll('tr'):
    row_list = []
    for col in row.findAll('td'):
        for img in col.findAll('img'):
            # Create a dict of each img file: the filename and alt.
            row_list.append({'terrain_type':img['src'], 'name':img['alt']})
    map_list.append(row_list)

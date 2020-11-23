def r(p1, p2):
    long_diff = np.radians(p2[1] - p1[1])
    
    lat1 = np.radians(p1[0])
    lat2 = np.radians(p2[0])
    
    x = np.sin(long_diff) * np.cos(lat2)
    y = (np.cos(lat1) * np.sin(lat2) 
        - (np.sin(lat1) * np.cos(lat2) 
        * np.cos(long_diff)))
    rotate = np.degrees(np.arctan2(x, y))
    if rotate < 0:
        return rotate + 360
    return rotate

m = f.Map(location=[40.783435, -73.96625], tiles="Stamen Terrain", zoom_start=11)

for coord in idx.items():
    f.PolyLine(locations=coord, weight=1, color = 'black').add_to(m)
    
    f.RegularPolygonMarker(location=coord[1], 
                          fill_color='black', number_of_sides=3, 
                          radius=4, rotation=r(coord[0], coord[1]) - 90, 
                           weight=0, fill=True, fill_opacity=1).add_to(m)
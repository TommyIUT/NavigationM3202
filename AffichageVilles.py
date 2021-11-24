from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

def dessiner_carte(m, scale=0.2):
    # Crée le fond de carte
    m.shadedrelief(scale=scale)
    
    # latitudes et longitudes retournes dans un dictionnaire
    latitudes = m.drawparallels(np.linspace(-90, 90, 12))
    longitudes = m.drawmeridians(np.linspace(-180, 180, 12))

    # keys contain the plt.Line2D instances
    paralleles = chain(*(tup[1][0] for tup in latitudes.items()))
    meridiens = chain(*(tup[1][0] for tup in longitudes.items()))
    all_lines = chain(paralleles, meridiens)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')
    

fig = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )


#Paris
plt.plot(2.3, 48.8 , 'ok', markersize=3)
plt.text(2.3, 48.8 , ' Paris', fontsize=10)

#Tokyo
plt.plot(139.7, 35.78 , 'ok', markersize=3)
plt.text(139.7, 35.78 , ' Tokyo', fontsize=10)

#Le Cap
plt.plot(18.4, -33.9 , 'ok', markersize=3)
plt.text(18.4, -33.9 , ' Le Cap', fontsize=10)

#Mexico
plt.plot(-102.5, 23.6 , 'ok', markersize=3)
plt.text(-102.5, 23.6 , ' Mexico', fontsize=10)

#Punta Arenas
plt.plot(-70.9, -53.1 , 'ok', markersize=3)
plt.text(-70.9, -53.1 , ' Punta Arenas', fontsize=10)

dessiner_carte(m)

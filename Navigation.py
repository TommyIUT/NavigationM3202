import math as ma
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import chain


def dessiner_carte_mercator(m, scale=0.2):
    # Crée le fond de carte
    m.shadedrelief(scale=scale)
    
    # Affiche les parallèles et méridiens
    latitudes = m.drawparallels(np.linspace(-90, 90, 12))
    longitudes = m.drawmeridians(np.linspace(-180, 180, 12))


    # Stocke les longitudes et les latitudes
    paralleles = chain(*(tup[1][0] for tup in latitudes.items()))
    meridiens = chain(*(tup[1][0] for tup in longitudes.items()))
    all_lines = chain(paralleles, meridiens)
    
    # Change le style des parallèles et méridiens
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

# Demande et retourne la latitude d'un point
def demanderLatitude(p):
    return float(input("Entrez la Latitude du point "+p+" : "))


# Demande et retourne la longitude d'un point
def demanderLongitude(p):
    return float(input("Entrez la longitude du point "+p+" : "))

# Retourne la distance orthodromique entre deux points
def calculerDistance(long1, long2, lat1, lat2):
    
    return ma.acos(ma.sin(lat1)*ma.sin(lat2) + ma.cos(lat1)*ma.cos(lat2)*ma.cos(long1-long2))

# Retourne le cap entre 2 points
def calculerCap (long1, long2, lat1, lat2, d):
    
    v = (ma.sin(lat2) - ma.sin(lat1) * ma.cos(d))/(ma.cos(lat1) * ma.sin(d))
    x = ma.acos(v)
    if ((long1 < long2) & (abs(ma.degrees(long1)-ma.degrees(long2)) < 180)) | \
        ((long1 > long2) & (abs(ma.degrees(long1)-ma.degrees(long2)) > 180)) :
        return x
    else:
        return 2*ma.pi - x

# Coordonnés du prochain point dans l'orthodromie
def calculerLongitudePrime(long1,lat1, angle, intervalle):
    
    return long1 + intervalle * Q * ma.sin(angle)/ ma.cos(lat1)

def calculerLatitudePrime(lat1, angle, intervalle):
    
    return lat1 + ma.cos(angle) * intervalle * Q

# Trace la loxodromie
def tracerLoxodromie(long1, long2, lat1, lat2):
    
    if (abs(long1-long2) < 180):
        plt.plot([long1, long2], [lat1, lat2] , 'r-')
    else:
        if (long1>long2):
            plt.plot([long1, long2+360], [lat1, lat2] , 'r-')
            plt.plot([long1-360, long2], [lat1,lat2] , 'r-')
        else:
            plt.plot([long1, long2-360], [lat1, lat2] , 'r-')
            plt.plot([long1+360, long2], [lat1, lat2] , 'r-')

# Afficher les Indications
def donnerInformations(long1, long2):
    if(long1 == long2):
        print("\n\n L'orthodromie et la loxodromie se confondent dans la droite noire.")
    else:
        print("\n\nL'orthodromie est la courbe verte.")
        print("La loxodromie est la droite rouge.")

        
#Debut du prorgamme principal
fig = plt.figure(figsize=(8, 6), edgecolor='w')
m = Basemap(projection='cyl', resolution=None,
            llcrnrlat=-90, urcrnrlat=90,
            llcrnrlon=-180, urcrnrlon=180, )


Q = ma.pi / (1.852*60*180)
print(ma)

# Création des points
longAdeg = demanderLongitude("A")
latAdeg  = demanderLatitude("A")
longBdeg = demanderLongitude("B")
latBdeg = demanderLatitude("B") 

# Conversion en radians
longA = ma.radians(longAdeg)
longB = ma.radians(longBdeg)
latA  = ma.radians(latAdeg)
latB  = ma.radians(latBdeg)

distanceInitiale = calculerDistance(longA, longB, latA, latB)
print("\nLa distance entre les villes A et B est de " + str(round(distanceInitiale * 6371)) + " kilomètres.")

if (longAdeg == longBdeg):
    plt.plot([longAdeg, longBdeg], [latAdeg, latBdeg] , 'k-')
    
else:
    
    intervalle = 100
    
    capInitial = calculerCap(longA, longB, latA, latB, distanceInitiale)
    
    longPrime = calculerLongitudePrime(longA, latA, capInitial,intervalle)
    latPrime  = calculerLatitudePrime(latA, capInitial, intervalle)
    
    plt.plot([longAdeg, ma.degrees(longPrime)], [latAdeg, ma.degrees(latPrime)] , 'g-')
    
    distance = calculerDistance(longPrime, longB, latPrime, latB)
    
    #Tracer l'orthodromie
    while (distance*6371 >= intervalle):
    
        if(ma.degrees(longPrime)<(-180)):
            longPrime += ma.radians(360)
            
        if(ma.degrees(longPrime)>(180)):
            longPrime -= ma.radians(360)
            
        longPrec = longPrime
        latPrec = latPrime
        cap = calculerCap(longPrime, longB, latPrime, latB, distance)
        
        longPrime = calculerLongitudePrime(longPrime, latPrime, cap, intervalle)
        latPrime  = calculerLatitudePrime(latPrime, cap, intervalle)
        
        plt.plot([ma.degrees(longPrec), ma.degrees(longPrime)], [ma.degrees(latPrec), ma.degrees(latPrime)] , 'g-')
        distance = calculerDistance(longPrime,longB, latPrime, latB)
    
    plt.plot([ma.degrees(longPrime), longBdeg], [ma.degrees(latPrime), latBdeg] , 'g-')   
    tracerLoxodromie(longAdeg, longBdeg, latAdeg, latBdeg)

#Placer les points sur la carte
plt.plot(longAdeg, latAdeg , 'ok', markersize=3)
plt.plot(longBdeg, latBdeg , 'ok', markersize=3)
    
donnerInformations(longAdeg, longBdeg)
dessiner_carte_mercator(m)

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, MultiPoint

# Places visited
# https://gist.github.com/samcormack/5eeaec44cd95a682c287261bdd0cb7c8
stops = gpd.read_file('data/stops.json')
routes = list()
for a, b in zip(stops.geometry[:-1], stops.geometry[1:]):
    routes.append(LineString([a, b]))
routes = gpd.GeoSeries(routes)
routes.crs = stops.crs

# States
# https://eric.clst.org/tech/usgeojson/
EXCLUDE = ['Alaska', 'Hawaii', 'Puerto Rico']

states = gpd.read_file('data/gz_2010_us_040_00_500k.json')
states = states[~states['NAME'].isin(EXCLUDE)]

# States visited
visited = states[states.intersects(MultiPoint(stops.geometry))]


# Plotting
plot_crs = {'init': 'epsg:2277'}
fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
ax.set_aspect('equal')
# states.to_crs(plot_crs).plot(ax=ax, color='white', edgecolor='#8f8f8f', linewidth=0.1)
visited.to_crs(plot_crs).plot(ax=ax, color='#ffc4c4', edgecolor='white', linewidth=0.8)

routes.to_crs(plot_crs).plot(ax=ax, color='#ff5454', linewidth=1.6) 

ax.collections[1].set_capstyle('round')

ax.text(0.9, 0.0, 'B & S 2017', 
    horizontalalignment='center', 
    verticalalignment='center', 
    transform=ax.transAxes, 
    fontfamily='Josefin Sans', 
    fontweight='light',
    fontsize=26)

plt.axis('off')
plt.savefig('maps/roadtripmap.pdf')
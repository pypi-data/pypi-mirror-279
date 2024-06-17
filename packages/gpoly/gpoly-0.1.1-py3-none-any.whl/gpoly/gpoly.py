import sys, json, click, importlib.metadata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patheffects as pe
import numpy as np
from skimage import measure

#  ──────────────────────────────────────────────────────────────────────────
# global variables

gpoly_version = importlib.metadata.version('gpoly')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

#  ──────────────────────────────────────────────────────────────────────────
# global options

grid_json_option = click.option('-g', '--grid', 'grid_json', type=click.Path(exists=True), help='Path to gpoly-ready grid.JSON file', required=True)

# resolutions

res_option = click.option('-r', '--res', type=click.Choice(['110m', '50m', '10m']), default='110m', show_default=True, help='Resolution of the coastline; lower resolution is faster.')

grid_res_option = click.option('-gr', '--grid-res', 'grid_res', type=float, default=10, show_default=True, help='Resolution of the gridlines in degrees. Default is 10 deg.')

snap_grid_res_option = click.option('-sgr', '--snap-grid-res', 'snap_grid_res', type=str, default='1', show_default=True, help='Resolution of the snapping gridlines in degrees. Default is 1 deg.')

extent_option = click.option('-e', '-ext', '--extent', nargs=4, type=click.Tuple([float, float, float, float]), default=None, help='Set the extent of the map (-e lon./east lon./west lat./south lat./north); e.g. -e -7 37 29 47 for the Med. Sea.')

#  ──────────────────────────────────────────────────────────────────────────
# global functions

def snap_grid(snap_grid_res):
    snap_lon, snap_lat = np.meshgrid(np.arange(-180, 180 + snap_grid_res, snap_grid_res), np.arange(-90, 90 + snap_grid_res, snap_grid_res))
    return snap_lon.flatten(order='C'), snap_lat.flatten(order='C')


def snapping(x, y, snap_x, snap_y):
    dist = ( (snap_x - x)**2 + (snap_y - y)**2 )**.5
    return np.argmin(dist)


def plot_earth(res, grid_res, extent):

    colors = {'coast': (0, 0.51, 0.02, 1),
              'land': (27/255, 255/255, 0, 0.7),
              'ocean': (0, 122/255, 255/255, 0.7),
              'point': (245/255, 40/255, 145/255, 1),
              'polygon': (245/255, 40/255, 145/255, 0.75),
              }

    coast = cfeature.NaturalEarthFeature('physical', 'land', res, edgecolor=colors['coast'], facecolor=colors['land'])
    ocean = cfeature.NaturalEarthFeature('physical', 'ocean', res, edgecolor=(0, 0, 0), facecolor=colors['ocean']) 

    # make world plot
    fig, ax = plt.subplots(1, 1, subplot_kw={'projection': ccrs.PlateCarree()})

    # setting up gridlines for lat. long.
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=.75, color='black', alpha=0.1, linestyle='--', zorder=6)

    # removing upper and right lat. long. labels
    gl.top_labels = False
    gl.right_labels = False

    # fixing lat long. locations
    gl.xlocator = mticker.FixedLocator(np.arange(-180, 180 + grid_res, grid_res)) # longitude
    gl.ylocator = mticker.FixedLocator(np.arange(-90, 90 + grid_res, grid_res))  # latitude
    gl.xformatter = LONGITUDE_FORMATTER  # formatter needed to get proper labels
    gl.yformatter = LATITUDE_FORMATTER

    # add coast and ocean
    ax.add_feature(coast, zorder=1)
    ax.add_feature(ocean, zorder=1)

    # extent
    if extent:
        ax.set_extent(extent, crs=ccrs.PlateCarree())

    fig.tight_layout()
    fig.canvas.draw()

    ax.autoscale(False)

    return fig, ax, colors

#  ──────────────────────────────────────────────────────────────────────────
# global classes

class SnappingCursor:
    """
    A cross-hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    def __init__(self, ax, res):
        self.ax = ax
        self.res = res
        self.get_decimals()
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        self.x, self.y = snap_grid(self.res)
        self._last_index = None
        # text location in axes coords
        self.text = ax.text(0.7, 0.95, '', transform=ax.transAxes, weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground='white')])


    def get_decimals(self):
        if '.' in self.res:
            self.decimals = len(self.res.split('.')[-1])
        else:
            self.decimals = 0
        self.res = float(self.res)


    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw


    def on_mouse_move(self, event, lon, lat, colors):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)

            if need_redraw:
                if len(lon) > 0:
                    points = self.ax.scatter(lon, lat, transform=ccrs.PlateCarree(), color=colors['point'], edgecolor='k')
                    polygon = self.ax.fill(lon, lat, transform=ccrs.PlateCarree(), color=colors['polygon'])

                self.ax.figure.canvas.draw()

                if len(lon) > 0:
                    points.remove()
                    polygon[0].remove()

        else:
            self.set_cross_hair_visible(True)
            index = snapping(event.xdata, event.ydata, self.x, self.y)

            if index == self._last_index:
                return  # still on the same data point. Nothing to do.

            self._last_index = index
            x = self.x[index]
            y = self.y[index]
            # update the line positions
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            self.text.set_text(f'Lon.={x:1.{self.decimals}f}, Lat.={y:1.{self.decimals}f}')

            if len(lon) > 0:
                points = self.ax.scatter(lon, lat, transform=ccrs.PlateCarree(), color=colors['point'], edgecolor='k')
                polygon = self.ax.fill(lon, lat, transform=ccrs.PlateCarree(), color=colors['polygon'])

            self.ax.figure.canvas.draw()

            if len(lon) > 0:
                points.remove()
                polygon[0].remove()

#  ──────────────────────────────────────────────────────────────────────────
# base command

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(gpoly_version)
@click.pass_context
def gpoly(ctx):
    pass

#  ──────────────────────────────────────────────────────────────────────────
# mapping command to draw a polygon

@gpoly.command('map', short_help='Polygon creation tool.')
@res_option
@grid_res_option
@snap_grid_res_option
@extent_option
@click.option('-p', '--polygons', 'polygon_jsons', type=click.Path(exists=True), multiple=True, help='')
@click.pass_context
def map(ctx, res, grid_res, snap_grid_res, extent, polygon_jsons):
    """Create a polygon on the world map. Outputs a JSON object with the polygon vertices."""

    def onclick(event, ax, colors, lon, lat, snap_lon, snap_lat):

        if event.button == 3: # only works with right click to avoid clicking interference while zooming

            index = snapping(event.xdata, event.ydata, snap_lon, snap_lat)

            lon.append(snap_lon[index])
            lat.append(snap_lat[index])

            points = ax.scatter(lon, lat, transform=ccrs.PlateCarree(), color=colors['point'], edgecolor='k')
            polygon = ax.fill(lon, lat, transform=ccrs.PlateCarree(), color=colors['polygon'])

            fig.canvas.draw()

            polygon[0].remove()
            points.remove()


    fig, ax, colors = plot_earth(res, grid_res, extent)

    # initiating map with points
    lon, lat = [], []

    snap_lon, snap_lat = snap_grid(float(snap_grid_res))
    fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, ax, colors, lon, lat, snap_lon, snap_lat))

    # adding compositing polygons
    polygons = []
    for polygon_json in polygon_jsons:
        with open(polygon_json, 'r') as file:
            polygons.append(json.load(file))

    cmap = plt.get_cmap('rainbow', len(polygons))

    lons, lats = [], []
    for i, polygon in enumerate(polygons):
        lons.append(np.array(polygon['points'])[:,0].tolist())
        lats.append(np.array(polygon['points'])[:,1].tolist())

    for i, _ in enumerate(lons):
        ax.scatter(lons[i], lats[i], transform=ccrs.PlateCarree(), color=cmap(i), edgecolor='k')
        ax.fill(lons[i], lats[i], transform=ccrs.PlateCarree(), color=cmap(i), alpha=0.7)

    # snapping
    snap_cursor = SnappingCursor(ax, snap_grid_res)
    fig.canvas.mpl_connect('motion_notify_event', lambda event: snap_cursor.on_mouse_move(event, lon, lat, colors))

    plt.show()

    data = {'gpoly': gpoly_version,
            'description': 'Geopoly JSON containing the vertices of the polygon. Stored in a list of (longitude, latitude) tuples.',
            'points': [],
            }

    for i, loni in enumerate(lon):
        data['points'].append((loni, lat[i]))

    click.echo(json.dumps(data))

#  ──────────────────────────────────────────────────────────────────────────
# make grid mask with polygon

@gpoly.command('mask', short_help='Create a polygon(s) mask(s) for a grid.')
@grid_json_option
@click.argument('polygon_jsons', nargs=-1, type=click.Path(exists=True))
@click.pass_context
def mask(ctx, grid_json, polygon_jsons):
    """
    Create a mask of the given grid in the grid.JSON file marking the points within the polygons given in the POLYGON_JSONS files. Outputs a JSON object containing the grid, masks, and polygons.

    The grid.JSON file needs to have 2D grids for both the 'lon' and 'lat' keys.

    When giving multiple POLYGON_JSONS files, if they overlap, the polygons supplied first maintain their boundaries and overlaps in the proceeding masks are removed (first listed, first prioritized).
    """

    with open(grid_json, 'r') as file:
        grid = json.load(file)

    # adding compositing polygons
    polygons = []
    for polygon_json in polygon_jsons:
        with open(polygon_json, 'r') as file:
            polygons.append(json.load(file))

    # masking
    grid_points = np.array([np.array(grid['lon']).flatten(order='C'), np.array(grid['lat']).flatten(order='C')]).transpose()

    masks = []
    for i, polygon in enumerate(polygons):
        polygon_points = polygon['points']
        masks.append(measure.points_in_poly(grid_points, polygon_points).reshape(np.array(grid['lon']).shape, order='C').astype(int))

    # correcting overlapping
    overlaps = []
    for i, maski in enumerate(masks):
        for j, maskj in enumerate(masks):
            if not maski.astype(bool) is maskj.astype(bool):
                if j > i: # order matters; precedence equals priority
                    overlap = maski.astype(bool) & maskj.astype(bool)
                    if overlap.any():
                        overlaps.append((i, j, overlap))

    for overlap in overlaps:
        masks[overlap[1]][overlap[-1]] = 0

    # preparing data
    for i, mask in enumerate(masks):
        masks[i] = mask.tolist()

    data = {'gpoly': gpoly_version,
            'description': 'Mask JSON file for grid points inside the given polygon (provided in the "polygon" key: 1 for within polygon, 0 for outside.',
            'grid': grid,
            'masks': masks,
            'polygons': polygons,
            }

    click.echo(json.dumps(data))

#  ──────────────────────────────────────────────────────────────────────────
# make grid mask with polygon

@gpoly.command('show', short_help='Show grid/masks/polygons.')
@res_option
@grid_res_option
@snap_grid_res_option
@extent_option
@click.option('--grid/--no-grid', '-G/-NG', 'grid_flag', show_default=True, default=True, help='Show grid.')
@click.option('--masks/--no-masks', '-M/-NM', 'masks_flag', show_default=True, default=True, help='Show masks.')
@click.option('--polygons/--no-polygons', '-P/-NP', 'polygons_flag', show_default=True, default=True, help='Show polygons.')
@click.option('--polygon_points/--no-polygon-points', '-PP/-NPP', 'polygon_points_flag', show_default=True, default=True, help='Show polygon points.')
@click.option('--labels/--no-labels', '-L/-NL', 'labels_flag', show_default=True, default=True, help='Show polygon/mask labels.')
@click.argument('masks_json', type=click.Path(exists=True))
@click.pass_context
def show(ctx, res, grid_res, snap_grid_res, extent, grid_flag, masks_flag, polygons_flag, polygon_points_flag, labels_flag, masks_json):
    """
    Show polygon masks and polygons from the MASKS_JSON.
    """

    # adding compositing polygons
    with open(masks_json, 'r') as file:
        tmp = json.load(file)
        grid = tmp['grid']
        masks = tmp['masks']
        polygons = tmp['polygons']

    # global plot and colors
    fig, ax, _ = plot_earth(res, grid_res, extent)
    colors = plt.get_cmap('rainbow', len(masks))

    grid_points = np.array([np.array(grid['lon']).flatten(order='C'), np.array(grid['lat']).flatten(order='C')]).transpose()

    if grid_flag:
        ax.scatter(grid_points[:,0], grid_points[:,1], transform=ccrs.PlateCarree(), color='k', marker='+')

    # adding masks and polygons
    for i, polygon in enumerate(polygons):

        lons = np.array(polygon['points'])[:,0]
        lats = np.array(polygon['points'])[:,1]

        # adding polygon
        if polygons_flag:
            ax.fill(lons, lats, transform=ccrs.PlateCarree(), color=colors(i), alpha=0.2)

            if polygon_points_flag:
                ax.scatter(lons, lats, transform=ccrs.PlateCarree(), color=colors(i), edgecolor='k')

        # adding mask
        if masks_flag:
            mask = np.array(masks[i]).flatten(order='C').astype(bool)
            ax.scatter(grid_points[mask,0], grid_points[mask,1], transform=ccrs.PlateCarree(), color=colors(i))

        # adding polygon label
        if labels_flag:
            center = (np.mean(lons), np.mean(lats))
            ax.text(center[0], center[1], s=str(i), color=colors(i), transform=ccrs.PlateCarree(), path_effects=[pe.withStroke(linewidth=4, foreground='k')])

    # snapping
    snap_cursor = SnappingCursor(ax, snap_grid_res)
    fig.canvas.mpl_connect('motion_notify_event', lambda event: snap_cursor.on_mouse_move(event, [], [], []))

    plt.show()

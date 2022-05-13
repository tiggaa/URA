from math import sin, cos, atan2, sqrt, radians
from wtforms import validators

_gridsys_to_inits = {} # add as go to avoid "X is not defined" here
_gridsys_to_funcs = {} # cache of loaded functions

def _load_gridsys(system):
    if _gridsys_to_funcs.get(system, False): return
    _gridsys_to_inits[system](_gridsys_to_funcs)

def _init_OSGB(lookup):
    from OSGridConverter import latlong2grid, grid2latlong
    def grid_to_latlong(gridref):
        l = grid2latlong(gridref)
        return (l.latitude,l.longitude)
    def grid_from_latlong(latlong):
        if latlong[0] == 200.0: return 'Transit'
        return str(latlong2grid(*latlong))
    def validate(form, field):
        try:
            grid_to_latlong(field.data)
        except Exception as e:
            raise validators.ValidationError(f"Not a valid OSGB Grid Reference: {e}")
    lookup['OSGB'] = {
        'to': grid_to_latlong,
        'from': grid_from_latlong,
        'validate': validate,
    }
_gridsys_to_inits['OSGB'] = _init_OSGB

def _init_MGRS(lookup):
    from mgrs import MGRS
    _m = MGRS() # singleton
    def grid_to_latlong(gridref):
        return _m.toLatLon(gridref)
    def grid_from_latlong(latlong):
        if latlong[0] == 200.0: return 'Transit'
        return _m.toMGRS(*latlong)
    def validate(form, field):
        try:
            grid_to_latlong(field.data)
        except Exception as e:
            raise validators.ValidationError(f"Not a valid MGRS Grid Reference: {e}")
    lookup['MGRS'] = {
        'to': grid_to_latlong,
        'from': grid_from_latlong,
        'validate': validate,
    }
_gridsys_to_inits['MGRS'] = _init_MGRS

def grid_to_latlong(system, grid):
    _load_gridsys(system)
    return _gridsys_to_funcs[system]['to'](grid)

def grid_from_latlong(system, latlong):
    _load_gridsys(system)
    return _gridsys_to_funcs[system]['from'](latlong)

# close over app as config might change after this function called
def grid_validate(app):
    def real_validate(form, field):
        system = app.config['RAPID_GRID_SYSTEM']
        _load_gridsys(system)
        return _gridsys_to_funcs[system]['validate'](form, field)
    return real_validate

def distance_between_points(latlong1, latlong2):
    """
    Calculate distance between two points using the Great Circle
    distance (Haversine approximation)

    To calculate distance between two points on a sphere
    Haversine Formula:
    Given point A at (lat1, lon1) and point B at (lat2, lon2),
    differences between longitudes (dlon) and latitudes (dlat)
    are converted to radians for use with the trigonometric functions:
    """
    lat1, lon1 = latlong1
    lat2, lon2 = latlong2
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    ##    Angle subtended at centre of the earth (a):
    a = (sin(dlat/2))**2 + (cos(radians(lat1)) * cos(radians(lat2)) * (sin(dlon/2))**2)
    ##    Corresponding distance at the surface of a unit sphere (c)
    c = 2 * atan2(sqrt(abs(a)), sqrt(1-abs(a)))
    ##    Forcing the earth to be a uniform sphere with radius 6371km,
    ##    Distance at the surface (distance):
    distance = 6371 * c
    return distance

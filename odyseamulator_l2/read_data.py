import datetime
import xarray
import logging
from typing import Optional

logger = logging.getLogger()
handler = logging.StreamHandler()
logger.addHandler(handler)

def load_model(path_model: str, start: datetime.datetime,
               end: datetime.datetime, dic_coord: Optional[dict] = {}
               ) -> xarray.Dataset:

    model = xarray.open_mfdataset(path_model, combine='by_coords',
                                  data_vars='different', coords='different',
                                  engine="netcdf4")
    #model.time.values.astype(float)
    if 'time_units' in dic_coord.keys():
        attrs = {'units': dic_coord['time_units']} #'days since 1950-01-01'}
        ntime = 'time'
        for key, value in dic_coord.items():
            if 'time' in value:
                ntime = key
        time = xarray.Dataset({ntime: (ntime, model[ntime].values, attrs)})
        time = xarray.decode_cf(time)
        model[ntime] = time[ntime].astype('datetime64[ns]')
        _ = dic_coord.pop('time_units')

    if len(dic_coord.keys()) > 0:
        for key, value in dic_coord.items():
            if 'lon' in value:
                model.coords[key] = (model.coords[key] + 180) % 360 - 180
        model = model.rename(name_dict=dic_coord)
    model = model.sortby(model.lon)
    strstart = datetime.datetime.strftime(start, '%Y-%m-%d')
    strend = datetime.datetime.strftime(end, '%Y-%m-%d')
    model = model.sel(time=slice(strstart, strend))
    logger.info(f'simulation for [{strstart}, {strend}] period')
    logger.debug(f'model starts at f{model["time"][0]}')
    return model


def convert_wind(model: xarray.Dataset, varu: Optional[str] = 'u_model',
                 varv: Optional[str] = 'v_model'):
    model['norm'] = numpy.sqrt(model[varu]**2 + model[varv]**2)
    model['direction'] = numpy.arctan2(model[varu]/model['norm'],
                                     model[varv]/model['norm'])
    model['direction'] = numpy.rad2deg(model['direction'])
    return model



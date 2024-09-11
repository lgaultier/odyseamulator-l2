import numpy
from typing import Optional, Tuple


def inversion(angle, uradial, dist: Optional[numpy.ndarray] = None,
              resol: Optional[numpy.ndarray] = 5000) -> Tuple[float, float]:
    H = numpy.zeros((len(angle), 2))
    H[:, 0] = numpy.cos(angle)
    H[:, 1] = numpy.sin(angle)
    if dist is not None:
        Ri = numpy.exp(-dist**2 / (0.5 * resol)**2)  # exp window
        RiH = numpy.tile(Ri, (2, 1)).T * H
    else:
        RiH = H
    M = numpy.dot(H.T, RiH)
    if not numpy.linalg.det(M):
        return None
    Mi = numpy.linalg.inv(M)
    eta_obs = numpy.dot(numpy.dot(Mi, RiH.T), uradial)
    return eta_obs


def perform_oi_on_l3(obs: dict, listkey: list, desc: Optional[bool] = False
                     ) -> dict:
    dic_out = {}
    for key in listkey:
        dic_out[f'{key}_northward'] = numpy.full(numpy.shape(obs[f'{key}_fore']),
                                          fill_value=numpy.nan)
        dic_out[f'{key}_eastward'] = numpy.full(numpy.shape(obs[f'{key}_fore']),
                                          fill_value=numpy.nan)
        # dic_out[key] = {'al': numpy.full(numpy.shape(obs[f'{key}_fore'])),
        #                'ac': numpy.full(numpy.shape(obs[f'{key}_fore']))}
    for i in range(len(obs['along_track'])):
        for j in range(len(obs['cross_track'])):
            rot = numpy.pi / 2
            obs_angle = [numpy.deg2rad(rot + obs['radial_angle_fore'][i, j]),
                         numpy.deg2rad(rot + obs['radial_angle_aft'][i, j])]
            for key in listkey:
                uradial = [obs[f'{key}_fore'][i, j], obs[f'{key}_aft'][i, j]]
                eta = inversion(obs_angle, uradial, dist=None)
                if eta is not None:
                    dic_out[f'{key}_northward'][i, j] = eta[1]
                    dic_out[f'{key}_eastward'][i, j] = eta[0]
    return dic_out

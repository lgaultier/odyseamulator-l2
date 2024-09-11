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


"""
def perform_oi_2(grd, obs, resol):
    # - In parameter file ## TODO -
    # Number of pixel (resolution for healpix)
    nside = 256
    # Number of diamonds for healpix
    ndiam = 12
    ntotpixel = nside * nside * ndiam
    # Conditionning threshold
    thresh_cond = 10
    ph = 2 * numpy.pi - numpy.deg2rad(lon)
    th = numpy.pi / 2 - numpy.deg2rad(lat)
    pidx = heal.ang2pix(nside, th, ph)

    for i in range(nbeam):
        for j in range(ndata):
            if ur[j, i] > -1E9:
                ip = pidx[j,i]
                # compute imulated model
                im[ip, 1] += u[j, i]
                im[ip, 2] += v[j,i]
                nim[ip] += 1
                # compute covariance(s) model
                co = numpy.cos(rangle[j,i])
                si = numpy.sin(rangle[j,i])
                w = ww[j,i]
                cov[ip, 0, 0] += co * co
                cov[ip, 1, 0] += si * co
                cov[ip, 0, 1] += si * co
                cov[ip, 1, 1] += si * si

                cov2[ip, 0, 0] += w * co * co
                cov2[ip, 1, 0] += w * si * co
                cov2[ip, 0, 1] += w * si * co
                cov2[ip, 1, 1] += w * si * si

                # compute data vector model
                vec[ip, 0] += co * ur[j,i]
                vec[ip, 1] += si * ur[j,i]

                # compute data noise vector model
                vec2[ip, 0] += w* co * uro[j,i]
                vec2[ip, 1] += w * si * uro[j,i]

                # compute doppler projection
                for k in range(3):
                    vecdop[k, ip, 0] += w * co * tdop[j,i,k]
                    vecdop[k, ip, 1] += w * si * tdop[j,i,k]
"""

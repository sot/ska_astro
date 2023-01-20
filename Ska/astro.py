# Licensed under a 3-clause BSD style license - see LICENSE.rst
import re
from math import floor

import ska_helpers

__version__ = ska_helpers.get_version(__name__)

class Equatorial(object):
    """Bare-bones class to get between decimal and sexigesimal representations of
    equatorial coordinates.

    Initialize an ``Equatorial`` object with any combination of string or
    numeric arguments that contain a total of either two or six numerical
    values.  Any separators in the list [,:dhms] are converted to <space>
    before splitting into numerical values.

    The following attributes will then be available:

    ================== =========================
    ra, dec            Decimal (0 <= ra < 360)
    ra0                RA (-180 < ra <= 180)
    ra_hms, dec_dms    Sexigesimal string
    rah, ram, ras      RA hour, min, sec
    decsign            Declination sign (+|-)
    decd, decm, decs   Declination deg, min, sec
    ================== =========================

    The sexigesimal delimiter is controlled by the ``delim`` attribute and is
    the colon character by default.

    Examples::

      >>> pos = ska_astro.Equatorial(123.4, "-34.12")
      >>> pos = ska_astro.Equatorial("12:01:02.34, -34:12:34.11")
      >>> pos = ska_astro.Equatorial("12 01 02.34", "-34d12m34.11s")
      >>> print(pos)
      RA, Dec = 180.25975, -34.2095 = 12:01:02.340, -34:12:34.11
      >>> pos.delim = " "
      >>> print(pos)
      RA, Dec = 180.25975, -34.2095 = 12 01 02.340, -34 12 34.11
    """
    def __init__(self, *args):
        self.delim = ':'
        argstr = ' '.join(str(x).strip() for x in args)
        argstr = re.sub(r'[,:dhms]', ' ', argstr)
        args = argstr.split()

        if len(args) == 2:
            ra, dec = [float(x) for x in args]
            ra = ra - floor(ra / 360.) * 360

            ra15 = ra / 15.
            rah = int(floor(ra15))
            ram = int(floor((ra15 - rah) * 60))
            ras = (ra15 - rah - ram / 60.) * 60 * 60

            decsign = '-' if dec < 0 else '+'
            absdec = abs(dec)
            decd = int(floor(absdec))
            decm = int(floor((absdec - decd) * 60))
            decs = (absdec - decd - decm / 60.) * 60 * 60

        elif len(args) == 6:
            rah = int(args[0])
            ram = int(args[1])
            ras = float(args[2])

            decsign = '-' if args[3].startswith('-') else '+'
            decd = abs(int(args[3]))
            decm = int(args[4])
            decs = float(args[5])

            ra = 15.0 * (rah + ram/60. + ras/3600.)
            dec = abs(decd) + decm/60. + decs/3600.
            if decsign == '-':
                dec = -dec
        else:
            raise ValueError('Input args %s does not have 2 or 6 values' % args)

        ra0 = ra - (360 if ra > 180 else 0)

        for attr in ('ra', 'dec', 'rah', 'ram', 'ras', 'decsign', 'decd', 'decm', 'decs', 'ra0'):
            setattr(self, attr, eval(attr))

    # Generate good sexigesimal strings.  Little bit tricky because of
    # floating point and rollover issues.  There is probably a better way...
    def get_ra_hms(self):
        ram, rah = self.ram, self.rah
        s_ras = "%06.3f" % self.ras
        if s_ras == '60.000':
            s_ras = '00.000'
            ram += 1
        s_ram = "%02d" % ram
        if s_ram == '60':
            s_ram = '00'
            rah += 1
        s_rah = "%02d" % rah
        if s_rah == '24':
            s_rah = '00'
        return self.delim.join([s_rah, s_ram, s_ras])
    ra_hms = property(get_ra_hms)

    def get_dec_dms(self):
        decm, decd = self.decm, self.decd
        s_decs = "%05.2f" % self.decs
        if s_decs == '60.00':
            s_decs = '00.00'
            decm += 1
        s_decm = "%02d" % decm
        if s_decm == '60':
            s_decm = '00'
            decd += 1
        s_decd = "%02d" % decd
        return self.decsign + self.delim.join([s_decd, s_decm, s_decs])

    dec_dms = property(get_dec_dms)

    def __str__(self):
        return 'RA, Dec = %.5f, %.4f = %s, %s' % (self.ra, self.dec,
                                                  self.ra_hms, self.dec_dms)

def sph_dist(a1, d1, a2, d2):
    """Calculate spherical distance between two sky positions.  Uses the haversine
    formula so accuracy degrades at distances near 180 degrees.

    The input coordinates can be either native python types (float, int) or
    numpy arrays.  The output will matchin the input type.

    >>> ska_astro.sph_dist(1, 2, 3, 4)
    2.8264172166623145
    >>> ska_astro.sph_dist(1, 2, np.array([1,2,3,4]), np.array([4,5,6,7]))
    array([ 2.        ,  3.16165191,  4.46977556,  5.82570185])

    :param a1: RA position 1 (deg)
    :param d1: dec position 1 (deg)
    :param a2: RA position 2 (deg)
    :param d2: dec position 2 (deg)

    :rtype: spherical distance (deg)
    """
    import numpy as np

    def haversine(theta):
        return np.sin(theta/2)**2

    ndarray = any(isinstance(x, np.ndarray) for x in (a1, d1, a2, d2))

    a1 = np.radians(a1)
    d1 = np.radians(d1)
    a2 = np.radians(a2)
    d2 = np.radians(d2)

    h = haversine(d1-d2) + np.cos(d1) * np.cos(d2) * haversine(a1-a2)
    h = np.where(abs(h) > 1.0, np.sign(h), h)
    dist = np.degrees(2 * np.arcsin(np.sqrt(h)))

    return (dist if ndarray else dist.tolist())

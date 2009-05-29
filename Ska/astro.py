import re
from math import floor

class Equatorial(object):
    """Bare-bones class to get between decimal and sexigesimal representations of
    equatorial coordinates.

    Initialize an ``Equatorial`` object with any combination of string or
    numeric arguments that contain a total of either two or six numerical
    values.  Any separators in the list [,:dhms] are converted to <space>
    before splitting into numerical values.
    
    The following attributes will then be available:

    ================== =========================
    ra, dec            decimal position
    rah, ram, ras      RA hour, min, sec
    decsign            Declination sign (+|-)
    decd, decm, decs   Declination deg, min, sec
    ================== =========================

    Examples::

      >>> pos = Equatorial(123.4, "-34.12")
      >>> pos = Equatorial("12:01:02.34, -34:12:34.11")
      >>> pos = Equatorial("12 01 02.34", "-34d12m34.11s")
    """
    def __init__(self, *args):
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

        for attr in ('ra', 'dec', 'rah', 'ram', 'ras', 'decsign', 'decd', 'decm', 'decs'):
            setattr(self, attr, eval(attr))

        self.ra_hms = "%02d:%02d:%06.3f" % (rah, ram, ras)
	self.dec_hms = "%s%02d:%02d:%05.2f" % (decsign, decd, decm, decs)

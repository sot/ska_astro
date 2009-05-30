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
    ra, dec            Decimal (0 <= ra < 360)
    ra0                RA (-180 < ra <= 180)
    ra_hms, dec_dms    Sexigesimal string
    rah, ram, ras      RA hour, min, sec
    decsign            Declination sign (+|-)
    decd, decm, decs   Declination deg, min, sec
    ================== =========================

    Examples::

      >>> pos = Ska.astro.Equatorial(123.4, "-34.12")
      >>> pos = Ska.astro.Equatorial("12:01:02.34, -34:12:34.11")
      >>> pos = Ska.astro.Equatorial("12 01 02.34", "-34d12m34.11s")
      >>> print pos
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

        ra0 = ra - (360 if ra > 180 else 0)

        for attr in ('ra', 'dec', 'rah', 'ram', 'ras', 'decsign', 'decd', 'decm', 'decs', 'ra0'):
            setattr(self, attr, eval(attr))

        # Generate good sexigesimal strings.  Little bit tricky because of
        # floating point and rollover issues.  There is probably a better way...
        s_ras = "%06.3f" % ras
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
        self.ra_hms = '%s:%s:%s' % (s_rah, s_ram, s_ras)

        s_decs = "%05.2f" % decs
        if s_decs == '60.00':
            s_decs = '00.00'
            decm += 1
        s_decm = "%02d" % decm
        if s_decm == '60':
            s_decm = '00'
            decd += 1
        s_decd = "%02d" % decd
	self.dec_dms = "%s%s:%s:%s" % (decsign, s_decd, s_decm, s_decs)

    def __str__(self):
        return 'RA, Dec = %.5f, %.4f = %s, %s' % (self.ra, self.dec, self.ra_hms, self.dec_dms)


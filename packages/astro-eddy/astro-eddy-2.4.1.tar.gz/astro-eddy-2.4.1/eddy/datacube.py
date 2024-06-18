# -*- coding: utf-8 -*-

import os
import numpy as np
from astropy.io import fits
import scipy.constants as sc
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator
import warnings

warnings.filterwarnings("ignore")


class datacube(object):
    """
    A ``datacube`` instance to read in data in a ``FITS`` format. This should
    contain all the functions to interact with a spectral line dataset.

    Args:
        path (str): Path to the datacube to load.
        FOV (Optional[float]): If specified, clip the data down to a
            square field of view with sides of `FOV` [arcsec].
        velocity_range (Optional[list]): A tuple or list of the minimum and
            maximum velocities in [m/s] to clip the data cube to.
        fill (Optional[float]): Replace all ``NaN`` values with this value.
        force_center (Optional[bool]): If ``True`` define the spatial axes such
            that they describe offset from the array center in [arcsec]. This
            is useful if the FITS header does not contain axis information.
    """

    flared_niter = 5
    shadowed_extend = 1.5
    shadowed_oversample = 2.0
    shadowed_method = 'nearest'

    msun = 1.98847e30
    fwhm = 2. * np.sqrt(2 * np.log(2))

    def __init__(self, path, FOV=None, velocity_range=None, fill=None,
                 force_center=False):

        # Read in the data

        self.path = path
        self._read_FITS(path=self.path,
                        fill=fill,
                        force_center=force_center)

        # Clip down the cube spatially and spectrally.

        if FOV is not None:
            self._clip_cube_spatial(FOV / 2.0, initial_load=True)
        if velocity_range is not None:
            self._clip_cube_velocity(*velocity_range)

    @property
    def rms(self):
        return self.estimate_cube_RMS()

    # -- PIXEL DEPROJECTION -- #

    def disk_coords(self, x0=0.0, y0=0.0, inc=0.0, PA=0.0, z0=None, psi=None,
                    r_cavity=0.0, r_taper=None, q_taper=1.0, z_func=None,
                    shadowed=False, outframe='cylindrical', flatten=False, **_):
        r"""
        Get the disk coordinates given certain geometrical parameters and an
        emission surface. The emission surface is most simply described as a
        power law profile,

        .. math::

            z(r) = z_0 \times \left(\frac{r}{1^{\prime\prime}}\right)^{\psi}

        where ``z0`` and ``psi`` can be provided by the user. For the case of
        a non-zero ``z0``, but ``psi=1``, we recover the conical surface
        described in Rosenfeld et al. (2013).

        With the increase in spatial resolution afforded by interferometers
        such as ALMA there are a couple of modifications that can be used to
        provide a better match to the data. For example, an inner cavity can be
        included with the ``r_cavity`` argument which makes the transformation:

        .. math::

            \tilde{r} = {\rm max}(0, r - r_{\rm cavity})

        Note that the inclusion of a cavity will mean that other parameters,
        such as ``z0``, would need to change as the radial axis has effectively
        been shifted.

        To account for the drop in emission surface in the outer disk where the
        gas surface density decreases there are two descriptions. The preferred
        way is to include an exponential taper to the power law profile,

        .. math::

            z_{\rm tapered}(r) = z(r) \times \exp\left( -\left[
            \frac{r}{r_{\rm taper}} \right]^{q_{\rm taper}} \right)

        where both ``r_taper`` and ``q_taper`` values must be set.

        If the emission surface is more complex than the analytical form
        described above, users may provide their own function, ``z_func``,
        which should return the emission height in [arcsec] for a midplane
        radius in [arcsec].

        For certain emission surfaces and high inclination disks, the
        transformation from on-sky coordinates to disk-frame coordinates can be
        hindered by the shadowing of certain regions of the disk. This is a
        particularly big problem if the emission surface is not monotonically
        increasing with radius. For some instances, the default deprojection
        algorithm will fail, and a more robust, albeit slower, algormith is
        needed. This can be turned on with ``shadowed=True``.

        As it is also possible to determine the rotation direction of the disk
        on the sky, we can encode this information in the sign of the
        inclination. A positive inclination describes a clockwise rotating
        disk, while a negative inclination describes an anti-clockwise rotating
        disk. For 2D disks, i.e., those without an emission surface, this will
        not make a difference, but for 3D disks, this will dictate the
        projection of the surface on the sky.

        Args:
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [degrees]. A positive
                inclination denotes a disk rotating clockwise on the sky, while
                a negative inclination represents a counter-clockwise rotation.
            PA (Optional[float]): Source position angle [degrees]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            r_taper (Optional[float]): Radius for tapered emission surface.
            q_taper (Optional[float]): Exponent for tapered emission surface.
            r_cavity (Optional[float]): Outer radius of a cavity. Within this
                region the emission surface is taken to be zero.
            z_func (Optional[callable]): A user-defined emission surface
                function that will return ``z`` in [arcsec] for a given ``r``
                in [arcsec]. This will override the analytical form.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust method for deprojecting pixel values.
            outframe (Optional[str]): Frame of reference for the returned
                coordinates. Either ``'cartesian'`` or ``'cylindrical'``.
            flatten (Optional[bool]): If ``True``, return flat arrays.

        Returns:
            array, array, array: Three coordinate arrays with ``(r, phi, z)``,
            in units of [arcsec], [radians], [arcsec], if
            ``frame='cylindrical'`` or ``(x, y, z)``, all in units of [arcsec]
            if ``frame='cartesian'``.
        """

        # Check the input variables.

        outframe = outframe.lower()
        if outframe not in ['cylindrical', 'cartesian']:
            raise ValueError("frame must be 'cylindrical' or 'cartesian'.")

        # Apply the inclination convention to be consistent with orbits.

        inc = inc if inc < 90.0 else inc - 180.0

        # Cycle through the different options for pixel deprojection.

        if z0 is None and z_func is None:
            r, t = self._get_midplane_polar_coords(x0, y0, inc, PA)
            z = np.zeros(r.shape)
        elif psi is None and z_func is None:
            r, t, z = self._get_conical_polar_coords(x0, y0, inc, PA, z0)
        else:
            if z_func is None:
                r_taper = np.inf if r_taper is None else r_taper
                def z_func(r_in):
                    r = np.clip(r_in - r_cavity, a_min=0.0, a_max=None)
                    return z0 * r**psi * np.exp(-np.power(r/r_taper, q_taper))
            if shadowed:
                r, t, z = self._get_shadowed_coords(x0, y0, inc, PA, z_func)
            else:
                r, t, z = self._get_flared_coords(x0, y0, inc, PA, z_func)

        # Return the values.

        if flatten:
            r = r.flatten()
            t = t.flatten()
            z = z.flatten()
        if outframe == 'cylindrical':
            return r, t, z
        return r * np.cos(t), r * np.sin(t), z

    def disk_to_sky(self, coords, x0=0.0, y0=0.0, inc=0.0, PA=0.0,
                    frame='cylindrical'):
        """
        Project disk-frame coordinates onto the cartesian sky plane.

        Args:
            coords (tuple): A tuple of the disk-frame coordinates to transform.
                Must be either cartestian, cylindrical or spherical frames,
                specified by the ``frame`` argument. If only two coordinates
                are given, the input is assumed to be 2D. All spatial
                coordinates should be given in [arcsec], while all angular
                coordinates should be given in [radians].
            x0 (Optional[float]): Source right ascension offset in [arcsec].
            y0 (Optional[float]): Source declination offset in [arcsec].
            inc (Optional[float]): Inclination of the disk in [deg].
            PA (Optional[float]): Position angle of the disk, measured Eastwards
                to the red-shifted major axis from North in [deg].
            frame (Optional[str]): Coordinate frame of the disk coordinates,
                either ``'cartesian'``, ``'cylindrical'`` or ``'spherical'``.

        Returns:
            Two arrays representing the projection of the input coordinates
            onto the sky, ``x_sky`` and ``y_sky``.
        """
        try:
            c1, c2, c3 = coords
        except ValueError:
            c1, c2 = coords
            c3 = np.zeros(c1.shape)
        if frame.lower() == 'cartesian':
            x = c1
            y = c2
            z = c3
        elif frame.lower() == 'cylindrical':
            x = c1 * np.cos(c2)
            y = c1 * np.sin(c2)
            z = c3
        elif frame.lower() == 'spherical':
            x = c1 * np.cos(c2) * np.sin(c3)
            y = c1 * np.sin(c2) * np.sin(c3)
            z = c1 * np.cos(c3)
        else:
            msg = "frame_in must be 'cartestian', 'cylindrical' or 'spherical'."
            raise ValueError(msg)
        inc = np.radians(inc)
        PA = -np.radians(PA + 90.0)
        y_roll = np.cos(inc) * y - np.sin(inc) * z
        x_sky = np.cos(PA) * x - np.sin(PA) * y_roll
        y_sky = np.sin(PA) * x + np.cos(PA) * y_roll
        return x_sky + x0, y_sky + y0

    def sky_to_disk(self, coords, x0=0.0, y0=0.0, inc=0.0, PA=0.0, z0=None,
                    psi=None, r_cavity=0.0, r_taper=None, q_taper=1.0,
                    z_func=None, shadowed=True, frame='cartesian',
                    griddata_kwargs=None):
        """
        Project sky-frame coordinates onto cylindrical disk-plane coordinates.
        Note that the azimuthal angle is returned in [degrees].

        Args:
            coords (tuple): A tuple of the sky-frame coordinates to transform.
                Must be either cartestian or polar frames,
                specified by the ``frame`` argument. If only two coordinates
                are given, the input is assumed to be 2D. All spatial
                coordinates should be given in [arcsec], while all angular
                coordinates should be given in [radians].
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [degrees]. A positive
                inclination denotes a disk rotating clockwise on the sky, while
                a negative inclination represents a counter-clockwise rotation.
            PA (Optional[float]): Source position angle [degrees]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            r_taper (Optional[float]): Radius for tapered emission surface.
            q_taper (Optional[float]): Exponent for tapered emission surface.
            r_cavity (Optional[float]): Outer radius of a cavity. Within this
                region the emission surface is taken to be zero.
            z_func (Optional[callable]): A user-defined emission surface
                function that will return ``z`` in [arcsec] for a given ``r``
                in [arcsec]. This will override the analytical form.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust method for deprojecting pixel values.
            frame (Optional[str]): Coordinate frame of the disk coordinates,
                either ``'cartesian'`` or ``'polar'``.
            griddata_kwargs (Optional[dict]): Kwargs to pass to
                ``scipy.interpolate.griddata``.

        Returns:
            array, array, array: The projection of the input coordinates into
                cylindrical disk-frame coordaintes, ``r_disk``, ``t_disk`` and
                ``z_disk`` in units of [arcesc], [degrees] and [arcsec],
                respectively.
        """

        # Unpack the desired points and convert them to cartesian form.

        msg = "Unknown `coords` format."
        coords = np.squeeze(coords)
        if coords.size > 2:
            if coords.shape[1] == 2:
                coords = coords.T
            elif coords.shape[0] != 2:
                raise ValueError(msg)
        elif coords.size != 2:
            raise ValueError(msg)
        
        if frame == 'polar':
            x = coords[0] * np.cos(np.radians(coords[1]))
            y = coords[0] * np.sin(np.radians(coords[1]))
        elif frame == 'cartesian':
            x = coords[0]
            y = coords[1]
        else:
            raise ValueError("Unknown `frame` value {}.".format(frame))

        # Generate the on-sky pixels.

        rvals, tvals, zvals = self.disk_coords(x0=x0,
                                               y0=y0,
                                               inc=inc,
                                               PA=PA,
                                               z0=z0,
                                               psi=psi,
                                               r_taper=r_taper,
                                               q_taper=q_taper,
                                               r_cavity=r_cavity,
                                               z_func=z_func,
                                               shadowed=shadowed,
                                               flatten=True)
        
        xvals, yvals, _ = self.disk_coords(x0=0.0,
                                           y0=0.0,
                                           inc=0.0,
                                           PA=0.0,
                                           outframe='cartesian',
                                           flatten=True)
        
        # Interpolate the locations and return.

        r = datacube._griddata(points=(xvals, yvals),
                               values=rvals,
                               xi=(x, y),
                               griddata_kwargs=griddata_kwargs)
        t = datacube._griddata(points=(xvals, yvals),
                               values=np.degrees(tvals),
                               xi=(x, y),
                               griddata_kwargs=griddata_kwargs)
        z = datacube._griddata(points=(xvals, yvals),
                               values=zvals,
                               xi=(x, y),
                               griddata_kwargs=griddata_kwargs)

        return r, t, z

    @staticmethod
    def _rotate_coords(x, y, PA):
        """Rotate (x, y) by PA [deg]."""
        x_rot = y * np.cos(np.radians(PA)) + x * np.sin(np.radians(PA))
        y_rot = x * np.cos(np.radians(PA)) - y * np.sin(np.radians(PA))
        return x_rot, y_rot

    @staticmethod
    def _deproject_coords(x, y, inc):
        """Deproject (x, y) by inc [deg]."""
        return x, y / np.cos(np.radians(inc))

    def _get_cart_sky_coords(self, x0, y0):
        """Return cartesian sky coordinates in [arcsec, arcsec]."""
        return np.meshgrid(self.xaxis - x0, self.yaxis - y0)

    def _get_midplane_cart_coords(self, x0, y0, inc, PA):
        """Return cartesian coordaintes of midplane in [arcsec, arcsec]."""
        x_sky, y_sky = self._get_cart_sky_coords(x0, y0)
        x_rot, y_rot = self._rotate_coords(x_sky, y_sky, PA)
        return datacube._deproject_coords(x_rot, y_rot, inc)

    def _get_midplane_polar_coords(self, x0, y0, inc, PA):
        """Return the polar coordinates of midplane in [arcsec, radians]."""
        x_mid, y_mid = self._get_midplane_cart_coords(x0, y0, inc, PA)
        return np.hypot(y_mid, x_mid), np.arctan2(y_mid, x_mid)

    def _get_conical_cart_coords(self, x0, y0, inc, PA, z0):
        """Return the cartesian coords of a conical surface."""
        inc = np.radians(inc)
        PA = np.radians(PA - 90.0)
        x_sky, y_sky = self._get_cart_sky_coords(x0, y0)
        x_rot = x_sky * np.cos(PA) - y_sky * np.sin(PA)
        y_rot = x_sky * np.sin(PA) + y_sky * np.cos(PA)
        psi = np.tan(z0)
        a = np.cos(2 * inc) + np.cos(2 * psi)
        b = -4.0 * np.sin(psi)**2 * y_rot * np.tan(inc)
        c = -2.0 * np.sin(psi)**2 * (x_rot**2 + y_rot**2 / np.cos(inc)**2)
        t = -b + np.sqrt(b**2 - 4 * a * c) / 2 / a
        x_d = x_rot
        y_d = y_rot / np.cos(inc) + t * np.sin(inc)
        z_d = z0 * np.hypot(x_d, y_d)
        return x_d, y_d, z_d

    def _get_conical_polar_coords(self, x0, y0, inc, PA, z0):
        """Return the cylindrical coords of a conical surface."""
        x_d, y_d, z_d = self._get_conical_cart_coords(x0, y0, inc, PA, z0)
        return np.hypot(y_d, x_d), np.arctan2(y_d, x_d), z_d

    def _get_flared_coords(self, x0, y0, inc, PA, z_func, w_func=None):
        """Return cyclindrical coords of surface in [arcsec, rad, arcsec]."""
        x_mid, y_mid = self._get_midplane_cart_coords(x0, y0, inc, PA)
        r_tmp, t_tmp = np.hypot(x_mid, y_mid), np.arctan2(y_mid, x_mid)
        for _ in range(self.flared_niter):
            y_tmp = y_mid + z_func(r_tmp) * np.tan(np.radians(inc))
            r_tmp = np.hypot(y_tmp, x_mid)
            t_tmp = np.arctan2(y_tmp, x_mid)
        return r_tmp, t_tmp, z_func(r_tmp)

    def _get_shadowed_coords(self, x0, y0, inc, PA, z_func, w_func=None):
        """
        Return cyclindrical coords of surface in [arcsec, rad, arcsec].
        """

        # Make the disk-frame coordinates.

        xdisk, ydisk, rdisk, tdisk = self._get_diskframe_coords()
        zdisk = z_func(rdisk)
        if w_func is not None:
            zdisk += w_func(rdisk, tdisk)

        # Incline the disk.

        inc = np.radians(inc)
        x_dep = xdisk
        y_dep = ydisk * np.cos(inc) - zdisk * np.sin(inc)

        # Remove shadowed pixels.
        # TODO: Check how this handles the bottom side of the disk.

        if inc < 0.0:
            y_dep = np.maximum.accumulate(y_dep, axis=0)
        else:
            y_dep = np.minimum.accumulate(y_dep[::-1], axis=0)[::-1]

        # Rotate and recenter the disk.

        x_rot, y_rot = self._rotate_coords(x_dep, y_dep, PA)
        x_rot, y_rot = x_rot + x0, y_rot + y0

        # Grid the disk.

        from scipy.interpolate import griddata
        disk = (x_rot.flatten(), y_rot.flatten())
        grid = (self.xaxis[None, :], self.yaxis[:, None])
        r_obs = griddata(disk, rdisk.flatten(), grid,
                         method=self.shadowed_method)
        t_obs = griddata(disk, tdisk.flatten(), grid,
                         method=self.shadowed_method)
        return r_obs, t_obs, z_func(r_obs)

    def _get_diskframe_coords(self):
        """Disk-frame coordinates based on the cube axes."""
        x_disk = np.linspace(self.shadowed_extend * self.xaxis[0],
                             self.shadowed_extend * self.xaxis[-1],
                             int(self.nxpix * self.shadowed_oversample))[::-1]
        y_disk = np.linspace(self.shadowed_extend * self.yaxis[0],
                             self.shadowed_extend * self.yaxis[-1],
                             int(self.nypix * self.shadowed_oversample))
        x_disk, y_disk = np.meshgrid(x_disk, y_disk)
        r_disk = np.hypot(x_disk, y_disk)
        t_disk = np.arctan2(y_disk, x_disk)
        return x_disk, y_disk, r_disk, t_disk
    
    def cartesian_deprojection(self, data, x0=0.0, y0=0.0, inc=0.0, PA=0.0,
                               z0=None, psi=None, r_taper=None, q_taper=1.0,
                               r_cavity=0.0, z_func=None, shadowed=False,
                               grid=None, griddata_kwargs=None):
        """
        Deproject the provided array into a face-on cartesian array.

        Args:
            data (array): Data to be deprojected. Must be the same shape as a
                channel of the attached data.
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [degrees]. A positive
                inclination denotes a disk rotating clockwise on the sky, while
                a negative inclination represents a counter-clockwise rotation.
            PA (Optional[float]): Source position angle [degrees]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            r_taper (Optional[float]): Radius for tapered emission surface.
            q_taper (Optional[float]): Exponent for tapered emission surface.
            r_cavity (Optional[float]): Outer radius of a cavity. Within this
                region the emission surface is taken to be zero.
            z_func (Optional[callable]): A user-defined emission surface
                function that will return ``z`` in [arcsec] for a given ``r``
                in [arcsec]. This will override the analytical form.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust method for deprojecting pixel values.
            grid (Optional[array]): Grid to define the axis of the deprojection.
            griddata_kwargs (Optional[dict]): Kwargs to pass to
                ``scipy.interpolate.griddata``. 

        Returns:
            array, array: The grid onto which the data is interpolated, and the
                interpolated data.
        """

        # Use the on-sky positions by default.

        if grid is None:
            grid = self.yaxis.copy()

        # Get the pixel coordinates.

        x, y, _ = self.disk_coords(x0=x0,
                                   y0=y0,
                                   inc=inc,
                                   PA=PA,
                                   z0=z0,
                                   psi=psi,
                                   r_taper=r_taper,
                                   q_taper=q_taper,
                                   r_cavity=r_cavity,
                                   z_func=z_func,
                                   shadowed=shadowed,
                                   outframe='cartesian',
                                   flatten=True)

        # Deproject onto a cartesian grid.

        gridded = datacube._griddata(points=(x, y),
                                     values=data.flatten(),
                                     xi=(grid[:, None], grid[None, :]),
                                     griddata_kwargs=griddata_kwargs)

        return grid, gridded

    def polar_deprojection(self, data, x0=0.0, y0=0.0, inc=0.0, PA=0.0,
                           z0=None, psi=None, r_taper=None, q_taper=1.0,
                           r_cavity=0.0, z_func=None, shadowed=False,
                           rgrid=None, tgrid=None, griddata_kwargs=None):
        """
        Deproject the provided data onto a polar grid.

        Args:
            data (array): Data to be deprojected. Must be the same shape as a
                channel of the attached data.
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [degrees]. A positive
                inclination denotes a disk rotating clockwise on the sky, while
                a negative inclination represents a counter-clockwise rotation.
            PA (Optional[float]): Source position angle [degrees]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            r_taper (Optional[float]): Radius for tapered emission surface.
            q_taper (Optional[float]): Exponent for tapered emission surface.
            r_cavity (Optional[float]): Outer radius of a cavity. Within this
                region the emission surface is taken to be zero.
            z_func (Optional[callable]): A user-defined emission surface
                function that will return ``z`` in [arcsec] for a given ``r``
                in [arcsec]. This will override the analytical form.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust method for deprojecting pixel values.
            rgrid (Optional[array]): Radial grid in [arcsec].
            tgrid (Optional[array]): Azimuthal grid in [degrees].
            griddata_kwargs (Optional[dict]): Kwargs to pass to
                ``scipy.interpolate.griddata``. 

        Returns:
            array, array, array: The radial and azimuthal grids onto which the
                data is interpolated, and the interpolated data.
        """

        # Set the default grids.

        if rgrid is None:
            rgrid = np.arange(0, self.xaxis.max(), self.dpix)
        if tgrid is None:
            tgrid = np.linspace(-np.pi, np.pi, self.xaxis.size)

        # Get the pixel coordinates.

        r, t, _ = self.disk_coords(x0=x0,
                                   y0=y0,
                                   inc=inc,
                                   PA=PA,
                                   z0=z0,
                                   psi=psi,
                                   r_taper=r_taper,
                                   q_taper=q_taper,
                                   r_cavity=r_cavity,
                                   z_func=z_func,
                                   shadowed=shadowed,
                                   outframe='cylindrical')
        
        # Deproject onto a polar grid.
        
        gridded = datacube._griddata(points=(r.flatten(), t.flatten()),
                                     values=data.flatten(),
                                     xi=(rgrid[None, :], tgrid[:, None]),
                                     griddata_kwargs=griddata_kwargs)

        return rgrid, tgrid, gridded

    @staticmethod
    def _griddata(points, values, xi, griddata_kwargs=None):
        """Wrapper for ``scipy.interpolate.griddata``."""
        from scipy.interpolate import griddata
        griddata_kwargs = {} if griddata_kwargs is None else griddata_kwargs
        griddata_kwargs['method'] = griddata_kwargs.pop('method', 'nearest')
        isfinite = np.isfinite(values)
        return griddata(points=(points[0][isfinite], points[1][isfinite]),
                        values=values[isfinite],
                        xi=xi,
                        **griddata_kwargs)

    # -- MASKING FUNCTIONS -- #

    def get_mask(self, r_min=None, r_max=None, exclude_r=False, phi_min=None,
                 phi_max=None, exclude_phi=False, abs_phi=False, x0=0.0,
                 y0=0.0, inc=0.0, PA=0.0, z0=0.0, psi=1.0, r_cavity=0.0,
                 r_taper=np.inf, q_taper=1.0, w_i=None, w_r=None, w_t=None,
                 z_func=None, shadowed=False, mask_frame='disk',
                 user_mask=None):
        """
        Returns a 2D mask for pixels in the given region. The mask can be
        specified in either disk-centric coordinates, ``mask_frame='disk'``,
        or on the sky, ``mask_frame='sky'``. If sky-frame coordinates are
        requested, the geometrical parameters (``inc``, ``PA``, ``z0``, etc.)
        are ignored, however the source offsets, ``x0``, ``y0``, are still
        considered.

        Args:
            r_min (Optional[float]): Minimum midplane radius of the annulus in
                [arcsec]. Defaults to minimum deprojected radius.
            r_max (Optional[float]): Maximum midplane radius of the annulus in
                [arcsec]. Defaults to the maximum deprojected radius.
            exclude_r (Optional[bool]): If ``True``, exclude the provided
                radial range rather than include.
            phi_min (Optional[float]): Minimum polar angle of the segment of
                the annulus in [deg]. Note this is the polar angle, not the
                position angle.
            phi_max (Optional[float]): Maximum polar angle of the segment of
                the annulus in [deg]. Note this is the polar angle, not the
                position angle.
            exclude_phi (Optional[bool]): If ``True``, exclude the provided
                polar angle range rather than include it.
            abs_phi (Optional[bool]): If ``True``, take the absolute value of
                the polar angle such that it runs from 0 [deg] to 180 [deg].
            x0 (Optional[float]): Source center offset along the x-axis in
                [arcsec].
            y0 (Optional[float]): Source center offset along the y-axis in
                [arcsec].
            inc (Optional[float]): Inclination of the disk in [degrees].
            PA (Optional[float]): Position angle of the disk in [degrees],
                measured east-of-north towards the redshifted major axis.
            z0 (Optional[float]): Emission height in [arcsec] at a radius of
                1".
            psi (Optional[float]): Flaring angle of the emission surface.
            z_func (Optional[function]): A function which provides
                :math:`z(r)`. Note that no checking will occur to make sure
                this is a valid function.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust, deprojection method for shadowed disks.

        Returns:
            A 2D array mask matching the shape of a channel.
        """

        # Check the requested frame.

        mask_frame = mask_frame.lower()
        if mask_frame not in ['disk', 'sky']:
            raise ValueError("mask_frame must be 'disk' or 'sky'.")
        if mask_frame == 'sky':
            inc = 0.0
            PA = 0.0

        # Calculate the deprojected pixel coordaintes.

        rvals, pvals = self.disk_coords(x0=x0, y0=y0, inc=inc, PA=PA, z0=z0,
                                        psi=psi, r_cavity=r_cavity,
                                        r_taper=r_taper, q_taper=q_taper,
                                        w_i=w_i, w_r=w_r, w_t=w_t,
                                        z_func=z_func, frame='cylindrical',
                                        shadowed=shadowed)[:2]
        pvals = abs(pvals) if abs_phi else pvals

        # Radial mask.

        r_min = np.nanmin(rvals) if r_min is None else r_min
        r_max = np.nanmax(rvals) if r_max is None else r_max
        if r_min >= r_max:
            raise ValueError("`r_min` must be smaller than `r_max`.")
        r_mask = np.logical_and(rvals >= r_min, rvals <= r_max)
        r_mask = ~r_mask if exclude_r else r_mask

        # Azimuthal mask.

        phi_min = np.nanmin(pvals) if phi_min is None else np.radians(phi_min)
        phi_max = np.nanmax(pvals) if phi_max is None else np.radians(phi_max)
        if phi_min >= phi_max:
            raise ValueError("`PA_min` must be smaller than `PA_max`.")
        phi_mask = np.logical_and(pvals >= phi_min, pvals <= phi_max)
        phi_mask = ~phi_mask if exclude_phi else phi_mask

        # Combine and return.

        mask = r_mask * phi_mask
        if np.sum(mask) == 0:
            raise ValueError("There are zero pixels in the mask.")
        if user_mask is not None:
            mask *= user_mask
        return mask

    # -- DATA I/O -- #

    def _read_FITS(self, path, fill=None, force_center=False):
        """Reads the data from the FITS file."""

        # File names.

        self.path = os.path.expanduser(path)
        self.fname = self.path.split('/')[-1]

        # Read in the data and, if necessary, fill the NaNs with default
        # values. Note that in the case of multiple data fields, we need to
        # think of something different.

        self.header = fits.getheader(path)
        self.data = np.squeeze(fits.getdata(self.path))
        if fill is not None:
            self.data = np.where(np.isfinite(self.data), self.data, fill)

        # Position axes. Two options here, either try to build the axis based
        # on the information in the header, or if force_center=True then return
        # an axis where the offset is relative to the image center

        if force_center:
            self.xaxis = self._forcepositionaxis(a=1)
            self.yaxis = self._forcepositionaxis(a=2)
        else:
            self.xaxis = self._readpositionaxis(a=1)
            self.yaxis = self._readpositionaxis(a=2)

        # Spectral axis.

        self.nu0 = self._readrestfreq()
        try:
            self.velax = self._readvelocityaxis()
            if self.velax.size > 1:
                self.chan = np.mean(np.diff(self.velax))
            else:
                self.chan = np.nan
            self.freqax = self._readfrequencyaxis()
            if self.chan < 0.0:
                self.data = self.data[::-1]
                self.velax = self.velax[::-1]
                self.freqax = self.freqax[::-1]
                self.chan *= -1.0
        except KeyError:
            self.velax = None
            self.chan = None
            self.freqax = None

        # Check that the data is saved such that increasing indices in x are
        # decreasing in offset counter to the yaxis.

        if np.diff(self.xaxis).mean() > 0.0:
            self.xaxis = self.xaxis[::-1]
            self.data = self.data[:, ::-1]

        # Read the beam properties.

        self._read_beam()

    def _read_beam(self):
        """Reads the beam properties from the header."""
        try:
            if self.header.get('CASAMBM', False):
                beam = fits.open(self.path)[1].data
                beam = np.median([b[:3] for b in beam.view()], axis=0)
                self.bmaj, self.bmin, self.bpa = beam
            else:
                self.bmaj = self.header['bmaj'] * 3600.
                self.bmin = self.header['bmin'] * 3600.
                self.bpa = self.header['bpa']
            self.beamarea_arcsec = self._calculate_beam_area_arcsec()
            self.beamarea_str = self._calculate_beam_area_str()
        except Exception:
            print("WARNING: No beam values found. Assuming pixel as beam.")
            self.bmaj = self.dpix
            self.bmin = self.dpix
            self.bpa = 0.0
            self.beamarea_arcsec = self.dpix**2.0
            self.beamarea_str = np.radians(self.dpix / 3600.)**2.0
        self.bpa %= 180.0

    def print_beam(self):
        """Print the beam properties."""
        print('{:.2f}" x {:.2f}" at {:.1f} deg'.format(*self.beam))

    @property
    def beam(self):
        """Returns beam properties."""
        return self.bmaj, self.bmin, self.bpa

    @property
    def beams_per_pix(self):
        """Number of beams per pixel."""
        return self.dpix**2.0 / self.beamarea_arcsec

    @property
    def pix_per_beam(self):
        """Number of pixels in a beam."""
        return self.beamarea_arcsec / self.dpix**2.0

    def _clip_cube_velocity(self, v_min=None, v_max=None):
        """Clip the cube to within ``vmin`` and ``vmax``."""
        if self.data.ndim == 2:
            raise ValueError("Attaced cube has no velocity axis.")
        v_min = self.velax[0] if v_min is None else v_min
        v_max = self.velax[-1] if v_max is None else v_max
        i = abs(self.velax - v_min).argmin()
        i += 1 if self.velax[i] < v_min else 0
        j = abs(self.velax - v_max).argmin()
        j -= 1 if self.velax[j] > v_max else 0
        self.velax = self.velax[i:j+1]
        self.data = self.data[i:j+1]

    def clip_cube_spatial(self, FOV):
        """Applies the new FOV."""
        if FOV > (self.xaxis.max() - self.xaxis.min()):
            raise ValueError("Cannot apply a larger FOV.")
        xa, xb, ya, yb = self._clip_cube_spatial(FOV / 2.0, False, True)
        self.data = self.data[ya:yb, xa:xb]
        self.error = self.error[ya:yb, xa:xb]
        self.mask = self.mask[ya:yb, xa:xb]
        self.xaxis = self.xaxis[xa:xb]
        self.yaxis = self.yaxis[ya:yb]

    def _clip_cube_spatial(self, radius, initial_load=True, indices=False):
        """Clip the cube plus or minus clip arcseconds from the origin."""
        if radius > min(self.xaxis.max(), self.yaxis.max()):
            print('WARNING: FOV = {:.1f}" larger than '.format(radius * 2)
                  + 'FOV of cube: {:.1f}".'.format(self.xaxis.max() * 2))
        else:
            if initial_load:
                self._original_shape = self.data.shape
            xa = abs(self.xaxis - radius).argmin()
            if self.xaxis[xa] < radius:
                xa -= 1
            xb = abs(self.xaxis + radius).argmin()
            if -self.xaxis[xb] < radius:
                xb += 1
            xb += 1
            ya = abs(self.yaxis + radius).argmin()
            if -self.yaxis[ya] < radius:
                ya -= 1
            yb = abs(self.yaxis - radius).argmin()
            if self.yaxis[yb] < radius:
                yb += 1
            yb += 1
            if initial_load:
                self._xa = xa
                self._xb = xb
                self._ya = ya
                self._yb = yb
            if indices:
                return xa, xb, ya, yb
            if self.data.ndim == 3:
                self.data = self.data[:, ya:yb, xa:xb]
            else:
                self.data = self.data[ya:yb, xa:xb]
            self.xaxis = self.xaxis[xa:xb]
            self.yaxis = self.yaxis[ya:yb]

    @property
    def nxpix(self):
        return self.xaxis.size

    @property
    def nypix(self):
        return self.yaxis.size

    @property
    def dpix(self):
        return np.diff(self.yaxis).mean()

    @property
    def nchan(self):
        if self.velax is not None:
            return self.velax.size
        return 0

    def _readspectralaxis(self, a):
        """Returns the spectral axis in [Hz] or [m/s]."""
        a_len = self.header['naxis%d' % a]
        a_del = self.header['cdelt%d' % a]
        a_pix = self.header['crpix%d' % a]
        a_ref = self.header['crval%d' % a]
        return a_ref + (np.arange(a_len) - a_pix + 1.0) * a_del

    def _readpositionaxis(self, a=1):
        """Returns the position axis in [arcseconds]."""
        if a not in [1, 2]:
            raise ValueError("'a' must be in [1, 2].")
        try:
            a_len = self.header['naxis%d' % a]
            a_del = self.header['cdelt%d' % a]
            a_pix = self.header['crpix%d' % a]
        except KeyError:
            if self._user_pixel_scale is None:
                print('WARNING: No axis information found.')
                _input = input("\t Enter pixel scale size in [arcsec]: ")
                self._user_pixel_scale = float(_input) / 3600.0
            a_len = self.data.shape[-1] if a == 1 else self.data.shape[-2]
            if a == 1:
                a_del = -1.0 * self._user_pixel_scale
            else:
                a_del = 1.0 * self._user_pixel_scale
            a_pix = a_len / 2.0 + 0.5
        axis = (np.arange(a_len) - a_pix + 1.0) * a_del
        axis = 3600.0 * a_del * (np.arange(a_len) - 0.5 * (a_len - 1.0))
        return axis

    def _forcepositionaxis(self, a=1):
        """Returns the axis in [arcsec] assuming image is centered."""
        if a not in [1, 2]:
            raise ValueError("'a' must be in [1, 2].")
        a_len = self.data.shape[-1] if a == 1 else self.data.shape[-2]
        axis = np.arange(a_len).astype('float') - a_len / 2.0
        axis += 0.5 * (abs(axis[0]) - abs(axis[-1]))
        return axis

    def _readrestfreq(self):
        """Read the rest frequency."""
        try:
            nu = self.header['restfreq']
        except KeyError:
            try:
                nu = self.header['restfrq']
            except KeyError:
                try:
                    nu = self.header['crval3']
                except KeyError:
                    nu = np.nan
        return nu

    def _readvelocityaxis(self):
        """Wrapper for _velocityaxis and _spectralaxis."""
        a = 4 if 'stokes' in self.header['ctype3'].lower() else 3
        if 'freq' in self.header['ctype%d' % a].lower():
            specax = self._readspectralaxis(a)
            velax = (self.nu0 - specax) * sc.c
            velax /= self.nu0
        else:
            velax = self._readspectralaxis(a)
        return velax

    def _readfrequencyaxis(self):
        """Returns the frequency axis in [Hz]."""
        a = 4 if 'stokes' in self.header['ctype3'].lower() else 3
        if 'freq' in self.header['ctype3'].lower():
            return self._readspectralaxis(a)
        return self._readrestfreq() * (1.0 - self._readvelocityaxis() / sc.c)

    def force_relative_offset_axes(self):
        """Force the use of relative offset axes."""
        dx = (self.xaxis.max() - self.xaxis.min()) / 2.0
        self.xaxis = np.linspace(dx, -dx, self.xaxis.size)
        dy = (self.yaxis.max() - self.yaxis.min()) / 2.0
        self.yaxis = np.linspace(-dy, dy, self.yaxis.size)

    # -- UNIT CONVERSIONS -- #

    def jybeam_to_Tb_RJ(self, data=None, nu=None):
        """[Jy/beam] to [K] conversion using Rayleigh-Jeans approximation."""
        nu = self.nu0 if nu is None else nu
        data = self.data if data is None else data
        jy2k = 1e-26 * sc.c**2 / nu**2 / 2. / sc.k
        return jy2k * data / self._calculate_beam_area_str()

    def jybeam_to_Tb(self, data=None, nu=None):
        """[Jy/beam] to [K] conversion using the full Planck law."""
        nu = self.nu0 if nu is None else nu
        data = self.data if data is None else data
        Tb = 1e-26 * abs(data) / self._calculate_beam_area_str()
        Tb = 2.0 * sc.h * nu**3 / Tb / sc.c**2
        Tb = sc.h * nu / sc.k / np.log(Tb + 1.0)
        return np.where(data >= 0.0, Tb, -Tb)

    def Tb_to_jybeam_RJ(self, data=None, nu=None):
        """[K] to [Jy/beam] conversion using Rayleigh-Jeans approxmation."""
        nu = self.nu0 if nu is None else nu
        data = self.data if data is None else data
        jy2k = 1e-26 * sc.c**2 / nu**2 / 2. / sc.k
        return data * self._calculate_beam_area_str() / jy2k

    def Tb_to_jybeam(self, data=None, nu=None):
        """[K] to [Jy/beam] conversion using the full Planck law."""
        nu = self.nu0 if nu is None else nu
        data = self.data if data is None else data
        Fnu = 2. * sc.h * nu**3 / sc.c**2
        Fnu /= np.exp(sc.h * nu / sc.k / abs(data)) - 1.0
        Fnu *= self._calculate_beam_area_str() / 1e-26
        return np.where(data >= 0.0, Fnu, -Fnu)

    # -- BEAM FUNCTIONS -- #

    def _calculate_beam_area_arcsec(self):
        """Beam area in square arcseconds."""
        omega = self.bmin * self.bmaj
        if self.bmin == self.dpix and self.bmaj == self.dpix:
            return omega
        return np.pi * omega / 4. / np.log(2.)

    def _calculate_beam_area_str(self):
        """Beam area in steradians."""
        omega = np.radians(self.bmin / 3600.)
        omega *= np.radians(self.bmaj / 3600.)
        if self.bmin == self.dpix and self.bmaj == self.dpix:
            return omega
        return np.pi * omega / 4. / np.log(2.)

    def _beamkernel(self):
        """Returns the 2D Gaussian kernel for convolution."""
        from astropy.convolution import Gaussian2DKernel
        bmaj = self.bmaj / self.dpix / self.fwhm
        bmin = self.bmin / self.dpix / self.fwhm
        return Gaussian2DKernel(bmin, bmaj, np.radians(self.bpa))

    @staticmethod
    def _convolve_image(image, kernel, fast=True):
        """Convolve the image with the provided kernel."""
        if fast:
            from astropy.convolution import convolve_fft
            return convolve_fft(image, kernel, preserve_nan=True)
        from astropy.convolution import convolve
        return convolve(image, kernel, preserve_nan=True)

    # -- DIAGNOSTIC FUNCTIONS -- #

    def estimate_cube_RMS(self, N=10, r_in=0.0, r_out=1e10):
        """
        Estimate RMS of the cube based on first and last `N` channels and a
        circular area described by an inner and outer radius.

        Args:
            N (int): Number of edge channels to include.
            r_in (float): Inner edge of pixels to consider in [arcsec].
            r_out (float): Outer edge of pixels to consider in [arcsec].

        Returns:
            RMS (float): The RMS based on the requested pixel range.
        """
        r_dep = np.hypot(self.xaxis[None, :], self.yaxis[:, None])
        rmask = np.logical_and(r_dep >= r_in, r_dep <= r_out)
        rms = np.concatenate([self.data[:int(N)], self.data[-int(N):]])
        rms = np.where(rmask[None, :, :], rms, np.nan)
        return np.sqrt(np.nansum(rms**2) / np.sum(np.isfinite(rms)))

    def integrated_spectrum(self, x0=0.0, y0=0.0, inc=0.0, PA=0.0, r_min=None,
                            r_max=None):
        """
        Returns the integrated spectrum over a specified region.

        Args:
            x0 (Optional[float]): Right Ascension offset in [arcsec].
            y0 (Optional[float]): Declination offset in [arcsec].
            inc (Optional[float]): Disk inclination in [deg].
            PA (Optional[float]): Disk position angle in [deg].
            r_min (Optional[float]): Radius to integrate out from in [arcsec].
            r_max (Optional[float]): Radius to integrate out to in [arcsec].

        Returns:
            spectrum, uncertainty (array, array): Something about these.
        """
        rr = self.disk_coords(x0=x0, y0=y0, inc=inc, PA=PA)[0]
        r_max = rr.max() if r_max is None else r_max
        r_min = 0.0 if r_min is None else r_min
        mask = np.logical_and(rr <= r_max, rr >= r_min)
        nbeams = np.where(mask, 1, 0).sum() / self.pix_per_beam
        spectrum = np.array([np.nansum(c[mask]) for c in self.data])
        spectrum *= self.beams_per_pix
        uncertainty = np.sqrt(nbeams) * self.estimate_cube_RMS()
        return spectrum, uncertainty

    def _independent_samples(self, beam_spacing, rvals, pvals, dvals, xsky,
            ysky, jidx, iidx):
        """
        Returns spatially independent samples.

        Args:
            beam_spacing (int): Sample pixels separated by roughly
            `beam_spacing * bmaj` in azimuthal distance.
            rvals (ndarray): Array of radial values in [arcsec].
            pvals (ndarray): Array of polar angles in [radians].
            dvals (ndarray): Array of data values.
            xsky (ndarray): On-sky x-offset in [arcsec] of each pixel.
            ysky (ndarray): On-sky y-offset in [arcsec] of each pixel.
            jidx (ndarray): j-index of the original data array (y-axis).
            iidx (ndarray): i-index of the original data array (x-axis).

        Returns:
            rvals, pvals, dvals (array, array, array): A subsample of the   
                provided arrays, ordered in increasing `pvals`.
        """

        if not beam_spacing:
            return rvals, pvals, dvals, xsky, ysky, jidx, iidx

        # Order pixels and arrays in increasing phi.

        idxs = np.argsort(pvals)
        dvals = dvals[idxs]
        pvals = pvals[idxs]
        rvals = rvals[idxs]
        xsky = xsky[idxs]
        ysky = ysky[idxs]
        jidx = jidx[idxs]
        iidx = iidx[idxs]

        # Calculate the sampling rate.

        sampling = float(beam_spacing) * self.bmaj
        sampling /= np.mean(rvals) * np.median(np.diff(pvals))
        sampling = np.floor(sampling).astype('int')

        # If the sampling rate is above 1, start at a random location in
        # the array and sample at this rate, otherwise don't sample. This
        # happens at small radii, for example.

        if sampling > 1:
            start = np.random.randint(0, pvals.size)
            dvals = np.vstack([dvals[start:], dvals[:start]])
            pvals = np.concatenate([pvals[start:], pvals[:start]])
            rvals = np.concatenate([rvals[start:], rvals[:start]])
            xsky = np.concatenate([xsky[start:], xsky[:start]])
            ysky = np.concatenate([ysky[start:], ysky[:start]])
            jidx = np.concatenate([jidx[start:], jidx[:start]])
            iidx = np.concatenate([iidx[start:], iidx[:start]])
            dvals = dvals[::sampling]
            pvals = pvals[::sampling]
            rvals = rvals[::sampling]
            xsky = xsky[::sampling]
            ysky = ysky[::sampling]
            jidx = jidx[::sampling]
            iidx = iidx[::sampling]
        else:
            print("Pixels appear to be close to spatially independent.")

        return rvals, pvals, dvals, xsky, ysky, jidx, iidx
    
    def velocity_to_restframe_frequency(self, velax=None, vlsr=0.0):
        """Return restframe frequency [Hz] of the given velocity [m/s]."""
        velax = self.velax if velax is None else np.squeeze(velax)
        return self.nu0 * (1. - (velax - vlsr) / 2.998e8)

    def restframe_frequency_to_velocity(self, nu, vlsr=0.0):
        """Return velocity [m/s] of the given restframe frequency [Hz]."""
        return 2.998e8 * (1. - nu / self.nu0) + vlsr
    
    def spectral_resolution(self, dV=None):
        """Convert velocity resolution in [m/s] to [Hz]."""
        dV = dV if dV is not None else self.chan
        nu = self.velocity_to_restframe_frequency(velax=[-dV, 0.0, dV])
        return np.mean([abs(nu[1] - nu[0]), abs(nu[2] - nu[1])])
    
    # -- GENERAL ANALYSIS FUNCTIONS -- #

    def _beam_mask(self, x, y, threshold=0.5, stretch=1.0, response=False):
        """
        Returns a 2D Gaussian mask based on the attached beam centered at
        (x, y) on the sky.

        Args:
            x (flaot): RA offset of the center of the beam.
            y (float): Dec offset of the center of the beam.
            threshold (Optional[float]): Threshold beam power to consider a
                pixel within the beam. Default is 0.5.
            stretch (Optional[float]): Stretch the beam by this factor. A
                `stretch=2` will result in a beam mask that is twice as large
                as the attached beam.
            response (Optional[bool]): If ``True``, return the beam response
                function rather than a boolean mask.

        Returns:
            beammask (arr): 2D boolean array of pixels covered by the beam if
            ``response=False``, the default, otherwise a 2D array of the beam
            response function centered at that location.
        """
        xx, yy = np.meshgrid(self.xaxis - x, self.yaxis - y)
        theta = -np.radians(self.bpa)
        std_x = 0.5 * stretch * self.bmin / np.sqrt(np.log(2.0))
        std_y = 0.5 * stretch * self.bmaj / np.sqrt(np.log(2.0))
        a = np.cos(theta)**2 / std_x**2 + np.sin(theta)**2 / std_y**2
        b = np.sin(2*theta) / std_x**2 - np.sin(2*theta) / std_y**2
        c = np.sin(theta)**2 / std_x**2 + np.cos(theta)**2 / std_y**2
        f = np.exp(-(a*xx**2 + b*xx*yy + c*yy**2))
        return f if response else f >= threshold

    def radial_sampling(self, rbins=None, rvals=None, dr=None):
        """
        Return bins and bin center values. If the desired bin edges are known,
        will return the bin edges and vice versa. If neither are known will
        return default binning with the desired spacing.

        Args:
            rbins (Optional[list]): List of bin edges.
            rvals (Optional[list]): List of bin centers.
            dr (Optional[float]): Spacing of bin centers in [arcsec]. Defaults
                to a quarter of the beam major axis.

        Returns:
            rbins (list): List of bin edges.
            rpnts (list): List of bin centres.
        """
        if rbins is not None and rvals is not None:
            raise ValueError("Specify only 'rbins' or 'rvals', not both.")
        if rvals is not None:
            try:
                dr = np.diff(rvals)[0] * 0.5
            except IndexError:
                if self.dpix == self.bmaj:
                    dr = 2.0 * self.dpix
                else:
                    dr = self.bmaj / 4.0
            rbins = np.linspace(rvals[0] - dr, rvals[-1] + dr, len(rvals) + 1)
        if rbins is not None:
            rvals = np.average([rbins[1:], rbins[:-1]], axis=0)
        else:
            if dr is None:
                if self.dpix == self.bmaj:
                    dr = 2.0 * self.dpix
                else:
                    dr = self.bmaj / 4.0
            rbins = np.arange(0, self.xaxis.max(), dr)
            rvals = np.average([rbins[1:], rbins[:-1]], axis=0)
        return rbins, rvals

    def radial_profile(self, rbins=None, rvals=None, dr=None, x0=0.0, y0=0.0,
            inc=0.0, PA=0.0, z0=None, psi=None, r_cavity=0.0, r_taper=None,
            q_taper=1.0, z_func=None, shadowed=False, data=None,
            assume_correlated=True, percentiles=False):
        """
        Make an azimuthally averaged radial profile from the data.

        Args:
            rbins (Optional[list]): List of bin edges.
            rvals (Optional[list]): List of bin centers.
            dr (Optional[float]): Spacing of bin centers in [arcsec]. Defaults
                to a quarter of the beam major axis.
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [degrees]. A positive
                inclination denotes a disk rotating clockwise on the sky, while
                a negative inclination represents a counter-clockwise rotation.
            PA (Optional[float]): Source position angle [degrees]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            r_taper (Optional[float]): Radius for tapered emission surface.
            q_taper (Optional[float]): Exponent for tapered emission surface.
            r_cavity (Optional[float]): Outer radius of a cavity. Within this
                region the emission surface is taken to be zero.
            z_func (Optional[callable]): A user-defined emission surface
                function that will return ``z`` in [arcsec] for a given ``r``
                in [arcsec]. This will override the analytical form.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust method for deprojecting pixel values.
            data (Optional[array]): Data to calculate a radial profile of. If
                not provided, will use the attached dataset.
            assumed_correlated (Optional[bool]): If ``True``, take into account
                the beam size in calculating the uncertainty on the radial
                profile.
            percentiles (Optional[bool]): If ``True``, use the 16th, 50th and
                84th percentiles to define the profile and uncertainties.
                Otherwise use the mean and standard deviation.

        Returns:
            Three 1D arrays with ``x``, ``y`` and ``dy`` for plotting.
        """

        # Select the data to use. Defaults to attached data if not provided.

        data = self.data if data is None else data
        assert data.ndim == 2, "Can only provide radial profiles for 2D data."

        # Get the radial sampling.

        rbins, rvals = self.radial_sampling(rbins=rbins,
                                            rvals=rvals,
                                            dr=dr)

        # Calculate the deprojected pixel values.

        rpnts, _, _ = self.disk_coords(x0=x0, 
                                       y0=y0,
                                       inc=inc,
                                       PA=PA,
                                       z0=z0,
                                       psi=psi,
                                       r_cavity=r_cavity,
                                       r_taper=r_taper,
                                       q_taper=q_taper,
                                       z_func=z_func,
                                       shadowed=shadowed,
                                       flatten=True)
        
        # Calculate the radial profile.

        if assume_correlated:
            nbeams = 2.0 * np.pi * rvals / self.bmaj
        else:
            nbeams = 1.0

        # Radial binning.

        toavg = data.flatten()
        assert toavg.size == rpnts.size
        ridxs = np.digitize(rpnts, rbins)

        # Averaging.

        if percentiles:
            rstat = np.array([np.nabpercentile(toavg[ridxs == r], [16, 50, 84])
                              for r in range(1, rbins.size)]).T
            ravgs = rstat[1]
            rstds = np.array([rstat[1] - rstat[0], rstat[2] - rstat[1]])
            rstds /= np.sqrt(nbeams)[None, :]
        else:
            ravgs = np.array([np.nanmean(toavg[ridxs == r])
                              for r in range(1, rbins.size)])
            rstds = np.array([np.nanstd(toavg[ridxs == r])
                              for r in range(1, rbins.size)])
            rstds /= np.sqrt(nbeams)

        # Return.

        return rvals, ravgs, rstds

    def background_residual(self, rbins=None, rvals=None, dr=None, x0=0.0,
            y0=0.0, inc=0.0, PA=0.0, z0=None, psi=None, r_cavity=0.0,
            r_taper=None, q_taper=1.0, z_func=None, shadowed=False, data=None,
            return_background=False):
        """
        Subtract an azimuthally averaged residual from the data to highlight
        residuals.

        Args:
            rbins (Optional[list]): List of bin edges.
            rvals (Optional[list]): List of bin centers.
            dr (Optional[float]): Spacing of bin centers in [arcsec]. Defaults
                to a quarter of the beam major axis.
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [degrees]. A positive
                inclination denotes a disk rotating clockwise on the sky, while
                a negative inclination represents a counter-clockwise rotation.
            PA (Optional[float]): Source position angle [degrees]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            r_taper (Optional[float]): Radius for tapered emission surface.
            q_taper (Optional[float]): Exponent for tapered emission surface.
            r_cavity (Optional[float]): Outer radius of a cavity. Within this
                region the emission surface is taken to be zero.
            z_func (Optional[callable]): A user-defined emission surface
                function that will return ``z`` in [arcsec] for a given ``r``
                in [arcsec]. This will override the analytical form.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust method for deprojecting pixel values.
            data (Optional[array]): Data to calculate a radial profile of. If
                not provided, will use the attached dataset.
            return_background (Optional[bool]): If ``True``, return the modeled
                background rather than the residual.
                
        Returns:
            background (array): The residuals after subtracted an azimuthally
                symmetric background, or the modeled background if
                ``return_background=True``.

        """
        from scipy.interpolate import interp1d

        # Calculate the deprojected pixel values.

        rpnts, _, _ = self.disk_coords(x0=x0, 
                                       y0=y0,
                                       inc=inc,
                                       PA=PA,
                                       z0=z0,
                                       psi=psi,
                                       r_cavity=r_cavity,
                                       r_taper=r_taper,
                                       q_taper=q_taper,
                                       z_func=z_func,
                                       shadowed=shadowed,
                                       flatten=False)
        
        # Calculate the radial profile. Note here we already define what the
        # data array is such that we can subtract the model from it later.

        data = self.data if data is None else data
        x, y, _ = self.radial_profile(rbins=rbins,
                                      rvals=rvals,
                                      dr=dr,
                                      x0=x0, 
                                      y0=y0,
                                      inc=inc,
                                      PA=PA,
                                      z0=z0,
                                      psi=psi,
                                      r_cavity=r_cavity,
                                      r_taper=r_taper,
                                      q_taper=q_taper,
                                      z_func=z_func,
                                      shadowed=shadowed,
                                      data=data)
        
        # Calculate the background model and return if necessary.

        background = interp1d(x, y, bounds_error=False)(rpnts)
        if return_background:
            return background
        
        # Calculate the residual and return.

        residual = data - background
        return residual

    # -- PLOTTING FUNCTIONS -- #

    @staticmethod
    def cmap():
        import matplotlib.colors as mcolors
        c2 = plt.cm.Reds(np.linspace(0, 1, 16))
        c1 = plt.cm.Blues_r(np.linspace(0, 1, 16))
        colors = np.vstack((c1, np.ones((2, 4)), c2))
        return mcolors.LinearSegmentedColormap.from_list('eddymap', colors)

    @property
    def extent(self):
        """Cube field of view for use with Matplotlib's ``imshow``."""
        return [self.xaxis[0]+self.dpix/2.0, self.xaxis[-1]-self.dpix/2.0,
                self.yaxis[0]-self.dpix/2.0, self.yaxis[-1]+self.dpix/2.0]

    @property
    def FOV(self):
        """Cube field of view."""
        xFOV = self.xaxis[0] - self.xaxis[-1]
        yFOV = self.yaxis[-1] - self.yaxis[0]
        return np.mean([xFOV, yFOV])

    def extent_au(self, dist=1.0):
        """Cube field of view in [au] for use with Matplotlib's ``imshow``."""
        return dist * np.squeeze(self.extent)

    def plot_beam(self, ax, x0=0.1, y0=0.1, **kwargs):
        """Plot the sythensized beam on the provided axes."""
        from matplotlib.patches import Ellipse
        beam = Ellipse(ax.transLimits.inverted().transform((x0, y0)),
                       width=self.bmin, height=self.bmaj, angle=-self.bpa,
                       fill=kwargs.get('fill', False),
                       hatch=kwargs.get('hatch', '//////////'),
                       lw=kwargs.get('linewidth', kwargs.get('lw', 1)),
                       color=kwargs.get('color', kwargs.get('c', 'k')),
                       zorder=kwargs.get('zorder', 1000))
        ax.add_patch(beam)

    def _gentrify_plot(self, ax):
        """Gentrify the plot with a grid, label axes and a beam."""
        ax.set_aspect(1)
        ax.grid(ls='--', color='k', alpha=0.2, lw=0.5)
        ax.tick_params(which='both', right=True, top=True)
        ax.set_xlim(self.xaxis.max(), self.xaxis.min())
        ax.set_ylim(self.yaxis.min(), self.yaxis.max())
        ax.xaxis.set_major_locator(MaxNLocator(5, min_n_ticks=3))
        ax.yaxis.set_major_locator(MaxNLocator(5, min_n_ticks=3))
        ticks = np.diff(ax.xaxis.get_majorticklocs()).mean() / 5.0
        ax.xaxis.set_minor_locator(MultipleLocator(ticks))
        ax.yaxis.set_minor_locator(MultipleLocator(ticks))
        ax.set_xlabel('Offset (arcsec)')
        ax.set_ylabel('Offset (arcsec)')
        if self.bmaj is not None:
            self.plot_beam(ax=ax)

    def plot_maximum(self, ax=None, imshow_kwargs=None, return_fig=False):
        """
        Plot the maximum value along each spectrum.

        Args:
            ax (Optional[matplotlib axis]): Axis used for the plotting.
            imshow_kwargs (Optional[dict]): Kwargs to pass to
                ``matplotlib.imshow``.
            return_fig (Optional[bool]): Whether to return the figure instance.
                If an axis was provided, this will always be ``False``.

        Returns:
            fig (matplotlib figure): If ``return_fig=True``, will return the
                figure for continued plotting.
        """

        # Dummy axis to overplot.

        if ax is None:
            fig, ax = plt.subplots()
        else:
            return_fig = False

        # Collapse the data.

        dmax = np.nanmax(self.data, axis=0)
        vmax = np.percentile(dmax, [98])

        # Imshow defaults and plot the figure.

        imshow_kwargs = {} if imshow_kwargs is None else imshow_kwargs
        imshow_kwargs['interpolation'] = 'nearest'
        imshow_kwargs['extent'] = self.extent
        imshow_kwargs['origin'] = 'lower'
        imshow_kwargs['cmap'] = imshow_kwargs.pop('cmap', 'turbo')
        imshow_kwargs['vmin'] = imshow_kwargs.pop('vmin', 0.0)
        imshow_kwargs['vmax'] = imshow_kwargs.pop('vmax', vmax)

        im = ax.imshow(dmax, **imshow_kwargs)
        cb = plt.colorbar(im, ax=ax, pad=0.03, extend='both')
        cb.set_label('Peak Intensity (Jy/beam)', rotation=270, labelpad=13)
        cb.minorticks_on()
        self._gentrify_plot(ax=ax)

        # Returns

        if return_fig:
            return fig

    def plot_surface(self, x0=0.0, y0=0.0, inc=0.0, PA=0.0, z0=None, psi=None,
                     r_cavity=None, r_taper=None, q_taper=None, w_i=None,
                     w_r=None, w_t=None, z_func=None, w_func=None,
                     shadowed=False, r_max=None, mask=None, fill=None, ax=None,
                     contour_kwargs=None, imshow_kwargs=None, return_fig=True,
                     **_):
        """
        Overplot the emission surface onto the provided axis.

        Args:
            ax (Optional[AxesSubplot]): Axis to plot onto.
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [deg].
            PA (Optional[float]): Source position angle [deg]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            z1 (Optional[float]): Aspect ratio correction term at 1" for the
                emission surface. Should be opposite sign to z0.
            phi (Optional[float]): Flaring angle correction term for the
                emission surface.
            w_i (Optional[float]): Warp inclination in [degrees] at the disk
                center.
            w_r (Optional[float]): Scale radius of the warp in [arcsec].
            w_t (Optional[float]): Angle of nodes of the warp in [degrees].
            r_max (Optional[float]): Outer radius to plot.
            mask (Optional[array]): A 2D mask to define where the surcace is
                plotted.
            ntheta (Optional[int]): Number of theta contours to plot.
            nrad (Optional[int]): Number of radial contours to plot.
            mask (Optional[array]): Mask used to define regions where the
                surface should be plot. If not provided, will plot everywhere.
            check_mask (Optional[bool]): Mask regions which are like projection
                errors for highly flared surfaces.

        Returns:
            ax (AxesSubplot): Axis with the contours overplotted.
        """

        # Dummy axis to overplot.

        if ax is None:
            fig, ax = plt.subplots()
        else:
            return_fig = False

        rvals, tvals, zvals = self.disk_coords(x0=x0, y0=y0,
                                               inc=inc, PA=PA,
                                               z0=z0, psi=psi,
                                               r_cavity=r_cavity,
                                               r_taper=r_taper,
                                               q_taper=q_taper,
                                               w_i=w_i, w_r=w_r, w_t=w_t,
                                               z_func=z_func,
                                               w_func=w_func,
                                               shadowed=shadowed)

        # Mask the data based on r_max.

        r_max = np.nanmax(rvals) if r_max is None else r_max
        zvals = np.where(rvals <= r_max, zvals, np.nan)
        tvals = np.where(rvals <= r_max, tvals, np.nan)
        tvals = np.where(rvals >= 0.5 * self.bmaj, tvals, np.nan)
        rvals = np.where(rvals <= r_max, rvals, np.nan)

        # Mask the data based on user-defined mask.

        if mask is not None:
            rvals = np.where(mask, rvals, np.nan)
            tvals = np.where(mask, tvals, np.nan)
            zvals = np.where(mask, zvals, np.nan)

        # Fill in the background.

        if fill is not None:
            kw = {} if imshow_kwargs is None else imshow_kwargs
            kw['origin'] = 'lower'
            kw['extent'] = self.extent
            ax.imshow(eval(fill), **kw)

        # Draw the contours. The azimuthal angles are drawn on individually to
        # avoid having overlapping lines about the +\- pi boundary making a
        # particularly thick line.

        kw = {} if contour_kwargs is None else contour_kwargs
        kw['levels'] = kw.pop('levels', np.arange(0.5, 0.99 * r_max, 0.5))
        kw['levels'] = np.append(kw['levels'], 0.99 * r_max)
        kw['linewidths'] = kw.pop('linewidths', 1.0)
        kw['colors'] = kw.pop('colors', 'k')
        ax.contour(self.xaxis, self.yaxis, rvals, **kw)

        kw['levels'] = [0.0]
        for t in np.arange(-np.pi, np.pi, np.pi / 8.0):
            if t - 0.1 < -np.pi:
                a = np.where(abs(tvals - t) <= 0.4,
                             tvals - t, np.nan)
                b = np.where(abs(tvals - 2.0 * np.pi - t) <= 0.4,
                             tvals - 2.0 * np.pi - t, np.nan)
                amask = np.where(np.isfinite(a), 1, -1)
                bmask = np.where(np.isfinite(b), 1, -1)
                a = np.where(np.isfinite(a), a, 0.0)
                b = np.where(np.isfinite(b), b, 0.0)
                ttmp = np.where(amask * bmask < 1, a + b, np.nan)
            elif t + 0.1 > np.pi:
                a = np.where(abs(tvals - t) <= 0.4,
                             tvals - t, np.nan)
                b = np.where(abs(tvals + 2.0 * np.pi - t) <= 0.4,
                             tvals + 2.0 * np.pi - t, np.nan)
                amask = np.where(np.isfinite(a), 1, -1)
                bmask = np.where(np.isfinite(b), 1, -1)
                a = np.where(np.isfinite(a), a, 0.0)
                b = np.where(np.isfinite(b), b, 0.0)
                ttmp = np.where(amask * bmask < 1, a + b, np.nan)
            else:
                ttmp = np.where(abs(tvals - t) <= 0.4, tvals - t, np.nan)
            ax.contour(self.xaxis, self.yaxis, ttmp, **kw)
        ax.set_xlim(max(ax.get_xlim()), min(ax.get_xlim()))
        ax.set_aspect(1)

        if return_fig:
            return fig

    def plot_spectrum(self, ax=None, x0=0.0, y0=0.0, inc=0.0, PA=0.0,
                      r_min=None, r_max=None, return_fig=False):
        """
        Plot the integrated spectrum.

        Args:
            x0 (Optional[float]): Right Ascension offset in [arcsec].
            y0 (Optional[float]): Declination offset in [arcsec].
            inc (Optional[float]): Disk inclination in [deg].
            PA (Optional[float]): Disk position angle in [deg].
            r_max (Optional[float]): Radius to integrate out to in [arcsec].
        """
        if ax is None:
            fig, ax = plt.subplots()
        else:
            return_fig = False
        x = self.velax.copy() / 1e3
        y, dy = self.integrated_spectrum(x0, y0, inc, PA, r_min, r_max)
        ax.axhline(0.0, ls='--', lw=1.0, color='0.9', zorder=-9)
        ax.step(x, y, where='mid', lw=1.0, color='k')
        ax.errorbar(x, y, dy, fmt=' ', lw=1.0, color='k', zorder=-8)
        ax.set_xlabel("Velocity (km/s)")
        ax.set_ylabel("Integrated Flux (Jy)")
        ax.set_xlim(x[0], x[-1])
        ticks = np.diff(ax.xaxis.get_majorticklocs()).mean() / 5.0
        ax.xaxis.set_minor_locator(MultipleLocator(ticks))
        ticks = np.diff(ax.yaxis.get_majorticklocs()).mean() / 5.0
        ax.yaxis.set_minor_locator(MultipleLocator(ticks))

        if return_fig:
            return fig

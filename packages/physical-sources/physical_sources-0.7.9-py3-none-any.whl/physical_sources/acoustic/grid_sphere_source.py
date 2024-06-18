import numpy
import numpy as np
from scipy.interpolate import SmoothSphereBivariateSpline
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

from physical_sources.acoustic.sphere_source import ISphereSource, SphericalFitMethods
from PythonCoordinates.measurables.physical_quantities import Length, Angle
from PythonCoordinates.coordinates.coordinate_representations import SphericalCoordinate


def plot_fit_data_2d(locations=None, metric=None, source=None, metric_name=None):
    cm = plt.cm.get_cmap('jet')
    fig = plt.figure()
    plt.subplot(projection='aitoff')
    plt.grid()
    plt.yticks(
        [5 / 12 * np.pi, 4 / 12 * np.pi, 3 / 12 * np.pi, 2 / 12 * np.pi, 1 / 12 * np.pi, 0, -1 / 12 * np.pi,
         -2 / 12 * np.pi, -3 / 12 * np.pi, -4 / 12 * np.pi, -5 / 12 * np.pi],
        labels=['15', '30', '45', '60', '75', '90', '105', '120', '135', '150', '165']
    )
    plt.text(0, -0 + np.pi / 2, '+z')
    plt.text(0, -np.pi + np.pi / 2, '-z')
    plt.text(0, -np.pi / 2 + np.pi / 2, '+x')
    plt.text(np.pi, -np.pi / 2 + np.pi / 2, '-x')
    plt.text(-np.pi, -np.pi / 2 + np.pi / 2, '-x')
    plt.text(np.pi / 2, -np.pi / 2 + np.pi / 2, '+y')
    plt.text(-np.pi / 2, -np.pi / 2 + np.pi / 2, '-y')
    plt.xlabel('azimuth ($\phi$)')
    plt.ylabel('polar ($\Theta$)')

    if metric is not None:
        vmin = np.min(metric)
        vmax = np.max(metric)
    elif source is not None:
        if not isinstance(source, GridSphereSource):
            raise TypeError("Input source must be of type 'GridSphereSource'")
        vmin = source.metric_grid.min()
        vmax = source.metric_grid.max()
    else:
        raise ValueError('Either the input pair locations and metric or the input source must not equal None.')

    if source is not None:
        theta_regular = []
        for i in range(len(source.polar)):
            theta_regular.append(-source.polar[i].radians + np.pi / 2)
        phi_regular = []
        for i in range(len(source.azimuth)):
            phi_regular.append(source.azimuth[i].radians)
        plt.pcolormesh(phi_regular, theta_regular, source.metric_grid, cmap=cm, vmin=vmin, vmax=vmax)

    if locations is not None:

        normalize_180_180(locations)

        theta = []
        phi = []
        for i in range(len(locations)):
            theta.append(-locations[i].polar.radians + np.pi / 2)
            phi.append(locations[i].azimuthal.radians)
        plt.scatter(phi, theta, c=metric, cmap=cm, vmin=vmin, vmax=vmax, edgecolors='k')

    plt.colorbar(label=metric_name)

    return fig


# TODO Fix and implement 3D Sphere Plotting
def plot_fit_data_3d(locations=None, metric=None, source = None, metric_name=None):
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    #
    # if metric is not None:
    #     vmin = np.max(metric)
    #     vmax = np.min(metric)
    # elif source is not None:
    #     if not isinstance(source, GridSphereSource):
    #         raise TypeError("Input source must be of type 'GridSphereSource'")
    #     vmin = source.metric_grid.min()
    #     vmax = source.metric_grid.max()
    # else:
    #     raise ValueError('Either the input pair locations and metric or the input source must not equal None.')
    # norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    #
    # if source is not None:
    #     x = np.empty([len(source.polar), len(source.azimuth) + 1])
    #     y = np.empty([len(source.polar), len(source.azimuth) + 1])
    #     z = np.empty([len(source.polar), len(source.azimuth) + 1])
    #     for i in range(len(source.polar)):
    #         for j in range(len(source.azimuth)):
    #             location = SphericalCoordinate(r=source.radius, polar=source.polar[i], azimuthal=source.azimuth[j])
    #             location = location.to_cartesian()
    #             x[i, j] = location.x.meters
    #             y[i, j] = location.y.meters
    #             z[i, j] = location.z.meters
    #         location = SphericalCoordinate(r=source.radius, polar=source.polar[i], azimuthal=source.azimuth[1])
    #         location = location.to_cartesian()
    #         x[i, -1] = location.x.meters
    #         y[i, -1] = location.y.meters
    #         z[i, -1] = location.z.meters
    #     metric_grid_wrapped = np.concatenate((source.metric_grid, source.metric_grid[:, 1, None]), axis=1)
    #
    #     ax.plot_surface(x, y, z, facecolors=plt.cm.jet(norm(metric_grid_wrapped)))
    #     m = plt.cm.ScalarMappable(cmap=plt.cm.jet, norm=norm)
    #     m.set_array([])
    #     plt.colorbar(m)
    #     ax.set_xlabel('x (m)')
    #     ax.set_ylabel('y (m)')
    #     ax.set_zlabel('z (m)')
    #     # plt.show()
    #
    # return fig
    pass


def normalize_180_180(locations):
    for i in range(len(locations)):
        while locations[i].azimuthal.degrees > 180:
            locations[i] = SphericalCoordinate(
                locations[i].r,
                locations[i].polar,
                Angle(locations[i].azimuthal.degrees - 360, unit=Angle.Units.Degrees)
            )
        while locations[i].azimuthal.degrees < -180:
            locations[i] = SphericalCoordinate(
                locations[i].r,
                locations[i].polar,
                Angle(locations[i].azimuthal.degrees + 360, unit=Angle.Units.Degrees)
            )


class GridSphereSource(ISphereSource):
    """
    This class defines any metric on the surface of a sphere of fixed radius, with regular angular
    spacing in the polar (theta) and azimuthal (phi) conventional spherical coordinates.

    :param polar: Iterable[Angle]
        List, Tuple, or 'numpy.ndarray' of polar (theta) angle values, regularly spaced in the range [0, 180]
    :param azimuth: Iterable[Angle]
        List, Tuple, or 'numpy.ndarray' of polar (theta) angle values, regularly spaced in the range [-180, 180]
    :param radius: Length
        A single value of type 'Length' denoting the fixed sphere radius
    :param metric_grid: numpy.ndarray
        A 2-dimensional 'numpy.ndarray' of size len(polar) x len(azimuth)
    """

    def __init__(self, polar=None, azimuth=None, radius: Length = None, metric_grid: numpy.ndarray = np.empty([0, 0]),
                 corr_coef: float = None, mse: float = None):
        super().__init__()

        self._polar = polar
        if self._polar is not None:
            self._theta = self._calculate_angles_degrees(self._polar)
        else:
            self._theta = None

        self._azimuth = azimuth
        if self._azimuth is not None:
            self._phi = self._calculate_angles_degrees(self._azimuth)
        else:
            self._phi = None

        self._radius = radius
        if self._radius is not None:
            self._check_radius(self._radius)

        self._metric_grid = metric_grid
        self._check_metric_grid(self._metric_grid, self.polar, self.azimuth)

        self._corr_coef = corr_coef
        self._mse = mse

    @property
    def polar(self):
        return self._polar

    @polar.setter
    def polar(self, values):

        self._polar = values
        self._theta = self._calculate_angles_degrees(self._polar)

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, values):
        self._azimuth = values
        self._phi = self._calculate_angles_degrees(self.azimuth)

    @property
    def radius(self):
        if self._radius is not None:
            self._check_radius(self._radius)
        return self._radius

    @radius.setter
    def radius(self, value):
        self._check_radius(value)
        self._radius = value

    @property
    def metric_grid(self):
        if self._metric_grid.any():
            self._check_metric_grid(self._metric_grid, self.polar, self.azimuth)
        return self._metric_grid

    @metric_grid.setter
    def metric_grid(self, array):
        self._metric_grid = array

    @property
    def mse(self):
        return self._mse

    @property
    def corr_coef(self):
        return self._corr_coef

    @staticmethod
    def fit(locations, metric, order: int = 0, dpolar: Angle = Angle(5.0, unit=Angle.Units.Degrees),
            dazimuth: Angle = Angle(5.0, unit=Angle.Units.Degrees),
            method=SphericalFitMethods.SmoothSphereBivariateSpline,
            std=1e-2):
        """
        This function will return a GridSphereSource object representing any metric by fitting the values in
        metric sampled at any set of SphericalCoordinate locations on a sphere of fixed radius.

        :param locations: Iterable[SphericalCoordinate]
            This is a collection of the known locations on the spherical surface. The radius values must be equal
            for all locations.
        :param metric: Iterable[float]
            A single or double dimensioned array that will be used to fit the regular grid values.
        :param order: int
            The order of fitting method that will be accomplished
        :param dpolar: Angle
            The desired regular polar angle spacing in degrees
        :param dazimuth: Angle
            The desired regular azimuthal angle spacing in degrees
        :param method: SphericalFitMethods
            An Enumeration of available methods for fitting metric to a spherical surface
        :param std: float
            The input parameter which controls the interplay between the smoothness of the resulting curve
            and the quality of the approximation of the data. Increasing std leads to smoother fits, and in
            the limit of a very large std, the curve degenerates into a single best-fit polynomial. A good
            choice might be around the approximate standard deviation of the data.
        :return: GridSphereSource
            A GridSphereSource object containing estimates of the metric values sampled at regular angular
            intervals over the surface of a sphere of the same radius as the input locations
        :raises ValueError: if the radius values r are not equal at all locations
        """

        # TODO - Alan implement check and warning if input points overlap in location

        GridSphereSource._check_polar_angles(locations)

        radius = GridSphereSource._get_radius(locations)
        theta = np.empty(len(locations))
        phi = np.empty(len(locations))
        for i in range(len(locations)):
            theta[i] = locations[i].polar.radians
            phi[i] = locations[i].azimuthal.normalized.radians

        grid_interpolation = SmoothSphereBivariateSpline(theta, phi, metric, s=len(locations) * std ** 2)
        metric_predicted = grid_interpolation(theta, phi, grid=False)

        theta_regular = np.arange(0., np.pi * 1.0001, step=dpolar.radians)
        phi_regular = np.arange(0, 2 * np.pi, step=dazimuth.radians)
        metric_grid = grid_interpolation(theta_regular, phi_regular)

        # Shift data to -180 <= phi <= +180 convention
        phi_regular[phi_regular < 0] += 2 * np.pi
        metric_grid = np.concatenate((
            metric_grid[:, [i for i in range(len(phi_regular)) if phi_regular[i] >= np.pi]],
            metric_grid[:, [i for i in range(len(phi_regular)) if phi_regular[i] < np.pi]],
            metric_grid[:, np.where(phi_regular >= np.pi)[0][0], None]
        ), axis=1)
        phi_regular = np.concatenate((
            phi_regular[[i for i in range(len(phi_regular)) if phi_regular[i] >= np.pi]] - 2 * np.pi,
            phi_regular[[i for i in range(len(phi_regular)) if phi_regular[i] < np.pi]],
            phi_regular[np.where(phi_regular >= np.pi)[0][0], None]
        ))

        theta_grid = np.empty(len(theta_regular), dtype=Angle)
        for i in range(len(theta_regular)):
            theta_grid[i] = Angle(theta_regular[i], unit=Angle.Units.Radians)
        phi_grid = np.empty(len(phi_regular), dtype=Angle)
        for i in range(len(phi_regular)):
            phi_grid[i] = Angle(phi_regular[i], unit=Angle.Units.Radians)

        return GridSphereSource(
            polar=theta_grid,
            azimuth=phi_grid,
            radius=radius,
            metric_grid=metric_grid,
            corr_coef=pearsonr(metric, metric_predicted).statistic,
            mse=mean_squared_error(metric, metric_predicted)
        )

    def predict(self, location):
        pass

    @staticmethod
    def parse_xml(root):
        pass

    def make_xml(self, root):
        pass

    @staticmethod
    def _calculate_angles_degrees(angles):
        """
        Calculates angles as a 'numpy.ndarray' in degrees from an iterable of type 'Angle' objects
        """
        degrees = np.empty(shape=[len(angles)])
        for i in range(len(degrees)):
            if not isinstance(angles[i], Angle):
                raise TypeError("Elements of input iterable must be of type 'Angle'")
            degrees[i] = angles[i].degrees
        return degrees

    @staticmethod
    def _check_radius(radius):
        if not isinstance(radius, Length):
            raise TypeError("radius must be of type 'Length'")

    @staticmethod
    def _get_radius(locations):
        for i in range(len(locations)):
            if locations[i].r != locations[0].r:
                raise ValueError("All locations must be given as 'SphericalCoordinate' objects with the same radius r")
        return locations[0].r

    @staticmethod
    def _check_polar_angles(locations):
        for a in locations:
            if not 0 <= a.polar.radians <= np.pi:
                raise ValueError('polar angles must lie within the interval [0, pi]')

    @staticmethod
    def _check_metric_grid(metric_grid, polar, azimuth):
        if not isinstance(metric_grid, numpy.ndarray):
            raise TypeError("metric_grid must be of type 'numpy.ndarray'")
        if len(metric_grid.shape) != 2:
            raise ValueError("metric_grid must be a 2-dimensional array")
        if metric_grid.any():
            if metric_grid.shape[0] != len(polar):
                raise ValueError("The length of the first dimension of metric_grid must equal len(polar)")
            if metric_grid.shape[1] != len(azimuth):
                raise ValueError("The length of the second dimension of metric_grid must equal len(azimuth)")


class GridSphereSourceTemp(ISphereSource):
    def __init__(self,
                 grid_sphere: GridSphereSource = None,
                 corr_coeff: float = None,
                 mse: float = None
                 ):
        super().__init__()
        self._corr_coeff = None
        self._mse = None


class Weapon(ISphereSource):

    @staticmethod
    def fit(x, y, order: int = 0):
        """
        :param x: Numpy.ndarray of SphericalCoordinate objects
            This is a collection ...
        :param y: Numpy.ndarray or Dataframe
            A single or double ...
        :param order: int
            The maximum...
        """

        # series =

        # Import data from standard file

        # Loop through the second dimenstion of the y values (i.e. metric columns)

        # source = GridSphereSource.fit()

        return "Object of type Weapon"

    def predict(self, location):
        return "all metrics at a single location"

    @staticmethod
    def parse_xml(root):
        pass

    def save(self):
        pass

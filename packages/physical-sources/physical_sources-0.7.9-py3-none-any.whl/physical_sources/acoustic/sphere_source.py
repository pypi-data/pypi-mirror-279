import abc
from enum import Enum
from physical_sources.acoustic.inoisesource import INoiseSource
from PythonCoordinates.measurables.Measurable import InvalidUnitOfMeasureException
from PythonCoordinates.measurables.physical_quantities import Length
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xml.etree.ElementTree
import os.path
from PythonCoordinates.measurables.physical_quantities import Length, Angle, Temperature, Pressure, Humidity
from PythonCoordinates.coordinates.coordinate_representations import SphericalCoordinate
from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools
import sys
import scipy
from matplotlib import cm, colors


class SphericalFitMethods(Enum):
    """
    The available methods for fitting data to the surface of a sphere
    """

    SphericalHarmonics = 0
    SmoothSphereBivariateSpline = 1


class ISphereSource(INoiseSource):
    """
    This class represents a single value on the surface of a sphere. The methods here are abstracted and must be
    implemented in any child class.
    """

    def __init__(self):
        """
        This is a generic constructor. It only creates the instances of the object's private or protected properties.
        """
        super().__init__()

        self._description = None
        self._reference_distance = None

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def reference_distance(self):
        return self._reference_distance

    @reference_distance.setter
    def reference_distance(self, value):
        if not isinstance(value, Length):
            self._reference_distance = Length(value)
        else:
            self._reference_distance = value

    @staticmethod
    @abc.abstractmethod
    def fit(x, y, order: int):
        """
        This function will determine the internal representation of the grid
        :param x:
            This is a doubly dimensioned array that represents the azimuthal and polar angles from the
        :param y:
        :param order:
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def predict(self, location):
        """
        This will determine the value on the surface of the sphere at the specific location, or series of locations.
        :param location:
            This is either a collection (array or list) of locations or a SphericalCoordinate. If it is a list, it is
            expected that the list contains a collection of SphericalCoordinate objects.
        :return:
            The single value, or collection of values evaluated at the locations in the argument.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def parse_xml(root):
        """
        This function will parse the
        :param root:
        :return:
        """
        raise NotImplementedError


def plot_irregular_surface(locations, desired_x=None, desired_y=None, ax=None, vmin=None, vmax=None, colormap=cm.jet,
                           invert_z_axis: bool = True):
    """
    We desire the ability to plot the spherical surface in a 3-D representation where the faces will be the color of
    the acoustic level that we are attempting to characterize.
    :param desired_y:
    :param desired_x:
    :param invert_z_axis: bool
        This flag determines whether the z-axis values need to be negated for the proper display of the data
    :param colormap:
    :param vmax: float
        The maximum value for the coloring of the faces of the surface
    :param vmin: float
        The minimum value for the coloring of the faces of the surface
    :param locations: list or array-like
        Collection of spherical locations that we want to display one a spherical surface.
    :param ax: Matplotlib.pyplot.axis
        The axis that we want to use for the plotting
    :return:
        axis object that hold the data, and the smoothed surface
    """
    from PythonCoordinates.conversions.measurement_resolution import nearest_neighbor_dense_sampling

    if ax is None:
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    #   Use the nearest neighbor interpolation to define the surface that we want to plot.
    #
    #   Examine the data and determine the range of the azimuthal and polar angles within the data
    true_data = _transform_data_to_dataframe(locations)

    if desired_x is None:
        min_az = true_data['x'].min()
        max_az = true_data['x'].max()
        desired_azimuthal = np.linspace(min_az, max_az, 50)
    else:
        desired_azimuthal = desired_x

    if desired_y is None:
        min_polar = true_data['y'].min()
        max_polar = true_data['y'].max()
        desired_polar = np.linspace(min_polar, max_polar, 50)
    else:
        desired_polar = desired_y

    #   Build the ability to interpolate the colors
    if vmax is None:
        vmax = true_data['z'].max()
    if vmin is None:
        vmin = true_data['z'].min()

    color_normalizer = colors.Normalize(vmin=vmin, vmax=vmax)

    #   Calculate the interpolated grid in spherical coordinates
    xx, yy, szz, zz = nearest_neighbor_dense_sampling(true_data, desired_azimuthal, desired_polar,
                                                      smoothing_error_tolerance=1e-4, verbose_info=False)

    #   Now we need to create a set of locations that are in Cartesian coordinate representation, but still have the
    #   same shape as the spherical data
    cxx, cyy, czz = _transform_data_to_matrix(xx, yy, szz)

    if invert_z_axis:
        czz *= -1

    ax.plot_surface(cxx, cyy, czz, facecolors=colormap(color_normalizer(szz)))

    return ax, xx, yy, szz, color_normalizer


def _transform_data_to_dataframe(locations: np.ndarray):
    """
    This function assists in reducing the complexity of the plotting functions and transforms the SphericalCoordinate
    array to a Pandas.DataFrame that contains the information in a flat plane to be interpolated by the nearest
    neighbor interpolation routine.
    :param locations: Numpy.ndarray
        This is the collection of SphericalCoordinate classes that needs to be converted to a Pandas.DataFrame. The
        values will be represented in the DataFrame as Cartesian coordinates, but this is in name only.
    :return: Pandas.DataFrame
    """

    true_data = pd.DataFrame(columns=['x', 'y', 'z'], index=np.arange(len(locations)))

    for i in range(len(locations)):
        if not isinstance(locations[i], SphericalCoordinate):
            raise ValueError("The surface locations must be a SphericalCoordinate")

        true_data.iloc[i, :] = [locations[i].azimuthal.degrees, locations[i].polar.degrees, locations[i].r.meters]

    return true_data


def _transform_data_to_matrix(xx, yy, zz):
    """
    Data is returned from the nearest neighbor interpolation as doubly dimensioned matrices. However,
    this information will be stored in whatever format the data was presented in. For the plotting of the surfaces
    the information is obtained as a series of angles and lengths that represent a Spherical Coordinate
    representation. This function will transform the spherical representation to a doubly dimensioned matrix using a
    CartesianCoordiante representation
    :param xx: Numpy.ndarray
        The decimal degrees values for the azimuthal direction
    :param yy: Numpy.ndarray
        The decimal degrees values for the polar direction
    :param zz: Numpy.ndarray
        The decimal meters values for the radial direction
    :return:
        Cartesian xx, yy, zz matrices in units of meters
    """
    cxx = np.zeros(xx.shape)
    cyy = np.zeros(yy.shape)
    czz = np.zeros(zz.shape)

    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            c = SphericalCoordinate(r=Length(zz[i, j]),
                                    polar=Angle(yy[i, j]),
                                    azimuthal=Angle(xx[i, j])).to_cartesian()
            cxx[i, j] = c.x.meters
            cyy[i, j] = c.y.meters
            czz[i, j] = c.z.meters

    return cxx, cyy, czz


def plot_unwrapped(xx, yy, zz, color_map_name: str = 'jet', contour_levels: np.ndarray = np.arange(0, 100, 10),
                   contour_lines: np.ndarray = np.arange(50, 100, 5)):
    """
    This function will plot the data as an unwrapped display of the spherical data.
    :param xx: Numpy.ndarray
        The x-values to plot
    :param yy: Numpy.ndarray
        The x-values to plot
    :param zz: Numpy.ndarray
        The surface-values to plot
    :param color_map_name: str
        The name of the colormap to use for the surface
    :param contour_levels: Numpy.ndarray
        A linear array of values that we will use to color the faces of the surface
    :param contour_lines: Numpy.ndarray
        A collection of value to calculate contour lines at
    :return:
        the figure
    """

    #   Create the figure
    fig, ax = plt.subplots()

    #   Build the filled contour plot
    contours = ax.contourf(xx,
                           yy,
                           zz,
                           levels=contour_levels,
                           cmap=color_map_name,
                           antialiased=True)
    cbar = plt.colorbar(contours)

    #   Add the contour lines
    cs = ax.contour(xx,
                    yy,
                    zz,
                    levels=contour_lines,
                    linestyles='solid',
                    colors='k')
    ax.clabel(cs, fontsize=6, inline=1, fmt='%.0f')

    return fig, ax


class HarmonicSeries(ISphereSource):
    """
    The harmonic source is a collection of coefficient definition sets. This definition is the example of how to
    organize the information, but does not have to be a frequency band. So this was refactored to be more generic.
    """

    def __init__(self, series_coefficients: np.ndarray, description: str, r: float = None, mse: float = None):
        """
        This constructor builds the object for the holding of information regarding the construction of a frequency's
        acoustic surface
        :param mse: float
            The mean squared error determined during the curve fitting
        :param r: float
            The pearson correlation coefficient determined during the curve fitting
        :param description: str
            a text description of the object represented by this series expansion
        :param series_coefficients: complex, array-like
            the list of harmonic coefficients for the reconstruction
        """
        super().__init__()

        self._coefficients = series_coefficients
        self._description = description
        self._order = int(np.floor(np.sqrt(len(self._coefficients)) - 1))
        self._pearson_r = r
        self._mse = mse

    @property
    def coefficients(self):
        """
        If the user needs to explore the coefficients directly, they can use this property to gain access to the
        array-like list of complex coefficients.
        :return: array-like
            List of complex coefficients that represent the harmonic expansion
        """
        return self._coefficients

    @property
    def fit_correlation_coefficient(self):
        return self._pearson_r

    @property
    def fit_mse(self):
        return self._mse

    @property
    def order(self):
        """
        The order refers to the harmonic series expansion order that is represented by the coefficients within this
        class. While this can be easily calculated from the length of the coefficient array, it was determined in the
        constructor so that it is quicker to determine the limits of the expansion.
        :return: int
            The order ("l") within the harmonic series expansion.
        """
        return self._order

    @staticmethod
    def parse_xml(root):
        """
        This function will parse through the information in the XML node and return a HarmonicSeries object to the user.
        :param root: ElementTree
        :return: HarmonicSeries object
        """

        #   Loop through the coefficient list
        coefficient_list = list()
        for coefficients in root:
            for coefficient in coefficients:
                coefficient_list.append(complex(float(coefficient[0].text), float(coefficient[1].text)))

        if "description" in root.attrib.keys():
            description = root.attrib['description']
        else:
            description = None

        if "fit_mse" in root.attrib.keys():
            mse = root.attrib['fit_mse']
        else:
            mse = None

        if "fit_correlation_coefficient" in root.attrib.keys():
            fit_r = root.attrib["fit_correlation_coefficient"]
        else:
            fit_r = None

        series = HarmonicSeries(series_coefficients=np.asarray(coefficient_list), description=root.attrib[
            'description'], r=fit_r, mse=mse)

        return series

    @staticmethod
    def yml(l, m, polar, azimuthal):
        """
        Calculate the normalized spherical harmonics for the provided order (l) and power (m) at the provided angle set.
        The original function was replaced with the scipy function for the calculation of the spherical harmonics.

        :param l : int
            the order of the series
        :param m : int
            the power of the series
        :param polar : double (units: radians)
            the polar angle of the spherical harmonics
        :param azimuthal : double (units: radians)
            the azimuthal angle of the spherical harmonics

        :returns : complex
            the values of the spherical harmonics at these angles, order and power.

        20220329 - FSM - Refactored the calculation of the angles that are used within the determination of the
            spherical harmonic value
        """
        if isinstance(azimuthal, Angle):
            az_angle_radians = azimuthal.radians
        elif isinstance(azimuthal, tuple):
            if isinstance(azimuthal[0], Angle):
                az_angle_radians = azimuthal[0].radians
            else:
                az_angle_radians = azimuthal[0]
        else:
            az_angle_radians = azimuthal

        if isinstance(polar, Angle):
            pol_angle_radians = polar.radians
        elif isinstance(polar, tuple):
            if isinstance(polar[0], Angle):
                pol_angle_radians = polar[0].radians
            else:
                pol_angle_radians = polar[0]
        else:
            pol_angle_radians = polar

        result = scipy.special.sph_harm(m, l, az_angle_radians, pol_angle_radians)

        return result

    @staticmethod
    def harmonic_matrix(order, polar, azimuthal):
        """
        Using the matrix format, create a matrix that has a row for each element in the theta and phi vectors, and a
        column for each of the l, m pairs up to the (l**2 + 1) count.

        order : int
            The maximum order of the series expansion and the definition of the elements to calculate
        polar : Angle or double, array-like
            the polar angle of the series expansion
        azimuthal : Angle or double, array-like
            the azimuthal angle of the series expansion

        returns: complex, array-like
            the matrix that is nxm, where n = len(polar) and m = (l**2+1).
        """

        #   If both the polar and azimuthal arguments are of type Angle

        if isinstance(polar, Angle) and isinstance(azimuthal, Angle):
            #   Create the return object
            b = HarmonicSeries._build_even_order_matrix(order, [polar], [azimuthal])

            #   Using the positive values of the power (m), look for the symmetric values to determine the negative
            #   values of the power (m)
            b = HarmonicSeries._build_reflected_matrix(b, order, [polar])

        else:
            #   Create the return object
            b = HarmonicSeries._build_even_order_matrix(order, polar, azimuthal)

            #   Using the positive values of the power (m), look for the symmetric values to determine the negative
            #   values of the power (m)
            b = HarmonicSeries._build_reflected_matrix(b, order, polar)

        return b

    @staticmethod
    def \
            _build_even_order_matrix(order: int, polar, azimuthal):
        """
        This function will build the positive 'm' values within the harmonic series matrix. This is because the
        calculation of the spherical harmonics is non-trivial and exponentially increasing with time. However,
        there is a relationship between the +m and -m values where, knowing the value of the +m harmonic, the -m harmonic
        is easily calculated with symmetry and conjugation.
        :param order: int
            The order of the harmonic - this is the L index for which we calculate the m values on the interval 0 <= m <= l
        :param polar: list or Numpy.ndarray
            The collection of polar angles that we want to calculate the harmonics at
        :param azimuthal: list or Numpy.ndarray
            The collection of azimuthal angles that we want to calculate the harmonics at
        :return: np.ndarray
            The dense matrix of values for positive values of m
        """

        b = np.zeros(shape=(len(polar), ((order + 1) * (order + 1))), dtype=np.complex_)

        #   Calculate the values of the spherical harmonics with a positive power (m)

        for index_element in range(len(polar)):
            for index_order in range(order + 1):
                for index_m in range(index_order + 1):
                    #   Calculate the index within the matrix for this l, m combination
                    index = index_order * index_order + index_order + index_m

                    #   Insert the harmonic value at this site
                    b[index_element, index] = HarmonicSeries.yml(
                        index_order,
                        index_m,
                        polar[index_element],
                        azimuthal[index_element])

        return b

    @staticmethod
    def _build_reflected_matrix(b: np.ndarray, order: int, polar):
        """
        This function reflects the upper triangle to the lower triangle of the matrix of harmonic values. This is
        accomplished due to the relationship of the m and -m values of the harmonic series.
        :param b: numpy.ndarray
            This is the matrix that have been calculated for the positive mode values (m)
        :param order: int
            The number of harmonics to use (l)
        :param polar:
            The collection of polar angles. This is only used to provide a limit for the integration and summation
        :return:
            The fully built matrix is returned.
        """
        for index_element in range(len(polar)):
            for index_order in range(order + 1):
                for index_m in range(-index_order, 0, 1):
                    #   Calculate the index of this element, and the symmetric +m value
                    index = index_order * index_order + index_order + index_m
                    sym_index = index_order * index_order + index_order + abs(index_m)

                    #   get the symmetric value and adjust the complex value
                    b[index_element, index] = np.power(-1.0, index_m) * complex.conjugate(
                        b[index_element, sym_index])

        return b

    @staticmethod
    def invertible_harmonic_matrix(order, polar, azimuthal):
        """
        Inherently the matrix B is non-square.  To invert this matrix we must generate a square matrix.  For this we
        use the complex conjugate transpose of B and multiply by B, i.e. BtB.

        order : int
            The maximum order of the series expansion and the definition of the elements to calculate
        polar : Angle or double, array-like
            the polar angle of the series expansion
        azimuthal : Angle or double, array-like
            the azimuthal angle of the series expansion

        returns: complex, array-like
            the matrix that is mxm, where m = (l**2+1).
        """

        #   Get the matrix
        b = np.asmatrix(HarmonicSeries.harmonic_matrix(order, polar, azimuthal))

        #   Determine the complex conjugate transpose
        trans = b.getH()

        #   Multiply with the harmonic matrix to obtain the BtB square matrix
        mul = trans.dot(b)

        return np.asarray(mul)

    @staticmethod
    def scaled_surface_value(b, r):
        """
        The R.H.S. of the matrix equation evaluates to BtR and this will need to be computed from the harmonic matrix
        and the radial sound pressure level values.

        b : complex, array-like
            the harmonic series matrix that is nxm, where n is the number of elements on the surface of the sphere, and
            m is the number of harmonic components (m = (order + 1)**2)

        r : double, array-like
            the sound pressure level radial function at a selected frequency

        returns : complex, array-like
            the complex conjugate transpose of the harmonic matrix multiplied by the radial values (i.e. BtR)
        """
        if (isinstance(b, np.ndarray) or isinstance(b, np.matrix)) and (
                isinstance(r, np.ndarray) or isinstance(r, list)):
            bt = np.asmatrix(b).getH()
            btr = np.matmul(bt, r)

            return np.asarray(btr).reshape((b.shape[1],))

    def predict(self, location):
        """
        This function will calculate the value of the harmonic series expansion at the specified location.
        :param location: SphericalCoordinate
            The location on the surface of the sphere where we want to determine the value of the harmonic series.
            Since the data is expanded as a sphere, we will require the user to represent the location as a
            SphericalCoordinate object
        :return: float
            The value of the harmonic series at the specific location provided
        """

        #   Determine the harmonic matrix at this location
        if isinstance(location, SphericalCoordinate):
            b = HarmonicSeries.harmonic_matrix(self.order, location.polar, location.azimuthal)
        elif (isinstance(location, np.ndarray) or isinstance(location, list)) and \
                isinstance(location[0], SphericalCoordinate):
            polar = np.empty(len(location), dtype=Angle)
            azimuthal = np.empty(len(location), dtype=Angle)
            for i in range(len(location)):
                polar[i] = location[i].polar
                azimuthal[i] = location[i].azimuthal

            b = HarmonicSeries.harmonic_matrix(self.order, polar, azimuthal)

        return b.dot(self.coefficients).real

    def make_xml(self, root):
        """
        In effort to utilize the proper construction of the XML nodes, we will provide the node that represents this
        class's series expansion and append it directly to the root that is provided.
        :param root: ElementTree
            The parent of the XML node that we are constructing in this function
        :return:
        """

        parent = xml.etree.ElementTree.SubElement(root, "series_expansion")
        parent.attrib['description'] = self.description
        if self.fit_correlation_coefficient is not None:
            parent.attrib['fit_correlation_coefficient'] = "{:.10f}".format(self.fit_correlation_coefficient)
        if self.fit_mse is not None:
            parent.attrib['fit_mse'] = "{:.10f}".format(self.fit_mse)

        coefficients = xml.etree.ElementTree.SubElement(parent, "coefficients")

        for c in self.coefficients:
            node = xml.etree.ElementTree.SubElement(coefficients, "coefficient")

            real_node = xml.etree.ElementTree.SubElement(node, "real")
            real_node.text = str(c.real)

            imag_node = xml.etree.ElementTree.SubElement(node, "imaginary")
            imag_node.text = str(c.imag)

    @staticmethod
    def fit(x, y, order: int):
        """
        This function will convert the array data into a spherical harmonic representation of the radial basis function.

        20231017 - FSM - Replaced the error metric with median absolute error

        :param x: Numpy.ndarray of SphericalCoordinate objects
            This is a collection of the known locations on the spherical surface. At this point, the radius is ignored
        :param y: Numpy.ndarray
            A single or double dimensioned array that will be used to define the radial value of the harmonic series
            expansion.
        :param order: int
            The maximum order of fitting that will be accomplished
        :return: HarmonicSeries
            The collection of coefficients that best fit this array of location/radial values

        """
        from scipy.stats import pearsonr
        from sklearn.metrics import median_absolute_error
        from sklearn.metrics import mean_absolute_error

        if isinstance(order, int):
            o = order
        else:
            o = int(np.floor(order))

        if not (isinstance(x, np.ndarray) or isinstance(x, list)) and not isinstance(x[0], SphericalCoordinate):
            raise ValueError("The x values must be a list or numpy array of SphericalCoordinate objects")

        if not (isinstance(y, np.ndarray) or isinstance(y, list)):
            raise ValueError("The y values must be a numpy array")

        #   Extract the polar and azimuthal angles from the collection
        if isinstance(x, list):
            length = len(x)
        else:
            length = x.shape[0]
        polar = np.empty(length, dtype=Angle)
        azimuthal = np.empty(length, dtype=Angle)
        for i in range(length):
            polar[i] = x[i].polar
            azimuthal[i] = x[i].azimuthal

        #   Calculate the matrix solution to the fitting
        b = HarmonicSeries.harmonic_matrix(o, polar, azimuthal)
        btb = HarmonicSeries.invertible_harmonic_matrix(o, polar, azimuthal)
        inv_btb = np.linalg.inv(btb + sys.float_info.epsilon)
        btf = HarmonicSeries.scaled_surface_value(b, y)

        c = inv_btb.dot(btf)
        lvl = abs(b.dot(c).real)
        r = pearsonr(y, lvl)[0]
        mse = median_absolute_error(y, lvl)
        return HarmonicSeries(c, "", r, mse)


class HarmonicSpectrumNoiseSource(ISphereSource):
    """
    In effort to create a class that contains the information for a sound pressure level spectrum, this class
    contains a collection of HarmonicSeries objects that represent each frequency in the spectrum. In the future,
    additional classes can be derived that will represent different methods or combinations of functions on the
    surface of a sphere.
    """

    def __init__(self, a=None):
        """
        This constructor will build a dataset from the file that is passed as an argument to the constructor, or build
        the blank contents of the class for the construction of the directivity pattern and the file later.
        :param a: str - the path to the file that is to be read
        """
        super().__init__()

        self._de_dopplerized = False
        self._creation_date = None
        self._data_measured = 1
        self._measure_date = None
        self._version = "XML v1.1.0.1"
        self._power_setting = None
        self._power_setting_units = None

        self._reference_temperature = Temperature.std_temperature()
        self._reference_pressure = Pressure.std_pressure()
        self._reference_humidity = Humidity.std_humidity()
        self._reference_distance = Length.reference_sphere_radius()
        self._frequency_resolution = 3
        self._minimum_frequency_band = 10
        self._maximum_frequency_band = 40
        self._coefficients = []

        self._filename = None

        if a is not None:
            if not (isinstance(a, str) or isinstance(a, xml.etree.ElementTree.Element)):
                raise ValueError()
            else:
                if isinstance(a, str):
                    if not os.path.exists(a):
                        raise FileNotFoundError()

                    self._filename = a
                    self._load_definition(a)
                elif isinstance(a, xml.etree.ElementTree.Element):
                    self._load_definition(a)

                self._build_reference_atmospheric_absorption_losses()

    @property
    def is_de_dopplerized(self):
        return self._de_dopplerized

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value):
        import dateutil.parser

        if isinstance(value, str):
            try:
                value = dateutil.parser.parse(value)
            except dateutil.parser.ParserError:
                return

        self._creation_date = value

    @property
    def is_measured(self):
        return self._data_measured

    @is_measured.setter
    def is_measured(self, value):
        self._data_measured = int(value)

    @property
    def measurement_date(self):
        return self._measure_date

    @measurement_date.setter
    def measurement_date(self, value):
        import dateutil.parser

        if isinstance(value, str):
            try:
                value = dateutil.parser.parse(value)
            except dateutil.parser.ParserError:
                return

        self._measure_date = value

        self._measure_date = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def aircraft_power_setting(self):
        return self._power_setting

    @aircraft_power_setting.setter
    def aircraft_power_setting(self, value):
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return

        self._power_setting = value

    @property
    def aircraft_power_setting_units(self):
        return self._power_setting_units

    @aircraft_power_setting_units.setter
    def aircraft_power_setting_units(self, value):
        self._power_setting_units = value

    @property
    def ref_measurement_distance(self):
        return self._reference_distance

    @ref_measurement_distance.setter
    def ref_measurement_distance(self, value):
        if isinstance(value, str):
            value = Length(float(value), Length.Units.Meters)
        elif isinstance(value, float):
            value = Length(value, Length.Units.Meters)

        self._reference_distance = value

    @property
    def ref_humidity(self):
        return self._reference_humidity

    @ref_humidity.setter
    def ref_humidity(self, value):
        if isinstance(value, str):
            value = Humidity(float(value))
        elif isinstance(value, float):
            value = Humidity(value, Humidity.Units.Percentage)

        self._reference_humidity = value

    @property
    def ref_pressure(self):
        return self._reference_pressure

    @ref_pressure.setter
    def ref_pressure(self, value):
        if isinstance(value, str):
            value = Pressure(float(value))
        elif isinstance(value, float):
            value = Pressure(value, Pressure.Units.InchesMercury)

        self._reference_pressure = value

    @property
    def ref_temperature(self):
        return self._reference_temperature

    @ref_temperature.setter
    def ref_temperature(self, value):
        if isinstance(value, float):
            value = Temperature(value, Temperature.Units.Kelvin)
        elif isinstance(value, str):
            value = Temperature(float(value), Temperature.Units.Kelvin)

        self._reference_temperature = value

    @property
    def fractional_resolution(self):
        return self._frequency_resolution

    @fractional_resolution.setter
    def fractional_resolution(self, value):
        if isinstance(value, str):
            value = int(value)
        self._frequency_resolution = value

    @property
    def min_freq_band(self):
        return self._minimum_frequency_band

    @min_freq_band.setter
    def min_freq_band(self, value):
        if isinstance(value, str):
            value = int(value)

        self._minimum_frequency_band = value

    @property
    def max_freq_band(self):
        return self._maximum_frequency_band

    @max_freq_band.setter
    def max_freq_band(self, value):
        if isinstance(value, str):
            value = int(value)

        self._maximum_frequency_band = value

    @property
    def orders(self):
        orders = list()

        for band in self._coefficients:
            orders.append(band.order)

        return orders

    @property
    def name(self):
        return os.path.splitext(self.filename)[0]

    @property
    def minimum_frequency(self):
        return FractionalOctaveBandTools.center_frequency(self._frequency_resolution, self._minimum_frequency_band)

    @property
    def maximum_frequency(self):
        return FractionalOctaveBandTools.center_frequency(self._frequency_resolution, self._maximum_frequency_band)

    @property
    def series_coefficients(self):
        return self._coefficients

    @series_coefficients.setter
    def series_coefficients(self, value):
        self._coefficients = value

    @property
    def filename(self):
        return self._filename

    @property
    def reference_atmospheric_losses(self):
        return self._reference_loss

    def _load_definition(self, a):
        """
        This will load the definition from the XML file
        :param a: str
            the path to the definition file

        20220330 - FSM - Added some error catching for when attributes are not actually specified
        """
        attribute_names = ['frequency_resolution',
                           'creation_date',
                           'data_measured',
                           'measure_date',
                           'version',
                           'power_setting',
                           'power_setting_units',
                           'reference_temperature',
                           'reference_pressure',
                           'reference_humidity',
                           'reference_distance',
                           'minimum_frequency_band',
                           'maximum_frequency_band']
        property_names = ['fractional_resolution',
                          'creation_date',
                          'is_measured',
                          'measurement_date',
                          'version',
                          'aircraft_power_setting',
                          'aircraft_power_setting_units',
                          'ref_temperature',
                          'ref_pressure',
                          'ref_humidity',
                          'ref_measurement_distance',
                          'min_freq_band',
                          'max_freq_band']

        if isinstance(a, str):
            tree = xml.etree.ElementTree.ElementTree()
            tree.parse(a)
            root = tree.getroot()
        elif isinstance(a, xml.etree.ElementTree.Element):
            root = a

        #   We have constructed two arrays that contain a 1-to-1 relationship between the name of the attribute in
        #   the XML structure to the name of the property. We can now use the getattr and setattr functions to put
        #   the data in the correct place.
        for name in root.attrib.keys():
            element_index = attribute_names.index(name)

            setattr(self, property_names[element_index], root.attrib[name])

        #   Now the only remaining node is the coefficients node
        self._read_coefficients(root[0])

    def _read_coefficients(self, root):
        """
        This function will read the series_coefficients nodes from the file and create the contents for the
        coefficients of this source description
        :param root: xml.etree.ElementTree.Element
            This is the container for the series_expansion nodes that define the approximation for the various
            frequencies
        """
        for coefficient_storage in root:
            self._coefficients.append(HarmonicSeries.parse_xml(coefficient_storage))

    def _build_reference_atmospheric_absorption_losses(self):
        """
        Calculate the acoustic losses for the atmosphere at the reference conditions
        """
        from physical_propagation.acoustic_losses import AtmosphericAbsorption
        from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools as fob

        self._reference_loss = list()
        for i in range(0, len(self._coefficients)):
            f = fob.center_frequency(self.fractional_resolution, i + self.min_freq_band)
            self._reference_loss.append(AtmosphericAbsorption.alpha(self.ref_temperature,
                                                                    self.ref_pressure,
                                                                    self.ref_humidity,
                                                                    f) * self.ref_measurement_distance.meters)

    def make_xml(self):
        """
        This will create the XML structure from the data within the class.
        :return: xml.etree.ElementTree.Element
        """
        #   Define the attribute and property names so that we can loop through these elements easily
        attribute_names = ['frequency_resolution',
                           'creation_date',
                           'data_measured',
                           'measure_date',
                           'version',
                           'power_setting',
                           'power_setting_units',
                           'reference_temperature',
                           'reference_pressure',
                           'reference_humidity',
                           'reference_distance',
                           'minimum_frequency_band',
                           'maximum_frequency_band']
        property_names = ['fractional_resolution',
                          'creation_date',
                          'is_measured',
                          'measurement_date',
                          'version',
                          'aircraft_power_setting',
                          'aircraft_power_setting_units',
                          'ref_temperature',
                          'ref_pressure',
                          'ref_humidity',
                          'ref_measurement_distance',
                          'min_freq_band',
                          'max_freq_band']

        #   Create the tree and the root element
        root = xml.etree.ElementTree.Element("sound_pressure_level_harmonic_series_definition")

        #   Loop through the attributes/properties and add them to the root node
        for i in range(len(attribute_names)):
            value = getattr(self, property_names[i])

            if not isinstance(value, str):
                if isinstance(value, Length):
                    value = str(value.meters)
                elif isinstance(value, Temperature):
                    value = str(value.kelvin)
                elif isinstance(value, Pressure):
                    value = str(value.kilopascal)
                elif isinstance(value, Humidity):
                    value = str(value.percentage)
                else:
                    value = str(value)

            root.attrib[attribute_names[i]] = value

        #   Now create the node that will hold the coefficient definitions.
        series_collection = xml.etree.ElementTree.SubElement(root, "frequency_definitions")

        #   Loop through the series collection within the class and build the nodes. Then add the nodes to this node
        for coefficients in self.series_coefficients:
            coefficients.make_xml(series_collection)

        return root

    def save(self, a: str = None):
        """
        Write the data to an XML file
        :param a: str - the path to the output file
        """

        tree = xml.etree.ElementTree.ElementTree(self.make_xml())
        tree.write(file_or_filename=a, xml_declaration=True, encoding="utf-8")

    def predict(self, location):
        """
        This function calculates the sound pressure level at a specific location and returns the entire spectrum
        :param location: SphericalCoordinate
            it is either the specific location on the surface as defined in Cartesian or spherical coordinates or the
            azimuthal angle
        :return: double, array-like
            the sound pressure level @ all frequencies within the definition
        """

        #   We expect that the user will want the complete set of information at the specific location that is
        #   provided as an argument. So we will create an array of values for each element in the collection of
        #   series coefficients.
        if isinstance(location, SphericalCoordinate):
            spl = np.zeros((len(self.series_coefficients), 1))
        else:
            spl = np.zeros((len(self.series_coefficients), len(location)))

        #   Loop through the series approximations and create the list of values that each creates.
        for i in range(len(self.series_coefficients)):
            spl[i, :] = self.series_coefficients[i].predict(location)

        return spl.transpose()

    @staticmethod
    def fit(x, y, maximum_order: int = 9):
        """
        This function expects the X values to be a single dimension array of SphericalCoordinate locations that will
        be transformed into a collection of angles. The y values must be a collection of 1-D data the same length as
        the x values. If y has a second dimension, then it will be iterated through and a number of series expansions
        will be created
        :param x: Numpy.ndarray of SphericalCoordinate objects
            This is a collection of the known locations on the spherical surface. At this point, the radius is ignored
        :param y: Numpy.ndarray
            A single or double dimensioned array that will be used to define the radial value of the harmonic series
            expansion.
        :param maximum_order: int
            The maximum order of fitting that will be accomplished
        """

        series = HarmonicSpectrumNoiseSource()

        #   ensure that the inputs are correct
        if not isinstance(x, np.ndarray):
            x = np.asarray(x)
        if not isinstance(x, np.ndarray) or not isinstance(x[0], SphericalCoordinate):
            raise ValueError("You must provide an array of SphericalCoordinate objects for the x argument")

        if x.shape[0] != y.shape[0]:
            raise ValueError("The first dimension of the x and y arrays must be the same!")

        #   Now loop through the second dimension of the y values
        if len(y.shape) == 1:
            series.series_coefficients.append(HarmonicSeries.fit(x, y, maximum_order))
        else:
            for i in range(y.shape[1]):
                series.series_coefficients.append(HarmonicSeries.fit(x, y[:, i], maximum_order))

        return series


class InterpolatedHarmonicSpectrumNoiseSource(ISphereSource):
    """
    We understand the data collected at Owens-Corning can construct a surface for the acoustic emissions on the surface
    of a sphere.  The Static_NoiseSource class represents a single engine power value for the definition of the source.
    This provides the user with the interface to determine the source description at specific engine power settings.

    20220330 - FSM - Added properties to average the reference conditions across the low and high power settings
    20230726 - FSM - Updated the inheritance for the class structure
    """

    def __init__(self, filename: str = None):
        """
        This constructs the source definition for the interpolated static source description of the acoustic emissions
        for SUAS.
        :param filename: str - the path to the file that contains the definition
        """
        super().__init__()

        self.definitions = list()
        self._low_power = None
        self._high_power = None
        self._max_power = None
        self._name = None
        self.desired_power_setting = None
        self.SOURCE_DESCRIPTION_ERROR = "The low and high power settings must be HarmonicNoiseSource"

        if filename is None:
            return

        self.filename = filename

        tree = xml.etree.ElementTree.ElementTree()
        tree.parse(filename)

        #   Get the parameters for the definition from the root's attributes

        root = tree.getroot()

        self._low_power = float(root.attrib['lo_definition'])
        self._high_power = float(root.attrib['hi_definition'])
        self._max_power = float(root.attrib['max_definition'])
        self._name = root.attrib['name']
        self.desired_power_setting = self._low_power

        for defs in root[0]:
            self.definitions.append(HarmonicSpectrumNoiseSource(defs))

    @property
    def source_name(self):
        return self._name

    @source_name.setter
    def source_name(self, value):
        self._name = value

    @property
    def low_power_setting(self):
        return self.low_power_description.aircraft_power_setting

    @property
    def high_power_setting(self):
        return self.high_power_description.aircraft_power_setting

    @property
    def maximum_power_setting(self):
        return self.maximum_power_description.aircraft_power_setting

    @property
    def low_power_engine_parameter(self):
        return self._low_power

    @low_power_engine_parameter.setter
    def low_power_engine_parameter(self, value):
        self._low_power = value

    @property
    def hi_power_engine_parameter(self):
        return self._high_power

    @hi_power_engine_parameter.setter
    def hi_power_engine_parameter(self, value):
        self._high_power = value

    @property
    def max_power_engine_parameter(self):
        return self._max_power

    @max_power_engine_parameter.setter
    def max_power_engine_parameter(self, value):
        self._max_power = value

    @property
    def low_power_description(self):
        tmp = None

        for definition in self.definitions:
            if definition.aircraft_power_setting == self._low_power:
                tmp = definition
                break

        if tmp is not None:
            return tmp
        else:
            raise ValueError("The low power setting conditions could not be found in the collection of definitions")

    @property
    def high_power_description(self):
        tmp = None

        for definition in self.definitions:
            if definition.aircraft_power_setting == self._high_power:
                tmp = definition
                break

        if tmp is not None:
            return tmp
        else:
            raise ValueError("The high power setting conditions could not be found in the collection of definitions")

    @property
    def maximum_power_description(self):
        tmp = None

        for definition in self.definitions:
            if definition.aircraft_power_setting == self._max_power:
                tmp = definition
                break

        if tmp is not None:
            return tmp
        else:
            raise ValueError("The maximum power setting conditions could not be found in the collection of definitions")

    @property
    def static_definitions(self):
        return self.definitions

    @static_definitions.setter
    def static_definitions(self, value):
        self.definitions = value

    @property
    def desired_engine_power(self):
        return self.desired_power_setting

    @property
    def ref_temperature(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_temperature + self.high_power_description.ref_temperature) / 2

    @property
    def ref_pressure(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_pressure + self.high_power_description.ref_pressure) / 2

    @property
    def ref_humidity(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_humidity + self.high_power_description.ref_humidity) / 2

    @property
    def ref_distance(self):
        if not (isinstance(self.low_power_description, HarmonicSpectrumNoiseSource) and
                isinstance(self.high_power_description, HarmonicSpectrumNoiseSource)):
            return ValueError(self.SOURCE_DESCRIPTION_ERROR)
        return (self.low_power_description.ref_measurement_distance +
                self.high_power_description.ref_measurement_distance) / 2

    @desired_engine_power.setter
    def desired_engine_power(self, value):
        import warnings

        if value < self.low_power_setting:
            self.desired_power_setting = self.low_power_setting

            warnings.warn("The desired engine power setting was below the minimum within the definition.  The value "
                          "was reset to the lowest value in the definition")
        elif value > self.maximum_power_setting:
            self.desired_power_setting = self.maximum_power_setting

            warnings.warn("The desired engine power setting was above the maximum within the definition.  The value "
                          "was reset to the maximum value in the definition")
        elif (value > self.high_power_setting) and (value < self.maximum_power_setting):
            self.desired_power_setting = self.maximum_power_setting

            warnings.warn("The value was above the interpolation range for this aircraft definition.  The source "
                          "description used will be the maximum definition.")
        else:
            self.desired_power_setting = value

    def predict(self, location):
        """
        This function calculates the sound pressure level at a specific location and returns the entire spectrum
        :param location: SphericalCoordinate
            it is either the specific location on the surface as defined in Cartesian or spherical coordinates or the
            azimuthal angle
        :return: double, array-like
            the sound pressure level @ all frequencies within the definition
        """
        import numpy as np

        if self.desired_power_setting > self.high_power_setting:
            return self.maximum_power_description.predict(location)
        else:
            #   Determine the weighting function or the two coefficients
            lo_definition = self.low_power_description
            hi_definition = self.high_power_description

            w_lo = 1 + (self.desired_power_setting - lo_definition.aircraft_power_setting) / \
                   (lo_definition.aircraft_power_setting - hi_definition.aircraft_power_setting)
            w_hi = 1 - w_lo

            #   Determine the locations for the determination of the harmonic coefficient matrix
            spl = np.zeros((len(self.definitions[0].series_coefficients), 1))

            for i in range(len(spl)):
                #   Build the matrix that we will use to determine the real values after creating the interpolated
                #   coefficients.
                b = HarmonicSeries.harmonic_matrix(
                    self.low_power_description.series_coefficients[i].order,
                    azimuthal=location.azimuthal,
                    polar=location.polar)

                #   Use the weights to determine the linear combination of the coefficients
                c_lo = self.low_power_description.series_coefficients[i]
                c_hi = self.high_power_description.series_coefficients[i]

                c = w_lo * c_lo.coefficients + w_hi * c_hi.coefficients

                spl[i] = (b.dot(c))[0].real

        return spl

    def save(self, filename: str):
        """
        This function creates the source file description using the information within the class.  It uses the functions
        from the static source to build the tree for the individual definitions.

        :param filename: string - the path to write the output
        """

        root = xml.etree.ElementTree.Element("interpolated_harmonic_series_definition")

        #   Build the interpolated source definition tree
        root.set("name", self.source_name)
        root.set("lo_definition", str(self.low_power_engine_parameter))
        root.set("hi_definition", str(self.hi_power_engine_parameter))
        if self._max_power is not None:
            root.set("max_definition", str(self._max_power))
        else:
            root.set("max_definition", str(self.hi_power_engine_parameter))

        definition_set = xml.etree.ElementTree.SubElement(root, "definitions")
        for definition in self.definitions:
            definition_set.append(self.definitions[i].m)

        #   Set the root of the tree and write the structure to the output file

        tree._setroot(interp_src)

        print(tree)
        tree.write(filename, encoding="UTF-8", xml_declaration=True)



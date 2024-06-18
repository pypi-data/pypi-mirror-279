from PythonCoordinates.measurables.physical_quantities import Speed, Angle, Length
from PythonCoordinates.measurables.Measurable import InvalidUnitOfMeasureException
from PythonCoordinates.coordinates.coordinate_representations import CartesianCoordinate, SphericalCoordinate
from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools as fob
import numpy as np
from physical_sources.acoustic.inoisesource import INoiseSource
import abc


class IAnalyticSource(INoiseSource):
    """
    This Interface base class defines the collection of information that is required for the analytic methods of
    determining value of an acoustic metric at a specific spherical location.
    """

    @abc.abstrcatmethod
    def predict(self, location: SphericalCoordinate):
        """
        This function employs the internal representation of the coefficients of the analytic function.

        :param location:
            This is the location on a sphere inscribed around the source where we want to evaluate the acoustic metric.
        """
        raise NotImplementedError()


class IdealDipoleX(IAnalyticSource):
    """
    This class implements the equation from Dr. Frank Mobley's dissertation that defines an acoustic dipole with an
    arbitrary rotation about the z-axis. It provides methods to alter the strength and frequency of the dipole so that
    a series of sound pressure levels can be obtained for any spherical angle.
    """

    def predict(self, location: SphericalCoordinate):
        """
        Given a location on the surface of the directivity pattern, this will determine the sound pressure leve at each
        of the frequencies within the frequency list.

        :param location:
            SphericalCoordinate - the first location of the point that we want to process
        :returns: np.ndarray - a collection of sound pressure levels for the location given
        """

        spl = np.zeros((len(self._frequency), ))

        if not isinstance(location, SphericalCoordinate):
            raise InvalidUnitOfMeasureException("You must provide the location of the point in SphericalCoordinate")

        for i in range(len(self._frequency)):
            wavelength = self._sound_speed.meters_per_second / self._frequency[i]
            k = 1 / wavelength
            w = 2 * np.pi * self._frequency[i]

            c_pressure = -complex(0, self._amplitude * k * self._separation / self.reference_distance.meters)
            c_pressure *= complex(np.cos(w * self._time - k * self.reference_distance.meters),
                                  np.sin(w * self._time - k * self.reference_distance.meters))
            c_pressure *= np.cos(location.polar) * np.sin(location.azimuthal)
            pressure = abs(c_pressure)

            spl[i] = 20 * np.log10(pressure / 20e-6)

        return spl

    def __init__(self, dipole_separation: float = 0.001, amplitude: float = 0.1,
                 sound_speed: Speed = Speed.ref_speed_of_sound(), frequency: np.ndarray = fob.tob_frequencies()):
        """
        This constructor defines the initial conditions for the dipole class

        :param dipole_separation: float
            the distance between the two monopoles that form the dipole
        :param amplitude: float
            the strength of both monopoles
        :param sound_speed: Speed
            This is the nominal speed of sound for the determination of the wave number
        """

        self._separation = dipole_separation
        self._amplitude = amplitude
        self._sound_speed = sound_speed
        self._frequency = frequency
        self.name = "Dr. Mobley's Ideal Dipole (X-axis orientation)"
        self.minimum_frequency_band = self._frequency[0]
        self.maximum_frequency_band = self._frequency[-1]
        self._time = 0

    @property
    def calculation_time(self):
        return self._time

    @calculation_time.setter
    def calculation_time(self, value):
        self._time = value


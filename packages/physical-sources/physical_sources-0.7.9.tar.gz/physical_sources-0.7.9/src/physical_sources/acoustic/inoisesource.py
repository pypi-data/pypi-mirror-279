import abc
from PythonCoordinates.coordinates.coordinate_representations import SphericalCoordinate
from PythonCoordinates.measurables.physical_quantities import Length


class INoiseSource:
    @abc.abstractmethod
    def predict(self, location: SphericalCoordinate):
        """
        This function will utilize the information within the class to predict the acoustic metric at the specific
        emission location on the surface of the definition.

        :param location:
            This is the emission location. It is defined on the surface of a sphere inscribed around the source.

        :returns:
            A specific value, or set of values, at the specific location.
        """

        raise NotImplementedError()

    def __init__(self):
        """
        A constructor for the generic interface to the acoustic source descriptions
        """
        pass

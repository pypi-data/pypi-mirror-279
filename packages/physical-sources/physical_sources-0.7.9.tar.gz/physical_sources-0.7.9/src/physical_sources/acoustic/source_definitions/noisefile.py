from physical_sources.acoustic.point_source import FlightPointSource, GroundPointSource, AircraftType


class FlightNoiseFileDatabase:
    def __init__(self, filename):
        """
        This constructor will load the entire noise database from the flight01.dat file that is passed to the
        constructor
        :param filename: str - the path to the NOISEFILE database which we want to load
        """
        self.filename = filename
        self.sources = []
        with open(filename, 'r') as f:
            contents = f.readlines()
        line_index = 0
        while line_index < len(contents):
            src_data = FlightPointSource()
            try:
                line_index = src_data._load_data(contents, line_index)
            except Exception as eee:
                raise ValueError('An incorrect formatted NOISEFILE entry found at index {}: {}'.format(
                    line_index, str(eee)))
            self.sources.append(src_data)

    def get_sources(self, id: int, ac_type: AircraftType = AircraftType.Military) -> list:
        """
        This function will extract all the elements of the database that possess the specific aircraft_id that is passed
        to the function.

        :param id:
            the integer id for the aircraft that we want to extract

        :returns:
            A list of the aircraft with the specific id that was provided to the function
        """

        sources = [x for x in self.sources if (x.aircraft_id == id) & (x.vehicle_type == ac_type)]

        return sources

class GroundNoiseFileDatabase:
    def __init__(self, path):
        """
        This will read a file with multiple NOISEFILE_Static_AcousticSource definition in a single file and place the
        elements into an internal array
        """

        self.filename = path
        self.sources = []

        with open(self.filename, 'rt') as f:
            contents = f.readlines()

        line_index = 0

        while line_index < len(contents):
            src_data = GroundPointSource()
            try:
                line_index = src_data._load_data(contents, line_index)
            except Exception as eee:
                raise ValueError("An incorrect formatted NOISEFILE entry found at index {}: {}".format(
                    line_index, str(eee)
                ))

            self.sources.append(src_data)
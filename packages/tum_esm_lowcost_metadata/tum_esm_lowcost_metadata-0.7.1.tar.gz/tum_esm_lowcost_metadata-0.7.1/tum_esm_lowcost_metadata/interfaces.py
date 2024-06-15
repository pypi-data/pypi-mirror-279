import json
import tum_esm_utils
import tum_esm_lowcost_metadata.types as types
import pendulum
import typing
import pydantic


class Interface:
    """Query interface for the metadata."""

    def __init__(
        self,
        samples: types.SampleDocument,
        sensors: types.SensorDocument,
        sites: types.SiteDocument,
    ):
        self.samples, self.sensors, self.sites = samples, sensors, sites
        # sort samples list by sampling_start datetime
        samples.sort(key = lambda x: x.sampling_start, reverse = True)

    def get(
        self, sensor_id: types.SensorIdentifier, timestamp: pendulum.DateTime
    ) -> types.MetaData:
        """Returns the metadata for the given sensor that was active at the given timestamp."""
        
        sensor = self.sensors.get(sensor_id)
        assert sensor is not None, f"Sensor {sensor_id} not found"
        
        # Find the sample that was active at the given timestamp
        # iterate through the whole sampling history of the sensor
        sample = None
        for element in self.samples:
            
            # find latest sampling event for sensor with given sensor id
            if (
                (element.sensor_ids == "all" or (sensor_id in element.sensor_ids)) # does the sampling event concern the sensor?
                and (element.sampling_start <= timestamp)):
                
                # now look at the most recent sampling event
                if ((element.sampling_end is None) or (timestamp <= element.sampling_end)): #does the sampling end happen after timestamp?
                    sample = element
                    break
                else: 
                    break
                    
        assert sample is not None, f"No active sampling event for sensor {sensor_id} at {timestamp}"
        
        # Find the corresponding site
        site = self.sites.get(sample.site_id)
        assert site is not None, f"Site {sample.site_id} not found"
        
        # Join the sample, sensor, and site and return
        return types.MetaData(
            site_id=sample.site_id,
            site_type=site.site_type,
            site_lat=site.site_lat,
            site_lon=site.site_lon,
            elevation=site.elevation,
            site_comment=site.comment,
            sensor_id=sensor_id,
            sensor_type=sensor.sensor_type,
            sensor_make=sensor.sensor_make,
            sensor_model=sensor.sensor_model,
            start_up_date=sensor.start_up_date,
            shut_down_date=sensor.shut_down_date,
            sensor_comment=sensor.comment,
            sampling_since = sample.sampling_start,
            sampling_until= sample.sampling_end,
            orientation=sample.orientation,
            elevation_ag=sample.elevation_ag,
            radiation_shield=sample.radiation_shield,
            sampling_comment=sample.comment,
        )
        
        
def print_beautiful(metadata:types.MetaData) -> None:
    """Prints metadata in a more accessible way."""
    
    m = metadata
    print(f"\nMetadata for Sensor {m.sensor_id}, located at {m.site_id}.")
    print(f"---")
    print(f"Sensor type: \t\t{m.sensor_make} {m.sensor_model}")
    print(f"Site coordinates: \t{m.site_lat} lat")
    print(f"\t\t\t{m.site_lon} lon")
    print(f"\t\t\t{m.elevation} m a.s.l.")
    print(f"Site type: \t\t{m.site_type}")
    print(f"Radiation shield: \t{m.radiation_shield}")
    print(f"Sampling since: \t{m.sampling_since}")
    if m.sampling_until is not None: print(f"Sampling until: \t{m.sampling_until}")
    print(f"Orientation \t\t{m.orientation}°")
    print(f"Elevation above ground:\t{m.elevation_ag} m")

    comment_str = ''.join(map(lambda comm: (comm+"\n\t\t\t"), 
                              filter(lambda i: len(i)>1, [m.sensor_comment, m.site_comment, m.sampling_comment])))
    if len(comment_str)>2: print(f"Comments: \t\t{comment_str}")
    print(f"---")
    
    return None


def load_from_github(
    github_repository: str,
    access_token: str,
) -> Interface:
    """Downloads metadata from GitHub and provides a query interface."""
    
    _req: typing.Callable[[str], list[Any]] = lambda t: json.loads(
        tum_esm_utils.github.request_github_file(
            github_repository=github_repository,
            filepath=f"data/{t}.json",
            access_token=access_token,
        )
    )
    
    # Instantiate and return the interface
    return Interface(
        samples = pydantic.parse_obj_as(types.SampleDocument, _req("SAMPLING")),
        sensors = pydantic.parse_obj_as(types.SensorDocument, _req("SENSORS")), 
        sites = pydantic.parse_obj_as(types.SiteDocument, _req("SITES")),
        )

# Lowcost Metadata

This repository handles the metadata around the lowcost sensor network in Munich.<br/>
We selected this format over putting it in a database due to various reasons:

-   Easy to read, modify and extend by selective group members using GitHub permissions
-   Changes to this are more obvious here than in database logs
-   Versioning (easy to revert mistakes)
-   Automatic testing of the files integrities
-   Easy import as a statically typed Python library

<br/>

## What does this data look like?

There is a set of **`JSON`** files in the data folder holding the follwing information:

- **`SENSORS.json`**<br/>
This files contains basic information about the sensors in use in the monitoring network.
```json
{
    "13077": {
        "sensor_type": "LP8",
        "sensor_make": "Decentlab",
        "sensor_model": "DL-LP8",
        "start_up_date": "2022-08-01T08:00:00+00:00",
        "shut_down_date": null,
        "comment": ""
    },
}
```
- **`SITES.json`**<br/>
This file contains basic information about the sites/locations where sensors have been installed.

```json
{
    "FREV": {
        "site_type": "individual",
        "site_lat": 48.1615591,
        "site_lon": 11.5860387,
        "elevation": 514,
        "comment": "Lamp post ids:55.0"
    },
}
```
- **`SAMPLING.json`**<br/>
This file contains basic information on which site, at which time, which sensors measured at which configuration. A new key "radiation_shield" was added with version 0.7 as all sensors will be deployed within radiation shieling in near future.

```json
[
    {
        "site_id": "HANV",
        "sensor_ids": [
            13171,
            13147
        ],
        "sampling_start": "2023-05-02T12:30+02:00",
        "sampling_end": null,
        "orientation": 0,
        "elevation_ag": 3,
        "comment": "", 
        "radiation_shield": false
    },
]
```

<br/>

## How to add new measurement days?

1. Possibly add new sensor in `data/SENSORS.json`
2. Possibly add new site in `data/SITES.json`
2. Add a new sampling event to `data/SAMPLING.json`

If necessary, use this tool to find the elevation of a certain location: <url>https://www.calcmaps.com/map-elevation/</url>
<br/>

## How can I know whether my changes were correct?

Whenever you make changes in the repository on GitHub, the integrity of the files will automatically be checked. You can check whether all tests have passed [here](https://github.com/tum-esm/lowcost-metadata/actions).

A list of all integrity checks can be found in [`tests/README.md`](https://github.com/tum-esm/lowcost-metadata//tree/main/tests).

<br/>

## How to use it in your codebase?

1. Install python library

```bash
poetry add tum_esm_lowcost_metadata
# or
pip install tum_esm_lowcost_metadata
```

2. Create a personal access token for a GitHub account that has read access to the metadata repository: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

3. Use the metadata anywhere

```python
import tum_esm_lowcost_metadata

lowcost_metadata_interface = tum_esm_lowcost_metadata.load_from_github(
    github_repository = "org-name/repo-name",
    access_token = "ghp_..."
)

metadata = lowcost_metadata_interface.get(
    sensor_id = "13077", date = pendulum.datetime(2023, 6, 6)
)  # is of type list[tum_esm_lowcost_metadata.types.SensorDataContext]

metadata = interface.get(sensor_id = '13155', timestamp=pendulum.datetime(2023, 6, 6))
interfaces.print_beautiful(metadata))
```

... prints out:

```
Metadata for Sensor 13155, located at MOSV.
---
Sensor type:            Decentlab DL-LP8
Site coordinates:       48.1870436 lat
                        11.5622708 lon
                        508.0 m a.s.l.
Orientation             0.0°
Elevation above ground: 3.0 m
Comment:                Lamp post ids:32.0

---
```

<br/>

## For Developers: Publish the Package to PyPI

```bash
poetry build
poetry publish
```

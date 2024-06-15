import pendulum
import pydantic
import typing


####################################################################################################
# Custom BaseModel with some sensible defaults
####################################################################################################


class _BaseModel(pydantic.BaseModel):
    class Config:
        extra = "forbid"
        allow_mutation = False


####################################################################################################
# Custom data types
####################################################################################################


SiteIdentifier = pydantic.constr(regex="^[A-Z]{4}$")
SensorIdentifier = pydantic.constr(max_length=16)


####################################################################################################
# Pydantic models
####################################################################################################


class Sample(_BaseModel):
    site_id: SiteIdentifier
    sensor_ids: typing.Union[
        pydantic.conlist(item_type=SensorIdentifier, min_items=1, unique_items=True),
        typing.Literal["all"],
    ]
    sampling_start: pendulum.DateTime
    sampling_end: typing.Optional[pendulum.DateTime] = ...  # Can be None, but must be set
    orientation: pydantic.confloat(ge=0, le=360)
    elevation_ag: pydantic.confloat(ge = 0, le = 300)
    comment: pydantic.constr(max_length=256)
    radiation_shield: bool


class Site(_BaseModel):
    #site_id: SiteIdentifier
    site_type: typing.Literal[
        "individual",
        "lfu_colocation",
        "midcost_colocation",
        "reference_colocation",
        "lc_aq_colocation",
        "climate_chamber",
    ]
    site_lat: pydantic.confloat(ge = -90, le = 90)
    site_lon: pydantic.confloat(ge = -180, le = 180)
    elevation: pydantic.confloat(ge = 0, le = 8000)
    comment: pydantic.constr(max_length=256)


class Sensor(_BaseModel):
    #sensor_id: SensorIdentifier
    sensor_type: pydantic.constr(max_length=32)
    sensor_make: pydantic.constr(max_length=32)
    sensor_model: pydantic.constr(max_length=32)
    start_up_date: pendulum.DateTime
    shut_down_date: typing.Optional[pendulum.DateTime] = ...
    comment: pydantic.constr(max_length=256)


class MetaData(_BaseModel):
    site_id: SiteIdentifier
    site_type: typing.Literal[
        "individual",
        "lfu_colocation",
        "midcost_colocation",
        "reference_colocation",
        "lc_aq_colocation",
        "climate_chamber",
    ]
    site_lat: pydantic.confloat(ge = -90, le = 90)
    site_lon: pydantic.confloat(ge = -180, le = 180)
    elevation: pydantic.confloat(ge = 0, le = 8000)
    site_comment: pydantic.constr(max_length=256)
    sensor_id: SensorIdentifier
    sensor_type: pydantic.constr(max_length=32)
    sensor_make: pydantic.constr(max_length=32)
    sensor_model: pydantic.constr(max_length=32)
    start_up_date: pendulum.DateTime
    shut_down_date: typing.Optional[pendulum.DateTime] = ...
    sensor_comment: pydantic.constr(max_length=256)
    sampling_since: pendulum.DateTime
    sampling_until: typing.Optional[pendulum.DateTime] = ...
    orientation: pydantic.confloat(ge=0, le=360)
    elevation_ag: pydantic.confloat(ge = 0, le = 300)
    radiation_shield: bool
    sampling_comment: pydantic.constr(max_length=256)

####################################################################################################
# Document models
####################################################################################################


SampleDocument = list[Sample]
SiteDocument = dict[SiteIdentifier, Site]
SensorDocument = dict[SensorIdentifier, Sensor]

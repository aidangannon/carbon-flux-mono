import pandas as pd
from icoscp import cpauth
from icoscp_core.icos import bootstrap, ATMO_STATION

meta, data = bootstrap.fromCredentials("aidanwilliamgannon@gmail.com", "2b6J6nohx9RZKLM")
cpauth.init_by(data.auth)
print(data.auth)

# Swedish atmospheric stations whose metadata is supplied to the Carbon Portal
# by the Atmospheric Thematic Center
se_atmo_stations = [
    s for s in meta.list_stations(ATMO_STATION)
    if s.country_code=='SE'
]

# Find basic metadata for CO2 release data sampled at at least 100 m above the ground
se_co2_from_100 = [
    dobj for dobj in meta.list_data_objects(
        # URL for official ICOS CO2 molar fraction release data
        datatype='http://meta.icos-cp.eu/resources/cpmeta/atcCo2L2DataObject',
        station=se_atmo_stations
    )
    if dobj.sampling_height >= 100
]

# prepare an empty pandas DataFrame to merge the data into
merged_co2 = pd.DataFrame(columns=['TIMESTAMP', 'co2'])

# batch-fetch the interesting columns and iterate through the results
for dobj, arrs in data.batch_get_columns_as_arrays(se_co2_from_100, ['TIMESTAMP', 'co2']):
    st_uri = dobj.station_uri
    # ICOS atmospheric station URIs end with underscore followed by a 3-letter station ID
    # this ID is convenient to use as a suffix to rename 'co2' with
    station_id = st_uri[st_uri.rfind('_'):]
    df = pd.DataFrame(arrs)
    # next line would be needed if `keep_bad_data` flag in batch_get_columns_as_arrays was set to True
    #df.loc[df['Flag'] != 'O', 'co2'] = np.nan
    del df['Flag']
    merged_co2 = pd.merge(merged_co2, df, on='TIMESTAMP', how='outer', suffixes=('', station_id))
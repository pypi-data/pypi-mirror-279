def regions(region):
    """
    This function takes the name of a geographic region and returns the associated geographic coordinates for that region.

    Arguments:
    region (str): The name of the geographic region.

    Returns:
    str: A string containing the geographic coordinates in the format "LAT1_LAT2,LON1_LON2".
    """

    if region == 'PoleNord':
        latlons = (60, 90, -180, 180)
    elif region == 'PoleSud':
        latlons = (-90, -60, -180, 180)
    elif region == 'AmeriqueduNord':
        latlons = (25, 60, -145, -50)
    elif region == 'OuestAmeriqueduNord':
        latlons = (25, 60, -145, -97.5)
    elif region == 'AmeriqueDuNordPlus':
        latlons = (25, 85, -170, -40)
    elif region == 'Monde':
        latlons = (-90, 90, -180, 180)
    elif region == 'Global':
        latlons = (-90, 90, -180, 180)
    elif region == 'ExtratropiquesNord':
        latlons = (20, 90, -180, 180)
    elif region == 'ExtratropiquesSud':
        latlons = (-90, -20, -180, 180)
    elif region == 'HemisphereNord':
        latlons = (0, 90, -180, 180)
    elif region == 'HemisphereSud':
        latlons = (-90, 0, -180, 180)
    elif region == 'Asie':
        latlons = (25, 60, 65, 145)
    elif region == 'Europe':
        latlons = (25, 70, -10, 28)
    elif region == 'Mexique':
        latlons = (15, 30, -130, -60)
    elif region == 'Canada':
        latlons = (45, 90, -151, -50)
    elif region == 'BaieDhudson':
        latlons = (55, 90, -90, -60)
    elif region == 'Arctiquecanadien':
        latlons = (58, 90, -141, -50)
    elif region == 'EtatsUnis':
        latlons = (25, 45, -130, -70)
    elif region == 'SudestEtatsUnis':
        latlons = (25, 40, -100, -70)
    elif region == 'EstAmeriqueduNord':
        latlons = (25, 60, -97.5, -50)
    elif region == 'EstAmeriqueduNordPlus':
        latlons = (25, 85, -97.5, -50)
    elif region == 'OuestAmeriqueduNordPlus':
        latlons = (25, 85, -170, -97.5)
    elif region == 'Tropiques30':
        latlons = (-30, 30, -180, 180)
    elif region == 'Tropiques':
        latlons = (-20, 20, -180, 180)
    elif region == 'Australie':
        latlons = (-55, -10, 90, 180)
    elif region == 'Pacifique':
        latlons = (20, 65, 130, -150)
    elif region == 'Atlantique':
        latlons = (20, 65, -80, -1)
    elif region == 'Alaska':
        latlons = (50, 75, -180, -140)
    elif region == 'HIMAPEst':
        latlons = (35, 65, -105, -50)
    elif region == 'HIMAPOuest':
        latlons = (40, 65, -145, -100)
    elif region == 'ExtremeSud':
        latlons = (-90, -87, -180, 180)
    elif region == 'ExtremeNord':
        latlons = (87, 90, -180, 180)
    elif region == 'TropiquesOuest':
        latlons = (-20, 0, 180, -90)
    elif region == 'Bande60a90':
        latlons = (60, 90, -180, 180)
    elif region == 'Bande30a60':
        latlons = (30, 60, -180, 180)
    elif region == 'Bande00a30':
        latlons = (0, 30, -180, 180)
    elif region == 'BandeM30a00':
        latlons = (-30, 0, -180, 180)
    elif region == 'BandeM60aM30':
        latlons = (-60, -30, -180, 180)
    elif region == 'BandeM90aM60':
        latlons = (-90, -60, -180, 180)
    elif region == 'Rapidscat':
        latlons = (-55, 55, -180, 180)
    elif region == 'npstere':
        latlons = (0, 90, -180, 180)
    elif region == 'spstere':
        latlons = (-90, 0, -180, 180)
    else:
        raise ValueError(f'Región desconocida: {region}')
    
    LAT1, LAT2, LON1, LON2 = latlons
    LATLONS = f"{LAT1}_{LAT2},{LON1}_{LON2}"
    
    return latlons

def generate_latlon_criteria(LAT1, LAT2, LON1, LON2):
    """
    This function generates a filtering criteria expression based on latitude and longitude coordinates.

    Arguments:
    LAT1 (float): The starting latitude.
    LAT2 (float): The ending latitude.
    LON1 (float): The starting longitude.
    LON2 (float): The ending longitude.

    Returns:
    str: A filtering criteria expression.
    """
    relatopLAT = '<=' if LAT2 == 90 else '<'
    relatopLON = '<=' if LON2 == 180 else '<'

    if LON1 >= LON2:
        LATLONCRIT = (
            f" and lat >= {LAT1} and lat {relatopLAT} {LAT2} "
            f" and ((lon >= 0. and lon < {LON2}) or (lon >= {LON1} and {LON1} < 179.99))"
        )
    else:
        LATLONCRIT = (
            f" and lat >= {LAT1} and lat {relatopLAT} {LAT2} "
            f" and lon >= {LON1} and lon {relatopLON} {LON2}"
        )

    return LATLONCRIT

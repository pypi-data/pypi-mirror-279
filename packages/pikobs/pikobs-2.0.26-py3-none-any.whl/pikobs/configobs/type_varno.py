def type_varno(varno):
    GRAPHE_NOMVAR = {
        '11215': ('U COMPONENT OF WIND (10M)', '[m/s]', 'review type_varno.py'),
        '11216': ('V COMPONENT OF WIND (10M)', '[m/s]', 'review type_varno.py'),
        '12004': ('DRY BULB TEMPERATURE AT 2M', '','review type_varno.py'),
        '10051': ('PRESSURE REDUCED TO MEAN SEA LEVEL', '','review type_varno.py'),
        '10004': ('PRESSURE', '','review type_varno.py'),
        '12203': ('DEW POINT DEPRESSION (2M)', '','review type_varno.py'),
        '12001': ('TEMPERATURE/DRY BULB', '','review type_varno.py'),
        '11003': ('U COMPONENT OF WIND', '[m/s]','review type_varno.py'),
        '11004': ('V COMPONENT OF WIND', '[m/s]','review type_varno.py'),
        '12192': ('DEW POINT DEPRESSION', '','revieaw type_varno.py'),
        '12163': ('BRIGHTNESS TEMPERATURE', '[K]', 'Channel'),
        '21014': ('Doppler velocity', '[m/s]', 'Height'),
        '15036': ('ATMOSPHERIC REFRACTIVITY', '','review type_varno.py'),
        '11001': ('WIND DIRECTION', '','review type_varno.py'),
        '11002': ('WIND SPEED', '','review type_varno.py'),
        '11011': ('WIND DIRECTION AT 10M', '','review type_varno.py'),
        '11012': ('WIND SPEED AT 10M', '[m/s]','review type_varno.py')
    }

    # Check if the variable number is in the dictionary
    if varno in GRAPHE_NOMVAR:
        # If it is, retrieve the variable name and units
        variable_name, units, vcoord_type = GRAPHE_NOMVAR[varno]
        # Return the variable name along with its units
        return variable_name, units, vcoord_type
    else:
        # If the variable number is not found, return a message indicating so
        raise ValueError("Varno  not found")        

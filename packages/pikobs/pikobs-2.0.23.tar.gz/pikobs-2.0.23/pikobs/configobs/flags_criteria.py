def flag_criteria(flags):
    """
    This function generates a filtering criteria expression based on flag selection.

    Arguments:
    flags (str): The selected flag option ('all', 'rejets', 'assim', 'qc', 'bias_corr', or 'obsselectionflags').

    Returns:

    str: A filtering criteria expression.
    """
    #12 	4096	AO	1	Élément assimilé (c'est-à-dire ayant influencé l'analyse)
    #11 	2048	AO	2	Élément rejeté par un processus de sélection (thinning ou canal)
    #10 	1024	AO	3	Élément généré par l'AO
    #9  	512	AO	4	Élément rejeté par le contrôle de la qualité de l'AO (Background Check ou QC-Var)
    #8  	256	AO	5	Élément rejeté parce qu'il est sur une liste noire
    #7  	128	DERIV	6	En réserve
    #6  	64	DERIV	7	Élément corrigé par la séquence DERIVATE ou correction de biais
    #5  	32	DERIV	8	Élément interpolé, généré par DERIVATE
    #4  	16	DERIV	9	Élément douteux
    #3  	8	ADE	10	Élément peut-être erroné
    #2  	4	ADE	11	Élément erroné
    #1  	2	ADE	12	Élément qui excède un extrême climatologique (ou) qui ne passe pas le test de consistance
    #0  	1	ADE	13	Élément modifié ou généré par l'ADE
    BIT17_QCVAR=131072
    BIT12_VUE=4096 
    BIT18_ORO=262144
    BIT9_REJ=512
    BIT16_REJBGCK=65536
    BIT19_SURFACE=524288
    BIT11_SELCOR=2048  
    BIT7_REJ=128  
    BIT8_BLACKLIST=256

    if flags == "all":
        FLAG = " flag >= 0 "
    elif "assimilee":
        FLAG=f" and (flag & {BIT12_VUE})= {BIT12_VUE} "
    elif "bgckalt":
        FLAG=f" and (flag & {BIT9_REJ})=0 and (flag & {BIT11_SELCOR}=0 and (flag & {BIT8_BLACKLIST})=0 "
    elif "bgckalt_qc":
        FLAG=f" and (flag & {BIT9_REJ})=0 and (flag & {BIT11_SELCOR})=0 "
    elif "monitoring":
        FLAG=f" and (flag & {BIT9_REJ})= 0 and (flag & {BIT7_REJ})= 0 "
    elif "postalt":
        FLAG=f" and (flag & {BIT17_QCVAR})=0 and (flag & {BIT9_REJ})=0 and (flag & {BIT11_SELCOR})=0 and (flag & {BIT8_BLACKLIST})=0 "
    else:
        raise ValueError(f'Invalid flag option: {flags}')

    return FLAG

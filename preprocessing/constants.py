def getChannelNames():
    """Return Channels names."""
    return ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 
            'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 
            'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 'P7', 
            'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10']

def getEventNames():
    """Return Event name."""
    return ['HandStart', 'FirstDigitTouch', 'BothStartLoadPhase', 'LiftOff',
            'Replace', 'BothReleased']

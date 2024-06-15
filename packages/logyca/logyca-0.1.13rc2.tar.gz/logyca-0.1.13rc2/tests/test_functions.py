from logyca import convertDateTimeStampUTCtoUTCColombia

def test_convertDateTimeStampUTCtoUTCColombia():
    ts = 1571595618.0
    assert str(convertDateTimeStampUTCtoUTCColombia(ts))=='2019-10-20 13:20:18-05:00'  

from datetime import datetime, timezone
import pytz
from logyca.utils.constants.app import App

def convertDateTimeStampUTCtoUTCColombia(timestamp)->datetime:
    '''Description    
    Build a from url correctly
    :param timestamp:int: timestamp as timezone UTC
    :return datetime: datetime as timezone UTC(-5) Colombia
    '''
    timestamp_utc=datetime.fromtimestamp(timestamp, tz=timezone.utc)
    dateTimeColombia = timestamp_utc.astimezone(pytz.timezone(App.TimeZone.Colombia))
    return dateTimeColombia


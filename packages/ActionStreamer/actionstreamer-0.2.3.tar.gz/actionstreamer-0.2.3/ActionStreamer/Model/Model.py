from enum import Enum

class EventStatus(Enum):

    Checked_out = 2,
    Complete = 4,
    Error = 5,
    Pending = 1,
    Processing = 3,
    Timed_out = 6


class EventType:

    class Video(Enum):
        Start_bars = 9,
        Follow = 8,
        Receive_stream = 5,
        Start_recording = 1,
        Start_streaming = 3,
        Stop_bars = 10,
        Stop_receive_stream = 6,
        Stop_recording = 2,
        Stop_streaming = 4,
        Test_event = 7,
        Test_stop = 11


class Event:

    def __init__(self, key, userID, deviceID, agentTypeID, agentID, eventTypeID, eventStatus, eventParameters, result, percentComplete, priority, expirationEpoch, attemptNumber, maxAttempts, checkoutToken, tagString, tagNumber, creationDate, createdBy, lastModifiedDate, lastModifiedBy):

        self.eventID = key
        self.userID = userID
        self.deviceID = deviceID
        self.agentTypeID = agentTypeID
        self.agentID = agentID
        self.eventTypeID = eventTypeID
        self.eventStatus = eventStatus
        self.eventParameters = eventParameters
        self.result = result
        self.percentComplete = percentComplete
        self.priority = priority
        self.expirationEpoch = expirationEpoch
        self.attemptNumber = attemptNumber
        self.maxAttempts = maxAttempts
        self.checkoutToken = checkoutToken
        self.tagString = tagString
        self.tagNumber = tagNumber
        self.creationDate = creationDate
        self.createdBy = createdBy
        self.lastModifiedDate = lastModifiedDate
        self.lastModifiedBy = lastModifiedBy


class EventWithNames(Event):

    def __init__(self, key, userID, deviceID, agentTypeID, agentID, eventTypeID, eventStatus, eventParameters, result, percentComplete, priority, expirationEpoch, attemptNumber, maxAttempts, checkoutToken, tagString, tagNumber, creationDate, createdBy, lastModifiedDate, lastModifiedBy, deviceName, eventType, agentType, version, eventStatusName, agentIndex):
        super().__init__(key, userID, deviceID, agentTypeID, agentID, eventTypeID, eventStatus, eventParameters, result, percentComplete, priority, expirationEpoch, attemptNumber, maxAttempts, checkoutToken, tagString, tagNumber, creationDate, createdBy, lastModifiedDate, lastModifiedBy)
        self.deviceName = deviceName
        self.eventType = eventType
        self.agentType = agentType
        self.version = version
        self.eventStatusName = eventStatusName
        self.agentIndex = agentIndex


class VideoParameters:

    def __init__(self, height, width, fps, bitrate, vflip, hflip, encoding, segment_length_seconds):
        self.height = height
        self.width = width
        self.fps = fps
        self.bitrate = bitrate
        self.vflip = vflip
        self.hflip = hflip
        self.encoding = encoding
        self.segment_length_seconds = segment_length_seconds

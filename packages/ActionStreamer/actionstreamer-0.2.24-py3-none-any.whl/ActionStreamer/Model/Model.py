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

    class Transcode(Enum):  
        Transcode_file = 12

    class Transfer(Enum):  
        Transfer_file = 13


class Event:

    def __init__(self, key, userID, deviceID, agentTypeID, agentID, eventTypeID, eventStatus, eventParameters, processID, result, percentComplete, priority, expirationEpoch, attemptNumber, maxAttempts, checkoutToken, tagString, tagNumber, creationDate, createdBy, lastModifiedDate, lastModifiedBy):

        self.eventID = key
        self.userID = userID
        self.deviceID = deviceID
        self.agentTypeID = agentTypeID
        self.agentID = agentID
        self.eventTypeID = eventTypeID
        self.eventStatus = eventStatus
        self.eventParameters = eventParameters
        self.processID = processID
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

    def __init__(self, key, userID, deviceID, agentTypeID, agentID, eventTypeID, eventStatus, eventParameters, processID, result, percentComplete, priority, expirationEpoch, attemptNumber, maxAttempts, checkoutToken, tagString, tagNumber, creationDate, createdBy, lastModifiedDate, lastModifiedBy, deviceName, eventType, agentType, version, eventStatusName, agentIndex):
        super().__init__(key, userID, deviceID, agentTypeID, agentID, eventTypeID, eventStatus, eventParameters, result, processID, percentComplete, priority, expirationEpoch, attemptNumber, maxAttempts, checkoutToken, tagString, tagNumber, creationDate, createdBy, lastModifiedDate, lastModifiedBy)
        self.deviceName = deviceName
        self.eventType = eventType
        self.agentType = agentType
        self.version = version
        self.eventStatusName = eventStatusName
        self.agentIndex = agentIndex


class RecordingParameters:

    def __init__(self, height, width, fps, bitrate, vflip, hflip, encoding, segment_length_seconds):
        self.height = height
        self.width = width
        self.fps = fps
        self.bitrate = bitrate
        self.vflip = vflip
        self.hflip = hflip
        self.encoding = encoding
        self.segment_length_seconds = segment_length_seconds


class VideoClip:

    def __init__(self, file_id=0, ts_file_id=0, video_clip_parameters='', local_file_path='', height=0, width=0, frames_per_second=0, bitrate = 0, audio_status=0, start_time=0, start_time_ms=0, end_time=0, end_time_ms=0, clip_length_in_seconds=0):
        self.fileID = file_id
        self.tSFileID = ts_file_id
        self.videoClipParameters = video_clip_parameters
        self.localFilePath = local_file_path
        self.height = height
        self.width = width
        self.framesPerSecond = frames_per_second
        self.bitrate = bitrate
        self.audioStatus = audio_status
        self.startTime = start_time
        self.startTimeMs = start_time_ms
        self.endTime = end_time
        self.endTimeMs = end_time_ms
        self.clipLengthInSeconds = clip_length_in_seconds


class TranscodingParameters:

    def __init__(self, file_id, source, source_file, target_file, fps, codec):
        self.fileID = file_id
        self.source = source
        self.sourceFile = source_file
        self.targetFile = target_file
        self.fps = fps
        self.codec = codec


class TransferArgs:

    def __init__(self, video_clip_id, local_file_path, remote_filename, remote_folder_path):
        self.videoClipId = video_clip_id
        self.localFilePath = local_file_path
        self.remoteFilename = remote_filename
        self.remoteFolderPath = remote_folder_path

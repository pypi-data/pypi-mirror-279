from enum import Enum


class StudioStatus(str, Enum):
    OTHER = "OTHER"
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    COMING_SOON = "Coming Soon"
    TEMP_CLOSED = "Temporarily Closed"
    PERM_CLOSED = "Permanently Closed"

    @classmethod
    def all_statuses(cls) -> list[str]:
        return list(cls.__members__.values())


class EquipmentType(int, Enum):
    Treadmill = 2
    Strider = 3
    Rower = 4
    Bike = 5
    WeightFloor = 6
    PowerWalker = 7


class ChallengeType(int, Enum):
    Other = 0
    DriTri = 2
    MarathonMonth = 5
    HellWeek = 52
    Mayhem = 58
    TwelveDaysOfFitness = 63
    Transformation = 64
    RemixInSix = 65
    Push = 66
    BackAtIt = 84


class BookingStatus(str, Enum):
    CheckedIn = "Checked In"
    CancelCheckinPending = "Cancel Checkin Pending"
    CancelCheckinRequested = "Cancel Checkin Requested"
    Cancelled = "Cancelled"
    LateCancelled = "Late Cancelled"
    Booked = "Booked"
    Waitlisted = "Waitlisted"
    CheckinPending = "Checkin Pending"
    CheckinRequested = "Checkin Requested"
    CheckinCancelled = "Checkin Cancelled"

    @classmethod
    def all_statuses(cls) -> list[str]:
        return list(cls.__members__.values())


class HistoryBookingStatus(str, Enum):
    Attended = "Attended"
    Cancelled = "Cancelled"
    LateCancelled = "Late Cancelled"

    @classmethod
    def all_statuses(cls) -> list[str]:
        return list(cls.__members__.values())


class HistoryClassStatus(str, Enum):
    CheckedIn = "Checked In"
    CancelCheckinPending = "Cancel Checkin Pending"
    CancelCheckinRequested = "Cancel Checkin Requested"
    LateCancelled = "Late Cancelled"
    Booked = "Booked"
    Waitlisted = "Waitlisted"
    CheckinPending = "Checkin Pending"
    CheckinRequested = "Checkin Requested"
    CheckinCancelled = "Checkin Cancelled"
    Pending = "Pending"
    Confirmed = "Confirmed"
    Requested = "Requested"

    @classmethod
    def all_statuses(cls) -> list[str]:
        return list(cls.__members__.values())


ALL_CLASS_STATUS = BookingStatus.all_statuses()
ALL_HISTORY_CLASS_STATUS = HistoryClassStatus.all_statuses()
ALL_STUDIO_STATUS = StudioStatus.all_statuses()

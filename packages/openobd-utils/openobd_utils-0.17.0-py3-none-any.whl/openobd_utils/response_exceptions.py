

class ResponseException(Exception):
    """
    Base class for all exceptions that can be raised during vehicle communication.
    """

    def __init__(self, request="", response="", request_id=0, response_id=0):
        self.request = request
        self.response = response
        self.request_id = request_id
        self.response_id = response_id

    def get_request(self):
        return self.request

    def get_response(self):
        return self.response

    def get_request_id(self):
        return self.request_id

    def get_response_id(self):
        return self.response_id

    def set_request(self, request):
        self.request = request

    def set_response(self, response, overwrite=True):
        # If self.response already has a value, check if it needs to be overwritten
        if self.response and not overwrite:
            return
        self.response = response

    def set_request_id(self, request_id):
        self.request_id = request_id

    def set_response_id(self, response_id):
        self.response_id = response_id

    def __str__(self):
        exception_info = self.__class__.__name__

        if self.request_id:
            exception_info += f" ({self.request_id:03X}"
            if self.response_id:
                exception_info += f" -> {self.response_id:03X}"
            exception_info += ")"
        if self.request:
            exception_info += f" request: {self.request}"
        if self.response:
            exception_info += f" response: {self.response}"

        return exception_info


class NoResponseException(ResponseException):
    """
    Did not receive a response from the vehicle in the specified time.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InvalidResponseException(ResponseException):
    """
    The response received from the vehicle does not have the correct format.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NegativeResponseException(ResponseException):
    """
    Base class for all exceptions that are raised because of a negative response received from the vehicle.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GeneralRejectException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ServiceNotSupportedException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SubFunctionNotSupportedException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class IncorrectMessageLengthOrInvalidFormatException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ResponseTooLongException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BusyRepeatRequestException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ConditionsNotCorrectException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RequestSequenceErrorException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NoResponseFromSubnetComponentException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FailurePreventsExecutionOfRequestedActionException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RequestOutOfRangeException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SecurityAccessDeniedException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InvalidKeyException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ExceedNumberOfAttemptsException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RequiredTimeDelayNotExpiredException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UploadDownloadNotAcceptedException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TransferDataSuspendedException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GeneralProgrammingFailureException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class WrongBlockSequenceCounterException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RequestCorrectlyReceivedResponsePendingException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SubFunctionNotSupportedInActiveSessionException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ServiceNotSupportedInActiveSessionException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SpecificConditionNotCorrectException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RpmTooHighException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RpmTooLowException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EngineIsRunningException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EngineIsNotRunningException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EngineRunTimeTooLowException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TemperatureTooHighException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TemperatureTooLowException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class VehicleSpeedTooHighException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class VehicleSpeedTooLowException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ThrottlePedalTooHighException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ThrottlePedalTooLowException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TransmissionRangeNotInNeutralException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TransmissionRangeNotInGearException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BrakeSwitchesNotClosedException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ShifterLeverNotInParkException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TorqueConverterClutchLockedException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class VoltageTooHighException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class VoltageTooLowException(SpecificConditionNotCorrectException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UnknownNegativeResponseException(NegativeResponseException):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Based on ISO 14229-1
negative_response_code_exceptions = {
    "10": GeneralRejectException,
    "11": ServiceNotSupportedException,
    "12": SubFunctionNotSupportedException,
    "13": IncorrectMessageLengthOrInvalidFormatException,
    "14": ResponseTooLongException,
    "21": BusyRepeatRequestException,
    "22": ConditionsNotCorrectException,
    "24": RequestSequenceErrorException,
    "25": NoResponseFromSubnetComponentException,
    "26": FailurePreventsExecutionOfRequestedActionException,
    "31": RequestOutOfRangeException,
    "33": SecurityAccessDeniedException,
    "35": InvalidKeyException,
    "36": ExceedNumberOfAttemptsException,
    "37": RequiredTimeDelayNotExpiredException,
    "70": UploadDownloadNotAcceptedException,
    "71": TransferDataSuspendedException,
    "72": GeneralProgrammingFailureException,
    "73": WrongBlockSequenceCounterException,
    "78": RequestCorrectlyReceivedResponsePendingException,
    "7E": SubFunctionNotSupportedInActiveSessionException,
    "7F": ServiceNotSupportedInActiveSessionException,
    "81": RpmTooHighException,
    "82": RpmTooLowException,
    "83": EngineIsRunningException,
    "84": EngineIsNotRunningException,
    "85": EngineRunTimeTooLowException,
    "86": TemperatureTooHighException,
    "87": TemperatureTooLowException,
    "88": VehicleSpeedTooHighException,
    "89": VehicleSpeedTooLowException,
    "8A": ThrottlePedalTooHighException,
    "8B": ThrottlePedalTooLowException,
    "8C": TransmissionRangeNotInNeutralException,
    "8D": TransmissionRangeNotInGearException,
    "8F": BrakeSwitchesNotClosedException,
    "90": ShifterLeverNotInParkException,
    "91": TorqueConverterClutchLockedException,
    "92": VoltageTooHighException,
    "93": VoltageTooLowException,
}

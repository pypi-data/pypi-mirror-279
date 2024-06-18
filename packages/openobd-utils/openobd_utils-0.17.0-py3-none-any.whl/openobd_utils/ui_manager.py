from openobd import *
from .stream_manager import StreamManager, requires_active_stream


_control_types = Label | Options | Continue | YesNo | FreeText | Numbers
control_mapping = {
    Label: "control_label",
    Options: "control_options",
    Continue: "control_continue",
    YesNo: "control_yesno",
    FreeText: "control_freetext",
    Numbers: "control_number",
}


class UserInterfaceException(Exception):
    """
    Base class for all exceptions that can be raised while using the user interface.
    """
    pass


class UiManager(StreamManager):

    def __init__(self, session: OpenOBDSession, target: InterfaceType = InterfaceType.INTERFACE_USER):
        """
        Handles sending UI elements to a gRPC stream and parsing their responses.

        :param session: an authenticated OpenOBDSession with which to start the stream.
        :param target: determines who is able to view the user interface.
        """
        super().__init__(session.control)
        self.target = target

    @requires_active_stream
    def show_ui(self, control: _control_types) -> None | int | bool | str:
        """
        Displays a control object and waits for a response.

        :param control: the control object to be displayed.
        :return: the user's response, depending on which control object has been displayed.
        """
        assert type(control) in control_mapping, f"Received unsupported control type {type(control)}."

        kwargs = {
            "target": self.target,
            control_mapping[type(control)]: control
        }
        self.send(UserInterface(**kwargs), clear_received_messages=True)
        while True:
            response = self.receive()
            if response.HasField("user_interface_status"):
                self._check_status(response.user_interface_status)
            # Confirm that the received control type matches the control sent earlier. If not, ignore it
            control_incoming = self._get_control_from_message(response)
            if isinstance(control_incoming, type(control)):
                if hasattr(control_incoming, "answer"):
                    return control_incoming.answer
                else:
                    return None

    @staticmethod
    def _get_control_from_message(message: UserInterface) -> _control_types:
        """
        Retrieves the control object from a given UserInterface message.

        :param message: UserInterface message containing a control object.
        :return: the control object present in the given message.
        """
        for control_type in control_mapping.values():
            if message.HasField(control_type):
                return getattr(message, control_type)

    @staticmethod
    def _check_status(status: Status):
        """
        Raises a UserInterfaceException if the given status contains ERROR or FAILURE. Prints a warning if it contains
        WARNING.

        :param status: the Status message to check.
        """
        if status.status_code == StatusCode.WARNING:
            print(f"Warning: {status.status_description}")
            return
        if status.status_code in (StatusCode.ERROR, StatusCode.FAILURE):
            raise UserInterfaceException(status.status_description)

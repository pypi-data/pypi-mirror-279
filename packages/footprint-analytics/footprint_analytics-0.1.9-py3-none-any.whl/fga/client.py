"""FGA client module that provide client class with public interface and configuration attributes

Classes:
    FGA: the FGA client class
"""

from typing import Optional, Union, List

from fga import constants
from fga.config import Config
from fga.event import Revenue, BaseEvent, Identify, IdentifyEvent, GroupIdentifyEvent, EventOptions, User, Event, \
    Account
from fga.plugin import FGADestinationPlugin, ContextPlugin, Plugin, EnrichmentPlugin, UserEnrichmentPlugin
from fga.timeline import Timeline
from fga.exception import InvalidEventError
import atexit
import threading
import pydash


class FGA:
    """FGA client used to store configurations and track events

    Args:
        api_key (str): The api key of FGA project. Must be set properly before tracking events.
        configuration (FGA.config.Config, optional): The configuration of client instance. A new instance
            with default config value will be used by default.

    Attributes:
        configuration (FGA.config.Config): the configuration of client instance

    Methods:
        track(event): Process and send event
        identify(identify_obj, event_properties, event_options): Send an identify event to update user properties
        group_identify(group_type, group_name, identify_obj, event_options, event_properties, user_properties): Send
            a group identify event to update group properties
        revenue(revenue_obj, event_options): Send a revenue event with revenue info in event_properties
        flush(): Flush all event waiting to be sent in the buffer
        add(plugin): Add the plugin object to client instance.
        remove(plugin): Remove the plugin object from client instance
        shutdown(): Shutdown the client instance
    """

    def __init__(self, token: str, project_id: int, configuration: Optional[Config] = None):
        """The constructor for the FGA class

        Args:
            api_key (str): The api key of FGA project. Must be set properly before tracking events.
            configuration (FGA.config.Config, optional): The configuration of client instance. A new instance
                with default config value will be used by default.
        """
        self.configuration: Config = configuration or Config()
        self.configuration.api_key = token
        self.configuration.project_id = project_id
        self.__timeline = Timeline()
        self.__timeline.setup(self)
        self._register_on_exit()
        self.add(FGADestinationPlugin())
        # self.add(UserEnrichmentPlugin())
        self.add(EnrichmentPlugin())
        self.add(ContextPlugin())

    def track(self, event: BaseEvent):
        """Process and send the given event object.

        Args:
            event (fga.event.BaseEvent): The event that we want to track
        """
        for field in event.need_fields:
            if getattr(event, field) is None:
                raise InvalidEventError(f"The {field} is required.")
        for filed, field_type in event.field_types.items():
            if 'event_properties.' in filed:
                event_properties = getattr(event, 'event_properties')
                value = pydash.get(event_properties, filed.split('.')[1])
                if event_properties is not None and value is not None and not isinstance(value, field_type):
                    raise InvalidEventError(f"The {filed} should be {field_type}.")
            elif 'user_properties.' in filed:
                user_properties = getattr(event, 'user_properties')
                value = pydash.get(user_properties, filed.split('.')[1])
                if user_properties is not None and value is not None and not isinstance(value, field_type):
                    raise InvalidEventError(f"The {filed} should be {field_type}.")
            elif getattr(event, filed) is not None and not isinstance(getattr(event, filed), field_type):
                raise InvalidEventError(f"The {filed} should be {field_type}.")

        try:
            self.configuration.server_url = constants.SERVER_URL
        except KeyError:
            raise InvalidEventError("Invalid event type.")
        self.__timeline.process(event)

    def identify(self, identify_obj: Identify, event_options: EventOptions, event_properties: Optional[dict] = None):
        """Send an identify event to update user properties

        Args:
            identify_obj (FGA.event.Identify): Identify object contain operations of updating user properties
            event_options (FGA.event.EventOptions): Provide additional information to identify event.
            event_properties (dict, optional): A dictionary of event properties.
        """
        if not identify_obj.is_valid():
            self.configuration.logger.error("Empty identify properties")
        else:
            event = IdentifyEvent(event_properties=event_properties,
                                  user_properties=identify_obj.user_properties)
            event.load_event_options(event_options)
            self.track(event)

    def user_set(self, user: User):
        self.track(user)

    def account_set(self, account: Account):
        self.track(account)

    # def asset_set(self, asset: Asset):
    #     self.track(asset)
    #
    # def session_set(self, session: Session):
    #     if session.event_properties is None:
    #         self.configuration.logger.error("Empty event properties")
    #     else:
    #         self.track(session)

    def user_set_once(self, user_id: str, key: str, value):
        user_properties = {}
        user_properties[key] = value
        event = User(user_id=user_id, user_properties=user_properties, event_properties={'user_operation': constants.IDENTITY_OP_SET_ONCE, 'set_once_key': key })
        self.track(event)

    def group_identify(self, group_type: str, group_name: str, identify_obj: Identify,
                       event_options: Optional[EventOptions] = None,
                       event_properties: Optional[dict] = None,
                       user_properties: Optional[dict] = None):
        """Send a group identify event to update group properties

        Args:
            group_type (str): The group type e.g. "sport"
            group_name (str): The group name e.g. "soccer"
            identify_obj (FGA.event.Identify): Identify object contain operations of updating group properties
            event_options (FGA.event.EventOptions, optional): Provide additional information to
                group identify event like user_id.
            event_properties (dict, optional): A dictionary of event properties. Defaults to None.
            user_properties (dict, optional): A dictionary of user properties. Defaults to None.
        """
        if not identify_obj.is_valid():
            self.configuration.logger.error("Empty group identify properties")
        else:
            event = GroupIdentifyEvent(event_properties=event_properties,
                                       user_properties=user_properties,
                                       groups={group_type: group_name},
                                       group_properties=identify_obj.user_properties)
            event.load_event_options(event_options)
            self.track(event)

    def revenue(self, revenue_obj: Revenue, event_options: EventOptions):
        """Send a revenue event with revenue info in event_properties

        Args:
            revenue_obj (FGA.event.Revenue): A revenue object that contains information like price,
                quantity, receipt,  revenue_type
            event_options (FGA.event.EventOptions): Provide additional information to revenue event
                like user_id.
        """
        if not revenue_obj.is_valid():
            self.configuration.logger.error("Invalid price for revenue event")
        else:
            event = revenue_obj.to_revenue_event()
            event.load_event_options(event_options)
            self.track(event)

    def set_group(self, group_type: str, group_name: Union[str, List[str]], event_options: EventOptions):
        """Sending an identify event to put a user in group(s) by setting group type and group name as
            user property for a user.

        Args:
            group_type (str): The group type e.g. "sport"
            group_name (str): The group name e.g. "soccer"
            event_options (FGA.event.EventOptions): Provide additional information for event
                like user_id.
        """
        identify = Identify().set(group_type, group_name)
        event = IdentifyEvent(groups={group_type: group_name}, user_properties=identify.user_properties)
        event.load_event_options(event_options)
        self.track(event)

    def flush(self):
        """Flush all event waiting to be sent in the buffer

        Returns:
            A list of Future objects for all destination plugins
        """
        return self.__timeline.flush()

    def add(self, plugin: Plugin):
        """Add the plugin object to client instance. Events tracked by this client instance will be
            processed by instance's plugins.

        Args:
            plugin (FGA.plugin.Plugin): the plugin object to be added to the client instance

        Returns:
            FGA: the client instance itself
        """
        self.__timeline.add(plugin)
        plugin.setup(self)
        return self

    def remove(self, plugin: Plugin):
        """Remove the plugin object from client instance

        Args:
            plugin (FGA.plugin.Plugin): the plugin object to be removed from the client instance

        Returns:
            FGA: the client instance itself
        """
        self.__timeline.remove(plugin)
        return self

    def shutdown(self):
        """Shutdown the client instance, not accepting new events, flush all events in buffer"""
        self.configuration.opt_out = True
        self.__timeline.shutdown()

    def _register_on_exit(self):
        """Internal method to clean up the client instance on main thread exit"""
        if hasattr(threading, "_register_atexit"):
            try:
                threading._register_atexit(self.shutdown)
            except Exception as e:
                self.configuration.logger.warning("register for exit fail")
        else:
            atexit.register(self.shutdown)

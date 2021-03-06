import os
import json
from ..TaskHolder import TaskHolder

class DispatcherTypeNotFoundError(Exception):
    """Dispatcher type not found error."""

class DispatcherInvalidOptionError(Exception):
    """Dispatcher invalid option error."""

class Dispatcher(object):
    """
    Abstract dispatcher.

    A dispatcher is used to delegate the execution of a task holder.
    """

    __registered = {}

    def __init__(self, dispatcherType):
        """
        Create a dispatcher object.
        """
        self.__options = {}
        self.__dispatcherType = dispatcherType

        # environment that should be used during the _perform
        self.setOption(
            'env',
            dict(os.environ)
        )

        # in case the task does not have the "output.verbose" metadata
        # the value of this option is assigned as metadata in the tasks
        # held by the task holder.
        self.setOption(
            'enableVerboseOutput',
            True
        )

    def type(self):
        """
        Return the dispatcher type.
        """
        return self.__dispatcherType

    def option(self, name, task=None):
        """
        Return a value for an option.

        When a task is specified it will look for the value of the option
        in the metadata first otherwise returns the value held by the
        dispatcher. This allows tasks to customize the behaviour
        of the dispatcher dynamically without affecting the defaults of the
        dispatcher itself.
        """
        # return from metadata
        if task:
            metadataKey = "dispatch.{}.{}".format(
                self.type(),
                name
            )

            if task.hasMetadata(metadataKey):
                return task.metadata(metadataKey)

        # return from dispatcher itself
        if name not in self.__options:
            raise DispatcherInvalidOptionError(
                'Invalid option name: "{0}"'.format(
                    name
                )
            )

        return self.__options[name]

    def setOption(self, name, value):
        """
        Set an option to the dispatcher.
        """
        self.__options[name] = value

    def optionNames(self):
        """
        Return a list of the option names.
        """
        return list(self.__options.keys())

    def dispatch(self, taskHolder, crawlers=[]):
        """
        Run the dispatcher.

        Return a list of ids created by the dispatcher that can be used to track
        the dispatched task holder.
        """
        assert isinstance(taskHolder, TaskHolder), "Invalid task holder type!"

        clonedTaskHolder = taskHolder.clone()

        # setting the verbose ouput to the tasks in place
        self.__setVerboseOutput(clonedTaskHolder)

        clonedTaskHolder.addCrawlers(crawlers)

        # in case the task does not have any crawlers means there is nothing
        # to be executed, returning right away.
        if len(clonedTaskHolder.task().crawlers()) == 0:
            return []

        return self._perform(clonedTaskHolder)

    def toJson(self):
        """
        Serialize a dispatcher to json (it can be loaded later through createFromJson).
        """
        contents = {
            "type": self.type()
        }

        # current options
        options = {}
        for optionName in self.optionNames():
            options[optionName] = self.option(optionName)
        contents['options'] = options

        return json.dumps(
            contents,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

    def _perform(self, taskHolder):
        """
        Execute the dispatcher.

        For re-implementation: should return a list of ids that can be used to track
        the dispatched task holder.
        """
        raise NotImplemented

    @staticmethod
    def createFromJson(jsonContents):
        """
        Create a dispatcher based on the jsonContents (serialized via toJson).
        """
        contents = json.loads(jsonContents)
        dispatcherType = contents["type"]
        dispatcherOptions = contents.get("options", {})

        # creating dispatcher
        dispatcher = Dispatcher.create(dispatcherType)

        # setting options
        for optionName, optionValue in dispatcherOptions.items():
            dispatcher.setOption(optionName, optionValue)

        return dispatcher

    @staticmethod
    def register(name, dispatcherClass):
        """
        Register a dispatcher type.
        """
        assert issubclass(dispatcherClass, Dispatcher), \
            "Invalid dispatcher class!"

        Dispatcher.__registered[name] = dispatcherClass

    @staticmethod
    def registeredNames():
        """
        Return a list of registered dispatchers.
        """
        return list(Dispatcher.__registered.keys())

    @staticmethod
    def create(dispatcherType, *args, **kwargs):
        """
        Create a dispatcher object.
        """
        if dispatcherType not in Dispatcher.__registered:
            raise DispatcherTypeNotFoundError(
                'Dispatcher name is not registed: "{0}"'.format(
                    dispatcherType
                )
            )
        return Dispatcher.__registered[dispatcherType](dispatcherType, *args, **kwargs)

    def __setVerboseOutput(self, taskHolder):
        """
        Assign the value held by the option "enableVerboseOutput" to the task metadata "output.verbose".

        The metadata assignment is done in place. However, the input task holder is the cloned
        version from the original one.
        """
        task = taskHolder.task()

        # making sure the task does not have specified any information about
        # "output.verbose"
        if not task.hasMetadata('output.verbose'):
            task.setMetadata(
                'output.verbose',
                self.option('enableVerboseOutput')
            )

        # propagating to the sub tasks recursively
        for subtaskHolder in taskHolder.subTaskHolders():
            self.__setVerboseOutput(subtaskHolder)

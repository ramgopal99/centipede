import json
import os
import glob
from ..Task import Task
from ..Template import Template
from ..CrawlerMatcher import CrawlerMatcher
from ..TaskHolder import TaskHolder
from ..Resource import Resource
from .TaskHolderLoader import TaskHolderLoader

class UnexpectedContentError(Exception):
    """Unexpected content error."""

class InvalidFileError(Exception):
    """Invalid file Error."""

class InvalidDirectoryError(Exception):
    """Invalid directory Error."""

class JsonLoader(TaskHolderLoader):
    """
    Loads configuration from json files.
    """

    def addFromJsonFile(self, fileName):
        """
        Add json from a file.

        The json file need to follow the format expected
        by {@link addFromJson}.
        """
        # making sure it's a valid file
        if not (os.path.exists(fileName) and os.path.isfile(fileName)):
            raise InvalidFileError(
                'Invalid file "{0}"!'.format(fileName)
            )

        with open(fileName, 'r') as f:
            contents = '\n'.join(f.readlines())
            self.addFromJson(
                contents,
                os.path.dirname(fileName),
                os.path.basename(fileName),
            )

    def addFromJsonDirectory(self, directory):
        """
        Add json from inside of a directory with json files.

        The json file need to follow the format expected
        by {@link addFromJson}.
        """
        # making sure it's a valid directory
        if not (os.path.exists(directory) and os.path.isdir(directory)):
            raise InvalidDirectoryError(
                'Invalid directory "{0}"!'.format(directory)
            )

        # collecting the json files and loading them to the loader.
        for fileName in glob.glob(os.path.join(directory, '*.json')):
            self.addFromJsonFile(fileName)

    def addFromJson(self, jsonContents, configPath, configName=''):
        """
        Add taskHolders from json.

        Expected format:
        {
          "scripts": [
            "*/*.py"
          ],
          "vars": {
            "prefix": "/tmp/test",
            "__uiHintSourceColumns": [
                "shot",
                "type"
            ]
          },
          "tasks": [
            {
              "run": "convertImage",
              "target": "{prefix}/foo/sequences/{seq}/{shot}/online/publish/elements/{plateName}/(newver <parent>).(pad {frame} 4).exr",
              "filter": "",
              "status": "execute",
              "metadata": {
                "match.types": [
                    "dpxPlate"
                ],
                "match.vars": {
                    "imageType": [
                        "sequence"
                    ]
                },
                "dispatch.await": True
              },
              "tasks": [
                {
                  "run": "movGen",
                  "target": "{prefix}/foo/sequences/{seq}/{shot}/online/review/{name}.mov",
                  "metadata": {
                    "match.types": [
                        "exrPlate"
                    ],
                    "match.vars": {
                        "imageType": [
                            "sequence"
                        ]
                    }
                  }
                },
                {
                    "include": "../../myTaskHolderInfo.json"
                }
              ]
            }
          ]
        }
        """
        contents = json.loads(jsonContents)

        # root checking
        if not isinstance(contents, dict):
            raise UnexpectedContentError('Expecting object as root!')

        # loading scripts
        if 'scripts' in contents:

            # scripts checking
            if not isinstance(contents['scripts'], list):
                raise UnexpectedContentError('Expecting a list of scripts!')

            for script in contents['scripts']:
                scriptFiles = glob.glob(os.path.join(configPath, script))

                # loading resource
                for scriptFile in scriptFiles:
                    Resource.get().load(scriptFile)

        vars = self.__parseVars(contents)
        vars['configPath'] = configPath
        vars['configName'] = configName

        self.__loadTaskHolder(contents, vars, configPath)

    def __loadTaskHolder(self, contents, vars, configPath, parentTaskHolder=None):
        """
        Load a task holder contents.
        """
        # loading task holders
        if 'tasks' not in contents:
            return

        # task holders checking
        if not isinstance(contents['tasks'], list):
            raise UnexpectedContentError('Expecting a list of task holders!')

        for taskHolderInfo in contents['tasks']:

            # task holder info checking
            if not isinstance(taskHolderInfo, dict):
                raise UnexpectedContentError('Expecting an object to describe the task holder!')

            taskHolderInfo = self.__expandTaskHolderInfo(taskHolderInfo, configPath)

            task = self.__parseTask(taskHolderInfo)

            # getting the target template
            targetTemplate = Template(taskHolderInfo.get('target', ''))

            # getting the filter template
            filterTemplate = Template(taskHolderInfo.get('filter', ''))

            # creating a task holder
            taskHolder = TaskHolder(
                task,
                targetTemplate,
                filterTemplate
            )

            # setting status of the task holder
            if 'status' in taskHolderInfo:
                taskHolder.setStatus(taskHolderInfo['status'])

            # adding variables to the task holder
            for varName, varValue in list(vars.items()) + list(self.__parseVars(taskHolderInfo).items()):
                taskHolder.addVar(
                    varName,
                    varValue,
                    isContextVar=True
                )

            if parentTaskHolder:
                parentTaskHolder.addSubTaskHolder(
                    taskHolder
                )
            else:
                self.addTaskHolder(taskHolder)

            # loading sub task holders recursevely
            if 'tasks' in contents:
                self.__loadTaskHolder(taskHolderInfo, {}, configPath, taskHolder)

    @classmethod
    def __expandTaskHolderInfo(cls, taskHolderInfo, configPath):
        """
        Return the expanded content of a task holder that can be described using an external resource.
        """
        # special case where configurations can be defined externally, when that
        # is the case loading that instead
        if 'include' in taskHolderInfo:

            # detecting if the path is absolute or needs to be resolved
            if os.path.isabs(taskHolderInfo['include']):
                absolutePath = taskHolderInfo['include']
            else:
                absolutePath = os.path.normpath(
                    os.path.join(configPath, taskHolderInfo['include'])
                )

            # replacing the current taskHolderInfo for the one defined externally
            # inside the json file (that one is going to contain the resolved task holder
            # information)
            with open(absolutePath) as f:
                taskHolderInfo = json.load(f)

        return taskHolderInfo

    @classmethod
    def __parseTask(cls, taskHolderInfo):
        """
        Return a task object parsed under the taskHolderInfo.
        """
        task = Task.create(taskHolderInfo['run'])

        # setting task options
        if 'options' in taskHolderInfo:
            for taskOptionName, taskOptionValue in taskHolderInfo['options'].items():
                task.setOption(taskOptionName, taskOptionValue)

        # setting task metadata
        if 'metadata' in taskHolderInfo:
            for taskMetadataName, taskMetadataValue in taskHolderInfo['metadata'].items():
                task.setMetadata(taskMetadataName, taskMetadataValue)

        return task

    @classmethod
    def __parseVars(cls, contents):
        """
        Return the variables defined inside of the contents.
        """
        vars = {}
        if 'vars' in contents:
            # vars checking
            if not isinstance(contents['vars'], dict):
                raise UnexpectedContentError('Expecting a list of vars!')
            vars = dict(contents['vars'])

        return vars

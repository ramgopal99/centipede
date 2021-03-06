from centipede.Task import Task
from centipede.TaskWrapper import TaskWrapper

class UPythonTestTask(Task):
    """
    Dummy task for testing UPython subprocess.
    """

    def _perform(self):
        sourceCrawler = self.crawlers()[0]
        if self.option('runUPython'):
            dummyTask = Task.create('uPythonTestTask')
            dummyTask.setOption("runUPython", False)
            dummyTask.add(sourceCrawler)
            wrapper = TaskWrapper.create('upython')
            result = wrapper.run(dummyTask)
        else:
            import OpenImageIO
            sourceCrawler.setVar("testUPython", OpenImageIO.VERSION)
            result = [sourceCrawler.clone()]

        return result


Task.register(
    'uPythonTestTask',
    UPythonTestTask
)

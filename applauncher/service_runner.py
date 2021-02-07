from multiprocessing import Process
import asyncio
import os
import logging


class ProcessServiceRunner:
    """Like a process pool but with initializer and friendly exit process"""
    def __init__(self):
        self.logger = logging.getLogger("service")
        self.running_services = []

    def add_service(self, name, function, args=(), kwargs={}):
        self.running_services.append((name, Process(target=function, args=args, kwargs=kwargs)))

    def run(self):
        for name, process in self.running_services:
            self.logger.info("Starting service %s", name)
            process.start()

    def wait(self):
        self.logger.info("Waiting for services to end")
        for _, i in self.running_services:
            i.join()

    def kill(self):
        for name, process in self.running_services:
            self.logger.info("Killing service %s (%s)", name, process.pid)
            os.kill(process.pid, 9)
            process.join()

    async def _terminate_processes(self, processes, grace_time=10):
        await asyncio.gather(*[
            self._terminate_process(*i, grace_time) for i in processes
        ])

    async def _terminate_process(self, name, process, grace_time=10):
        self.logger.info(f"Terminating service {name} ({process.pid})")
        process.terminate()
        wait = True
        while wait:
            grace_time -= 1
            await asyncio.sleep(1)
            wait = process.is_alive() and grace_time > 0

        if process.is_alive():
            self.logger.info(f"Killing service {name} ({process.pid})")
            os.kill(process.pid, 9)
            process.join()

    def shutdown(self, grace_time=10):
        self.logger.info("Shutting down services (grace time of %s seconds)", grace_time)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._terminate_processes(self.running_services, grace_time))

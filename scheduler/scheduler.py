"""

    @author : Manouchehr Rasouli

"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from config_loader import ConfigLoader


# todo : schedule all of the repeated jobs over the scheduler

class Scheduler:
    __instance = None

    @staticmethod
    def get_scheduler():
        """
        :param config:
        :return:
        """
        if Scheduler.__instance is None:
            Scheduler()
        return Scheduler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Scheduler.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Scheduler.__instance = self
            config_loader = ConfigLoader()
            self.config = config_loader.get_config()

            executors = {
                'default': self.config['monitor_engine.scheduler']['thread_pool_executor'],
                'processpool': self.config['monitor_engine.scheduler']['process_pool_executor']
            }
            job_defaults = {
                'coalesce': False,
                'max_instances': 3
            }
            self.scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)

    def add_job(self, function, args=None, minutes=10):
        """
        :param function:
        :param args:
        :param minutes:
        :return:
        """
        raise Exception('add job not implemented on job scheduler')

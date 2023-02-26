from info_collector import Collector

class PyLookout:
    def __init__(self):
        self.info = Collector()
        self.critical = 85

    def _stressed(self, percent):
        '''
        Compare a metric with the critical value.
        '''
        return True if percent > self.critical else False
    
    def _notify(self, metric):
        '''
        Send a notification.
        (right now it's just a print statement).
        '''
        print(f'Danger! ---> {metric} > {self.critical}%')

    def checker(self):
        '''
        One by one check if CPU, RAM and Disk space 
        utilization is larger than the critical value.
        '''
        if self._stressed(self.info.cpu_percent):
            self._notify('CPU')
        
        if self._stressed(self.info.ram_percent):
            self._notify('RAM')

        for disk in self.info.disks_info.values():
            if self._stressed(disk['du_percent']):
                self._notify('DISK')

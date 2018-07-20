#ZPF 
#encoding=utf-8 
import win32serviceutil 
import win32service 
import win32event 
import os 
import logging 
import inspect 
def readJSON():
  import json
  this_file = inspect.getfile(inspect.currentframe()) 
  dirpath = os.path.abspath(os.path.dirname(this_file)) 
  file=open(os.path.join(dirpath, "config.json"))
  content=file.read()
  data=json.loads(content)
  return data


class PythonService(win32serviceutil.ServiceFramework): 
  
  _svc_name_ = "MonitorService"
  
  _svc_display_name_ = "Monitor Service "
  _svc_description_ = "This is  a Monitor "
  
  def __init__(self, args): 
    win32serviceutil.ServiceFramework.__init__(self, args) 
    self.hWaitStop = win32event.CreateEvent(None, 0, 0, None) 
    self.config = readJSON()
    self.logger = self._getLogger() 
    self.run = True
  
  def start_appliction(self):
    import os
    os.system(self.config['bat_path'])
 
  def hasAppliction(self):
    import psutil
    for proc in psutil.process_iter():
      try:
          pinfo = proc.as_dict(attrs=['name'])
      except psutil.NoSuchProcess:
          pass
      else:
          if pinfo['name'] ==self.config['task_name']:
            return True
    return False


  def _getLogger(self): 
    
    logger = logging.getLogger('[MonitorService]') 
      
    this_file = inspect.getfile(inspect.currentframe()) 
    dirpath = os.path.abspath(os.path.dirname(this_file)) 
    handler = logging.FileHandler(os.path.join(dirpath, "service.log")) 
      
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s') 
    handler.setFormatter(formatter) 
      
    logger.addHandler(handler) 
    logger.setLevel(logging.INFO) 
      
    return logger 

 
  
  def SvcDoRun(self): 
    import time 
    while self.run: 
     if self.hasAppliction():
        self.logger.info("service  runing....")
     else:
        self.logger.info("service  restart....")
        self.start_appliction()
     time.sleep(int(self.config['monitor_time'])) 
     
  def SvcStop(self): 
    self.logger.info("service is stop....") 
    self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING) 
    win32event.SetEvent(self.hWaitStop) 
    self.run = False

if __name__=='__main__': 
  win32serviceutil.HandleCommandLine(PythonService) 
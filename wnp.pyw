'''
Created on 2010-2-21

@author: dell
'''
import subprocess,sys,os,time,win32com.client
import wx,win32api,win32gui  
from threading import Thread

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")

def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        #return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
        return os.path.dirname(sys.executable)
    #return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
    return os.path.dirname(__file__)

dir = module_path()
print dir

class NginxThread(Thread):
    
    def __init__(self,notify_window):
        
        Thread.__init__(self)
        self.father = notify_window
        self._want_abort = 0
        self.quit = False
        self.start()
        

    def run(self):
        while True:
            if self.father.startnginx:
                self.father.startnginx = False
                print 'rung-nginx\n'
                self.initRun();
                print 'nginx-down'
            if self.quit:
                print 'nginxquit'
                break
                return 
                print 'abort'
            print 'running-nginx'
            time.sleep(1)
        return

    def initRun(self):
       
        self.process = subprocess.Popen(['%s/nginx/nginx.exe'%dir,'-c','%s/nginx/conf/nginx.conf'%dir],shell=False,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        stdoutdata, stderrdata = self.process.communicate()
        self.father.setStd(stdoutdata, stderrdata)        
    def doQuit(self):
        self.quit = True
        
    def abort(self):
        
        try:
            self.process.kill()
            stopnginx = subprocess.Popen(['tskill','nginx'],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            stopnginx.wait()  
            print 'abort nginx'          
        except:
            pass
class PHPThread(Thread):
    
    def __init__(self,notify_window):
        
        Thread.__init__(self)
        self.father = notify_window
        self._want_abort = 0
        self.type = type
        self.quit = False
        self.start()
        

    def run(self):
        while True:
            if self.father.startphp:
                self.father.startphp = False
                print 'rung-php\n'
                self.initRun();
                #self.process.wait()
                
                print 'php-down'
            if self.quit:
                print 'phpquit'
                break
                return 
                print 'abort'
            print 'running-php'
            time.sleep(1)
        return

    def initRun(self):
        self.process = subprocess.Popen(['%s/php/php-cgi.exe'%dir,'-b','127.0.0.1:9000','-c','%s/php/php.ini'%dir],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE) 
        stdoutdata, stderrdata = self.process.communicate()
        self.father.setStd(stdoutdata, stderrdata)        
    def doQuit(self):
        self.quit = True
        
    def abort(self):
        
        #try:
            self.process.kill()
            stopnginx = subprocess.Popen(['tskill','php-cgi'],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            stopnginx.wait()  
            print 'abort php'          
        #except:
        #    pass
class TaskBarIcon(wx.TaskBarIcon):
    ID_Quit = wx.NewId()
    ID_RESTARTALL = wx.NewId()
    ID_RESTARTPHP = wx.NewId()
    ID_RESTARTNGINX = wx.NewId()
    ID_RELOADNGINX = wx.NewId()
    ID_ABOUT = wx.NewId()
    
    def __init__(self):
        
        wx.TaskBarIcon.__init__(self)
        
        self.firstRP = True
        self.startnginx = False
        self.stopnginx = False
        self.startphp = False
        self.stopphp = False
        
        
        self.php_process = PHPThread(self)
        self.nginx_process = NginxThread(self)
        
        
        
        self.StartPHP()
        self.StartNginx()
        
        self.SetIcon(wx.Icon(name='nginx.ico', type=wx.BITMAP_TYPE_ICO), 'WNP-nginx-php')
        
        self.Bind(wx.EVT_MENU, self.OnQuit, id=self.ID_Quit)
        self.Bind(wx.EVT_MENU, self.OnRestartAll, id=self.ID_RESTARTALL)
        self.Bind(wx.EVT_MENU, self.OnRestartPHP, id=self.ID_RESTARTPHP)
        self.Bind(wx.EVT_MENU, self.OnRestartNginx, id=self.ID_RESTARTNGINX)
        self.Bind(wx.EVT_MENU, self.OnReloadNginx, id=self.ID_RELOADNGINX)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.ID_ABOUT)
        
    
    def StartPHP(self):
        #self.php_process = subprocess.Popen(['%s/php/php-cgi.exe'%dir,'-b','127.0.0.1:9000'],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE) 
        #self.php_process.wait()
       
        self.startphp = True
        #self.php_process.initRun()
    
    def StopPHP(self):
        self.php_process.abort()    
    
    
    def StartNginx(self):
        #self.nginx_process = subprocess.Popen(['%s/nginx/nginx.exe'%dir,'-c','%s/nginx/conf/nginx.conf'%dir],shell=False,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        #self.nginx_process.wait()
        
        self.startnginx = True
        
    def StopNginx(self):
        self.nginx_process.abort()
        
    def ReloadNginx(self):
        pass
   
   
        
    def setStd(self,outdata,errdata):
        
        print outdata,errdata
        if errdata != "":
            dlg = wx.MessageDialog(None, "Please check your config.\n\n %s" %errdata,
                              'Error',
                              wx.OK)
            retCode = dlg.ShowModal()
            dlg.Destroy()
        
        
    def OnQuit(self, event):
        
        self.StopNginx()
        self.StopPHP()
        self.nginx_process.doQuit()
        self.php_process.doQuit()
        self.RemoveIcon()
        self.Destroy()
        
    def OnReloadNginx(self,event):
        self.ReloadNginx()
        
    def OnRestartPHP(self,event):
        
        self.StopPHP()
        self.StartPHP()
        
        if self.firstRP:
            self.StopNginx()
            self.StartNginx()
            self.firstRP = False
    
    def OnRestartNginx(self,event):
        self.StopNginx()
        self.StartNginx()
                  
    def OnRestartAll(self,event):
        self.StopNginx()
        self.StopPHP()
        #time.sleep(2)
        self.StartPHP()
        self.StartNginx()
    def OnAbout(self,event):
        try:
            ie = win32com.client.Dispatch("InternetExplorer.Application" )
            ie.Navigate("http://app.52686.com/win-nginx-php/")
            ie.Visible = 1
            ie.Show()
        except:
            pass
    # override
    def CreatePopupMenu(self):
        menu = wx.Menu()
        
        menu.Append(self.ID_RESTARTPHP,'RestartPHP')
        menu.Append(self.ID_RESTARTNGINX,'RestartNginx')
        #menu.Append(self.ID_RELOADNGINX,'ReloadNginx')
        menu.Append(self.ID_RESTARTALL,'RestartAll')
        menu.Append(self.ID_ABOUT,'About')
        menu.Append(self.ID_Quit, 'Exit')
        return menu
    
if __name__ == '__main__':
    
    app = wx.PySimpleApp()
    
    try:
        client = TaskBarIcon()
    except:
        pass
        #ct = win32api.GetConsoleTitle()  
        #hd = win32gui.FindWindow(0,ct)  
        #win32gui.ShowWindow(hd,0)  
    
    #client.dataReceived(frame)
    #client = CometClient()
    #client.sendData()
    #client.inputDate()
    
    #client.dataReceived()
    app.MainLoop()

'''
Created on 2010-2-21

@author: dell
'''
import subprocess,sys,os,time,win32com.client
import wx,win32api,win32gui  


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
class TaskBarIcon(wx.TaskBarIcon):
    ID_Quit = wx.NewId()
    ID_RESTARTALL = wx.NewId()
    ID_RESTARTPHP = wx.NewId()
    ID_RESTARTNGINX = wx.NewId()
    ID_RELOADNGINX = wx.NewId()
    ID_ABOUT = wx.NewId()
    def __init__(self):
        
        wx.TaskBarIcon.__init__(self)
        self.php_process = None
        self.nginx_process = None
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
        self.php_process = subprocess.Popen(['%s/php/php-cgi.exe'%dir,'-b','127.0.0.1:9000'],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE) 
        #self.php_process.wait()
    def StartNginx(self):
        self.nginx_process = subprocess.Popen(['%s/nginx/nginx.exe'%dir,'-c','%s/nginx/conf/nginx.conf'%dir],shell=False,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        #self.nginx_process.wait()
    def ReloadNginx(self):
        self.nginx_process = subprocess.Popen(['%s/nginx/nginx.exe'%dir,'-s','reload'],shell=False,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    def StopPHP(self):
        try:
            self.php_process.kill()
            stopphp = subprocess.Popen(['tskill','php-cgi'],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            stopphp.wait()
        except:
            pass
        
    def StopNginx(self):
        try:
            self.nginx_process.kill()
            stopnginx = subprocess.Popen(['tskill','nginx'],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            stopnginx.wait()
        except:
            pass
    def OnQuit(self, event):
        
        self.StopNginx()
        self.StopPHP()
        self.RemoveIcon()
        self.Destroy()
        
    def OnReloadNginx(self,event):
        self.ReloadNginx()
        
    def OnRestartPHP(self,event):
        self.StopPHP()
        self.StartPHP()
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

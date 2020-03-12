import pysftp, ftplib
from ..utils.logger import AlphaLogger

class FtpFile():
    name = ""
    size = 0

    def __init__(self,name,parameters=None):
        self.name  = name
        if parameters is not None:
            self.size   = parameters.st_size

class AlphaFtp():
    cnx     = None
    valid   = False
    sftp    = False
    files   = []
    index   = 0

    def __init__(self,host,user,password=None,port=22,key=None,sftp=False,log=None):
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None

        self.host       = host
        self.port       = port
        self.user       = user
        self.key        = key
        self.password   = password
        self.sftp       = sftp

        self.log     = AlphaLogger('AlphaFtp','alpha_ftp') if log is None else log
    
    def connect(self):
        if self.sftp:
            if self.key is None:
                cnx = pysftp.Connection(self.host, port=self.port, username=self.user, password=self.password, cnopts=self.cnopts)
            else:
                cnx = pysftp.Connection(self.host, port=self.port, username=self.user, password=self.password, cnopts=self.cnopts, private_key=self.key)
        else:
            cnx = ftplib.FTP(host=self.host,user=self.user,passwd=self.password)
        self.cnx = cnx
        return cnx
    
    def disconnect(self):
        if self.cnx is not None:
            self.cnx.close()

    def test_cnx(self):
        try:
            self.connect()
            self.log.info("Connection test to %s is valid"%self.host)
            self.valid = True
            self.disconnect()
        except Exception as ex:
            self.log.info("Connection test to %s failed: %s"%(self.host,ex))
            self.valid = False
        return self.valid

    def list_dir(self,directory,contain=None):
        files = []

        # Switch to a remote directory
        self.cnx.cwd(directory) #'/home/gollnwnw'

        # Obtain structure of the remote directory '/var/www/vhosts'
        if self.sftp:
            for attr in self.cnx.listdir_attr():
                if contain is None or contain in attr.filename:
                    files.append(FtpFile(attr.filename,attr))
                    #print (attr.filename,attr.st_uid, attr.st_gid, attr.st_mode,attr.st_mtime,attr.st_size)
        else:
            for attr in self.cnx.nlst():
                if contain is None or contain in attr:
                    files.append(FtpFile(attr,None))

        if len(files) == 0:
            print('No files in directory')
        return files

    def upload(self,sourcepath,remotepath):
        self.cnx.put(sourcepath,remotepath)

    def download(self,remotepath,localpath):
        try:
            if self.sftp:
                self.cnx.get(remotepath, localpath, callback=None)
            else:
                self.cnx.retrbinary("RETR " + remotepath ,open(localpath, 'wb').write)
            self.log.info('File %s downloaded to %s'%(remotepath,localpath))
            return True
        except Exception as ex:
            self.log.error(str(ex))
            return False

    def uploads(self,files_list):
        for file_dict in files_list:
            self.cnx.put(file_dict['sourcepath'],file_dict['remotepath'])

    def makedirs(self,remote_directory):
        self.cnx.makedirs(remote_directory)

    def set_line(self,txt):
        if not ';' in txt: return
        try:
            name        = txt.split()[0]
            ftp_file    = FtpFile(name)
            self.files.append(ftp_file)
            self.index += 1
        except Exception as Ex:
            print(Ex)
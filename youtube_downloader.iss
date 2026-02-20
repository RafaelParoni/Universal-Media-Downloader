[Setup]
AppName=YouTube Downloader
AppVersion=1.0
DefaultDirName={autopf}\YouTube Downloader
DefaultGroupName=YouTube Downloader
OutputDir=d:\MyPrograms\YT_V_DOWNLOAD
OutputBaseFilename=YouTube_Downloader_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Files]
Source: "d:\MyPrograms\YT_V_DOWNLOAD\youtube_downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\YouTube Downloader"; Filename: "{app}\youtube_downloader.exe"
Name: "{autodesktop}\YouTube Downloader"; Filename: "{app}\youtube_downloader.exe"; Tasks: desktopicon

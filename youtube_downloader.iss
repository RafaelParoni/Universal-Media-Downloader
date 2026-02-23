[Setup]
AppName=Universal Media Downloader
AppVersion=1.0
DefaultDirName={autopf}\Universal Media Downloader
DefaultGroupName=Universal Media Downloader
OutputDir=d:\MyPrograms\UniversalMediaDownloader
OutputBaseFilename=Universal_Media_Downloader_Setup
SetupIconFile=favIcon.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Files]
Source: "d:\MyPrograms\UniversalMediaDownloader\dist\universal downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Universal Media Downloader"; Filename: "{app}\universal downloader.exe"
Name: "{autodesktop}\Universal Media Downloader"; Filename: "{app}\universal downloader.exe"; Tasks: desktopicon

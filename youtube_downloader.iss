[Setup]
AppName=Universal Media Downloader
AppVersion=1.4.5
DefaultDirName={autopf}\Universal Media Downloader
DefaultGroupName=Universal Media Downloader
OutputDir=d:\MyPrograms\UniversalMediaDownloader
OutputBaseFilename=Universal_Media_Downloader_Setup
SetupIconFile=favIcon.ico
Compression=lzma
SolidCompression=yes
AppPublisher=Universal Media Soft
AppPublisherURL=https://universal-media-app.vercel.app/
AppSupportURL=https://github.com/
AppUpdatesURL=https://github.com/
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Files]
Source: "d:\MyPrograms\UniversalMediaDownloader\dist\universal downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[INI]
Filename: "{app}\lang_setup.ini"; Section: "Setup"; Key: "Language"; String: "{language}"

[Icons]
Name: "{autoprograms}\Universal Media Downloader"; Filename: "{app}\universal downloader.exe"
Name: "{autodesktop}\Universal Media Downloader"; Filename: "{app}\universal downloader.exe"; Tasks: desktopicon

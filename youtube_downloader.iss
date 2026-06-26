[Setup]
AppName=Paroni Downloader
AppVersion=1.4.6
DefaultDirName={autopf}\Paroni Downloader
DefaultGroupName=Paroni Downloader
OutputDir=dist
OutputBaseFilename=Paroni_Downloader_Setup
SetupIconFile=favIcon.ico
Compression=lzma
SolidCompression=yes
AppPublisher=Paroni Downloader Soft
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
Source: "dist\Paroni Downloader\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[INI]
Filename: "{app}\lang_setup.ini"; Section: "Setup"; Key: "Language"; String: "{language}"

[Icons]
Name: "{autoprograms}\Paroni Downloader"; Filename: "{app}\Paroni Downloader.exe"
Name: "{autodesktop}\Paroni Downloader"; Filename: "{app}\Paroni Downloader.exe"; Tasks: desktopicon

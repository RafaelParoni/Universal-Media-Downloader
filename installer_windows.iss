; Script Inno Setup para Paroni Downloader (Web Server)
; Compilar com Inno Setup 6+ no Windows

[Setup]
AppId={{A7E949D5-8E1A-4F3D-94B6-37D97B899C12}}
AppName=Paroni Downloader
AppVersion=2.5 Web
AppPublisher=Rafael Paroni
AppPublisherURL=https://rafaelparoni.vercel.app/
AppSupportURL=https://github.com/RafaelParoni/Paroni-Downloader
AppUpdatesURL=https://github.com/RafaelParoni/Paroni-Downloader
DefaultDirName={autopf}\Paroni Downloader
DefaultGroupName=Paroni Downloader
DisableProgramGroupPage=yes
LicenseFile=README_pt.md
OutputDir=installer_output
OutputBaseFilename=ParoniDownloader-Setup-v2.5
SetupIconFile=web\favIcon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Iniciar automaticamente ao ligar o Windows"; GroupDescription: "Inicialização:"; Flags: unchecked

[Files]
Source: "dist\ParoniDownloaderServer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "web\*"; DestDir: "{app}\web"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "README_pt.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Paroni Downloader"; Filename: "{app}\ParoniDownloaderServer.exe"; Parameters: "--open"; IconFilename: "{app}\web\favIcon.ico"
Name: "{group}\{cm:UninstallProgram,Paroni Downloader}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Paroni Downloader"; Filename: "{app}\ParoniDownloaderServer.exe"; Parameters: "--open"; IconFilename: "{app}\web\favIcon.ico"; Tasks: desktopicon
Name: "{userstartup}\Paroni Downloader"; Filename: "{app}\ParoniDownloaderServer.exe"; Tasks: startupicon

[Run]
Filename: "{app}\ParoniDownloaderServer.exe"; Parameters: "--open"; Description: "{cm:LaunchProgram,Paroni Downloader}"; Flags: nowait postinstall skipifsilent

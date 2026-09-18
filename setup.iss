[Setup]
AppName=Soul Client
AppVersion=1.0.0
; AppId is crucial so Windows uniquely tracks your app and its uninstaller
AppId={{9F5C5B52-3A61-4B98-82E5-2A42D157EF5D}}
DefaultDirName={userappdata}\SoulClient
DefaultGroupName=SoulClient
OutputDir=dist
OutputBaseFilename=SoulClientV1.0.0_Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=assets\icons\logo.ico
WizardStyle=modern
PrivilegesRequired=lowest

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; Main Executable compiled by PyInstaller
Source: "dist\SoulClient.exe"; DestDir: "{app}"; DestName: "SoulClient.exe"; Flags: ignoreversion

; Embedded Java Runtime, Modpack, Assets, OneConfig folders & background video
Source: "dist\runtimes\*"; DestDir: "{app}\runtimes"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\modpack\*"; DestDir: "{app}\modpack"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\OneConfig\*"; DestDir: "{app}\OneConfig"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\background.mp4"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Creates a folder named "SoulClient" in the Start Menu containing both the app and its uninstaller
Name: "{autoprograms}\SoulClient\Soul Client"; Filename: "{app}\SoulClient.exe"; IconFilename: "{app}\assets\icons\logo.ico"
Name: "{autoprograms}\SoulClient\Uninstall Soul Client"; Filename: "{uninstallexe}"; IconFilename: "{app}\SoulClient.exe"; IconIndex: 0

; Desktop shortcut
Name: "{autodesktop}\Soul Client"; Filename: "{app}\SoulClient.exe"; Tasks: desktopicon; IconFilename: "{app}\assets\icons\logo.ico"

[Run]
Filename: "{app}\SoulClient.exe"; Description: "{cm:LaunchProgram,Soul Client}"; Flags: nowait postinstall skipifsilent
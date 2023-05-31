[Setup]
AppName=ValockInstalocker
AppVersion=1.0
DefaultDirName={pf64}\valockinstalocker
DisableDirPage=yes
PrivilegesRequired=admin
OutputBaseFilename=valockinstalocker
OutputDir=C:\Users\riode\OneDrive\Desktop\vsets\
SetupIconFile=C:\Users\riode\OneDrive\Desktop\dist - Copy\assets\valicon2.ico
UninstallDisplayIcon=C:\Users\riode\OneDrive\Desktop\dist - Copy\assets\valicon2.ico

[Files]
Source: "C:\Users\riode\OneDrive\Desktop\finaldist\config.json"; DestDir: "{userappdata}\valock"
Source: "C:\Users\riode\OneDrive\Desktop\finaldist\valockinstalocker.exe"; DestDir: "{app}"
Source: "C:\Users\riode\OneDrive\Desktop\finaldist\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "valockinstalocker"; ValueData: "{app}\valockinstalocker.exe"; Flags: uninsdeletevalue;
[UninstallRun]
Filename: "{cmd}"; Parameters: "/C ""taskkill /im valockinstalocker.exe /f /t"
[Tasks]
Name: StartAfterInstall; Description: Run application after install
[Icons]
Name: "{commondesktop}\valockinstalocker"; Filename: "{app}\valockinstalocker.exe"; WorkingDir: "{app}"
Name: "{commonstartup}\valockinstalocker"; Filename: "{app}\valockinstalocker.exe"
[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    Sleep(10000); // Delay for 5 seconds
end;
[Run]
Filename: {app}\valockinstalocker.exe; Flags: shellexec skipifsilent nowait; Tasks: StartAfterInstall

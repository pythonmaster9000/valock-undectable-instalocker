[Setup]
AppName=Valock
AppVersion=1.0
DefaultDirName={pf}\valock
DisableDirPage=yes
OutputBaseFilename=valock
OutputDir=C:\Users\riode\OneDrive\Desktop\vsets\
SetupIconFile=C:\Users\riode\OneDrive\Desktop\dist - Copy\assets\valicon2.ico
UninstallDisplayIcon=C:\Users\riode\OneDrive\Desktop\dist - Copy\assets\valicon2.ico

[Files]
Source: "C:\Users\riode\OneDrive\Desktop\finaldist\config.json"; DestDir: "{userappdata}\valock"
Source: "C:\Users\riode\OneDrive\Desktop\finaldist\valock.exe"; DestDir: "{app}"
Source: "C:\Users\riode\OneDrive\Desktop\finaldist\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "valock"; ValueData: "{app}\valock.exe"; Flags: uninsdeletevalue;
[UninstallRun]
Filename: "{cmd}"; Parameters: "/C ""taskkill /im valock.exe /f /t"
[Tasks]
Name: StartAfterInstall; Description: Run application after install
[Run]
Filename: {app}\valock.exe; Flags: shellexec skipifsilent nowait; Tasks: StartAfterInstall

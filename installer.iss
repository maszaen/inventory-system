#define MyAppName "PyStockFlow"
#define MyAppVersion "5.5.0"
#define MyAppPublisher "Maszaen"
#define MyAppURL "https://github.com/maszaen/inventory-system"
#define MyAppExeName "PyStockFlow.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
AppId={{adfb107b-8fa6-45a3-9c91-1d07cdd422ba}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=installer
OutputBaseFilename=PyStockFlow_Setup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
DisableWelcomePage=no
DisableDirPage=auto
DisableProgramGroupPage=auto

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function GetCustomEnvPath(Param: String): String;
var
  ManifestFile: String;
  FileLines: TArrayOfString;
  I: Integer;
  Line: String;
  StartPos: Integer;
  EndPos: Integer;
begin
  Result := '';
  
  ManifestFile := ExpandConstant('{autopf}\{#MyAppName}\manifest.json');
  if not FileExists(ManifestFile) then
    ManifestFile := ExpandConstant('{localappdata}\{#MyAppName}\manifest.json');
    
  if LoadStringsFromFile(ManifestFile, FileLines) then
    for I := 0 to GetArrayLength(FileLines) - 1 do
    begin
      Line := FileLines[I];
      if Pos('"env_path":', Line) > 0 then
      begin
        StartPos := Pos('": "', Line) + 4;
        EndPos := Pos('",', Line);
        if (StartPos > 0) and (EndPos > StartPos) then
          Result := Copy(Line, StartPos, EndPos - StartPos);
        Break;
      end;
    end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{autopf}\{#MyAppName}\env"
Type: filesandordirs; Name: "{autopf}\{#MyAppName}\temp"

Type: filesandordirs; Name: "{localappdata}\{#MyAppName}\env"
Type: filesandordirs; Name: "{localappdata}\{#MyAppName}\temp"

Type: files; Name: "{code:GetCustomEnvPath}"

Type: filesandordirs; Name: "{autopf}\{#MyAppName}\logs"

Type: filesandordirs; Name: "{localappdata}\{#MyAppName}\logs"

Type: filesandordirs; Name: "{app}\logs"

Type: dirifempty; Name: "{autopf}\{#MyAppName}"
Type: dirifempty; Name: "{localappdata}\{#MyAppName}"
Type: dirifempty; Name: "{app}"

Type: files; Name: "{autopf}\{#MyAppName}\manifest.json"
Type: files; Name: "{localappdata}\{#MyAppName}\manifest.json"
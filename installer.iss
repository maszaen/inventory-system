#define MyAppName "PyStockFlow"
#define MyAppVersion "5.0.0"
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
  ManifestContent: String;
  EnvPath: String;
begin
  // Try Program Files manifest first
  ManifestFile := ExpandConstant('{autopf}\{#MyAppName}\manifest.json');
  if not FileExists(ManifestFile) then
    // Try LocalAppData manifest
    ManifestFile := ExpandConstant('{localappdata}\{#MyAppName}\manifest.json');
    
  if FileExists(ManifestFile) then
  begin
    LoadStringFromFile(ManifestFile, ManifestContent);
    // Simple JSON parsing to get env_path
    if Pos('"env_path":', ManifestContent) > 0 then
    begin
      EnvPath := Copy(ManifestContent, Pos('"env_path":', ManifestContent) + 11,Pos('",', ManifestContent) - (Pos('"env_path":', ManifestContent) + 11));
      Result := EnvPath;
    end;
  end;
end;

[UninstallDelete]
; Program Files
Type: filesandordirs; Name: "{autopf}\{#MyAppName}\env"
Type: filesandordirs; Name: "{autopf}\{#MyAppName}\temp"

; LocalAppData
Type: filesandordirs; Name: "{localappdata}\{#MyAppName}\env"
Type: filesandordirs; Name: "{localappdata}\{#MyAppName}\temp"

; Custom
Type: files; Name: "{code:GetCustomEnvPath}"

; Logs in Program Files
Type: filesandordirs; Name: "{autopf}\{#MyAppName}\logs"

; Logs in LocalAppData
Type: filesandordirs; Name: "{localappdata}\{#MyAppName}\logs"

; Logs in application directory
Type: filesandordirs; Name: "{app}\logs"

; Clean directories
Type: dirifempty; Name: "{autopf}\{#MyAppName}"
Type: dirifempty; Name: "{localappdata}\{#MyAppName}"
Type: dirifempty; Name: "{app}"

; Clean manifest
Type: files; Name: "{autopf}\{#MyAppName}\manifest.json"
Type: files; Name: "{localappdata}\{#MyAppName}\manifest.json"
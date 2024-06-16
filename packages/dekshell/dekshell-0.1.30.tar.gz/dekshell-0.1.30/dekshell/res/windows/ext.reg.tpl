Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Applications\{dekshell_exe}]

[HKEY_CLASSES_ROOT\Applications\{dekshell_exe}\shell]

[HKEY_CLASSES_ROOT\Applications\{dekshell_exe}\shell\open]

[HKEY_CLASSES_ROOT\Applications\{dekshell_exe}\shell\open\command]
@="\"{path_pythonw}\" -c \"from dektools.shell import shell_command_nt_as_admin;shell_command_nt_as_admin(r'{dekshell_exe} rf %1')\""

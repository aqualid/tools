# Example of user setup script for user's environment
#
# Such scripts could be placed in any of default locations:
# On Windows:
#   X:\PythonXX\Lib\site-packages\aqualid\tools
#   %USERPROFILE%\AppData\Roaming\Python\PythonXX\site-packages\aqualid\tools
#   %USERPROFILE%\.config\aqualid\tools
#
# On Unix:
#   /usr/lib/pythonX.Y/site-packages/aqualid/tools
#   $PYTHONUSERBASE/lib/pythonX.Y/site-packages
#   $HOME/.config/aqualid/tools
#
#
from aql import tool_setup, get_shell_script_env

script = r"C:\Program Files (x86)\Microsoft Visual Studio 12\VC\vcvarsall.bat"


@tool_setup('msvcpp', 'msvc++', 'msvc')
def msvc_env(cls, options):
    """
    Sets up system environment variables.
    :param cls: Tools class. It can be used to call static/class helpers methods
    :param options: Tools options which allow to configure environment.
    :return dictionary system envrironment.
    """

    if not options.target_arch.is_set():
        target = 'x86'
    else:
        target_map = {
                'x86-32': "x86",
                'x86-64': "amd64",
                'arm':    "arm",
        }

        target = options.target_arch.map_value(target_map)

    return get_shell_script_env(script, target)

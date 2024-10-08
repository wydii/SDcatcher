import plistlib
import os
from platforms import getPlatform

argument = "dialog"
launch_agents_dir = os.path.join(os.environ.get("HOME"), "Library", "LaunchAgents")
pl_path = os.path.join(launch_agents_dir, "com.sdcatcher.insert.plist")


def installed(pythonBin) :
    if getPlatform() == "Darwin" :
        installedBin = 0
        if os.path.exists(pl_path) :
            with open(pl_path,'rb') as pl :
                installedBin = plistlib.load(pl)['ProgramArguments'][0] == pythonBin
        return os.path.exists(pl_path) and installedBin

def install(pythonBin):
    if getPlatform() == "Darwin":
        
        
        # Create the LaunchAgents folder if it doesn't exist
        os.makedirs(launch_agents_dir, exist_ok=True)
        
        
        pl = {
            'Label': 'com.sdcatcher.sdcards',
            'ProgramArguments': [pythonBin, argument],
            'WatchPaths': ['/Volumes']
        }
        try:
            with open(pl_path, 'wb') as f:
                plistlib.dump(pl, f)
            print(pl_path, "created")
            return True

        except Exception as e:
            print('Could not install Launcher:', e)

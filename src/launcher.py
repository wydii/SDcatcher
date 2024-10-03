import plistlib
import os, platform

argument = "dialog"

def install(pythonBin):
    if platform.system() == "Darwin":
        launch_agents_dir = os.path.join(os.environ.get("HOME"), "Library", "LaunchAgents")
        
        # Create the LaunchAgents folder if it doesn't exist
        os.makedirs(launch_agents_dir, exist_ok=True)
        
        pl_path = os.path.join(launch_agents_dir, "com.sdcatcher.insert.plist")
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

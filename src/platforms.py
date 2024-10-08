import os,platform,subprocess
import autorun





####################################               Cross-platform functions                 #################################


def getPlatform() :
    return platform.system()

def volumeNotFound() :
    if getPlatform() == "Darwin" :
        show_notification("Volume not found", "No registerd SD card has been found.")




def dialog(mappings) :
     if getPlatform() == "Darwin" :
        return macDialog(mappings)
     

def execute(photo,video,mappings) :
    if photo and video :
        autorun.loader(mappings)
    elif photo :
        newMappings = []
        for mapping in mappings :
            if mapping["type"] == "photo" :
                newMappings.append(mapping)
        if len(newMappings) :
            autorun.loader(newMappings)
    elif video : 
        newMappings = []
        for mapping in mappings :
            if mapping["type"] == "video" :
                newMappings.append(mapping)
        if len(newMappings) :
            autorun.loader(newMappings)

def copy_with_progress(src, dst):
    # Get the size of the source file
    total_size = os.path.getsize(src)
    # Open the source file in binary mode
    with open(src, 'rb') as fsrc:
        # Open the destination file in binary mode
        with open(dst, 'wb') as fdst:
            # Copy the file chunk by chunk
            while True:
                # Read a chunk of data from the source file
                chunk = fsrc.read(1024)
                # If no more data is available, break the loop
                if not chunk:
                    break
                # Write the chunk to the destination file
                fdst.write(chunk)



#################################### MacOS function for displaying alerts and notifications #################################


def dialogLoopMac():
    firstContact = macAlert("SD Card detected","Both photo and clips mappings are available","Sync Both","Select Specific","No Thanks","3:1")
    if firstContact == "button returned:Select Specific":
        secondContact = macAlert("Select Specific Sync","Choose what type of media you wish to sync","Sync Photos","Sync Videos","Go Back","3:2")
        if len(secondContact) == 0:
            return dialogLoopMac()
        else:
            return secondContact
    elif len(firstContact) == 0:
        return False
    else:
        return firstContact


def macAlert(title, text, button1, button2, cancelButton, alertPreset):

    if alertPreset == "3:1" :
        command = """
                osascript -e 'display alert "{}" message "{}" buttons {{"{}", "{}", "{}"}} default button "{}" cancel button "{}"'
                """.format(title, text,button1,button2,cancelButton,button1,cancelButton)

    elif alertPreset == "3:2" :
        command = """
                osascript -e 'display alert "{}" message "{}" buttons {{"{}", "{}", "{}"}} cancel button "{}"'
                """.format(title, text,button1,button2,cancelButton,cancelButton)
    
    elif alertPreset == "2:1" :
        command = """
                osascript -e 'display alert "{}" message "{}" buttons {{"{}", "{}"}} default button "{}" cancel button "{}"'
                """.format(title, text,button1,cancelButton,button1,cancelButton)
        
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def macDialog(mappings) :
    photo = False
    video = False
    for mapping in mappings :
        if mapping["type"] == "photo" :
            photo = True
        elif mapping["type"] == "video" :
            video = True
    
    if photo and video :
        return dialogLoopMac()
    elif photo :
        return macAlert("SD Card detected","Photo mappings have been found","Sync Photos",None,"No Thanks","2:1")
    elif video :
        return macAlert("SD Card detected","Video mappings have been found","Sync Videos",None,"No Thanks","2:1")
    else :
        return False
    

def show_notification(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
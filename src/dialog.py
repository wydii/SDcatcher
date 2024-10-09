import platforms,settings

def dialog() :
    
    mappings = settings.checkVolume()

    try :    
        ### SD card not plugged
        if not mappings :
            print("Volume not attached")
        
        ### SD card plugged 
        else :                                       
            if settings.load()["showDialog"] :
                userInterraction = platforms.dialog(mappings) 
                
                if not userInterraction :
                    print ("User declined")
                    
                
                if userInterraction == "button returned:Sync Photos" :
                    platforms.execute(True,False,mappings)

                elif userInterraction == "button returned:Sync Videos" :
                    platforms.execute(False,True,mappings)

                elif userInterraction == "button returned:Sync Both" :
                    platforms.execute(True,True,mappings)

            else :
                platforms.execute(True,True,mappings)
    

    except Exception as e :
        print ('Something went wrong during dialog execution :',e)


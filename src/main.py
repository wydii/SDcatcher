import flet as ft
from flet import *
import launcher,dialog,settings,platforms
import os,sys,time

# Get the path of the currently running Python interpreter
python_binary = sys.executable

# Get the absolute path of the Python binary
python_binary_location = os.path.abspath(python_binary)

if len(sys.argv) >1 and sys.argv[1] == "dialog" :
    dialog.dialog()

else :
    def main(page: ft.Page):
        
        page.window.width = 500
        page.window.alignment= ft.alignment.center
        MAIN_COLOR = ft.colors.INDIGO_300
        SECOND_COLOR = ft.colors.INDIGO_300
        
        versionData = settings.load()["version"]
        showDialog = settings.load()["showDialog"]
        autoEject = settings.load()["autoEject"]
        playSound = settings.load()["playSound"]
        launcherButton = ft.TextButton()


        def settingsUpdate() :
            global versionData,showDialog,autoEject,playSound
            versionData = settings.load()["version"]
            showDialog = settings.load()["showDialog"]
            autoEject = settings.load()["autoEject"]
            playSound = settings.load()["playSound"]
        
        def launcherUpdate() :
            if launcher.installed(python_binary_location) :
                launcherButton.text = "Launcher installed"
                launcherButton.icon = ft.icons.CHECK_BOX_SHARP
                launcherButton.disabled = True
            else :
                launcherButton.text = "Install Launcher"
                launcherButton.icon = icons.CHECK_BOX_OUTLINE_BLANK_SHARP
                launcherButton.on_click = lambda e: launcherInstall()

        def launcherInstall() :
            launcher.install(python_binary_location)
            launcherUpdate()
            refreshUI()


        def updateInterface() :
            t.tabs[0].content=ft.Column(dataLoader(),scroll=ft.ScrollMode.ADAPTIVE)
            launcherUpdate()
            settingsUpdate()
            page.update()

        def refreshUI(message=None,undo=None) :
            if settingsManager.open:
                page.close(settingsManager)
            updateInterface()
            if message :
                showNotification(message,undo)

        def showNotification(notificationMessage,undo=None) :
            def undoManager(e,undo) :
                undo(e)
                snackbar.duration=1
                snackbar.show_close_icon=False
                snackbar.disabled=True
                snackbar.content=ft.Text("Undoing . . .",color=colors.BLACK)
                snackbar.open=True
                updateInterface()
            undoButton = ft.TextButton("Undo",icon=ft.icons.UNDO_OUTLINED,style=ButtonStyle(color=MAIN_COLOR),on_click=lambda e:undoManager(e,undo))
            snackbar = ft.SnackBar(
                content=ft.Row([ft.Text(notificationMessage,color=ft.colors.BLACK)],wrap=True),
                bgcolor=ft.colors.INDIGO_50,
                show_close_icon=True,
                close_icon_color=ft.colors.INDIGO_300,
                behavior=ft.SnackBarBehavior.FLOATING,
                )
            if undo!=None :
                snackbar.content.controls.append(undoButton)
            
                
            page.overlay.append(snackbar)
            snackbar.open=True
            page.update()

        ##################################### MAPPING CONTROLS ##################################
       
        
        def fooCreate() :
            settings.createNewMapping("ZV1","/Volumes/ZV1/PRIVATE/M4ROOT/CLIP/","/Users/yehdar/Pictures/ZV1/CLIPS/","video",".mp4")
            settings.createNewMapping("ZV1","/Volumes/ZV1/DCIM/100MSDCF/","/Users/yehdar/Pictures/ZV1/PICS/","photo",".jpg")
            refreshUI("Mappings Created")
        
        def removeMapping(uuid) :
            mapping = settings.getMapping(uuid)
            undo = lambda e: settings.createNewMapping(mapping["name"], mapping["sourcePath"], mapping["destinationPath"], mapping["type"], mapping["format"])
            settings.removeMapping(uuid)
            refreshUI("Removed mapping for "+mapping["name"]+" of type "+mapping["type"],undo)
        ##################################### SETTINGS LOADER ###################################
        

        def dataLoader() :
            mapTabs = []
            data = settings.load()     
            for mapping in data["mappings"] :
                
                uuid = mapping["uuid"]
                name = mapping["name"]
                source = mapping["sourcePath"]
                destination = mapping["destinationPath"]
                type = mapping["type"]
                format = mapping["format"]
                
                icon = ft.icons.PHOTO_CAMERA if type=="photo" else ft.icons.MOVIE
                description = "Picture Mapping" if type =="photo" else "Video Mapping"

                
               
                
                styleDict = [("Source :",source),("Destination :",destination),("Format :",format)]
                ListTiles = []
                for tup in styleDict :
                    ListTiles.append(ft.ListTile(
                                        title=ft.Row([ft.OutlinedButton(text=tup[0],style=ft.ButtonStyle(padding=5,shape=ft.RoundedRectangleBorder(radius=5),side=ft.BorderSide(color=SECOND_COLOR,width=2),color=SECOND_COLOR)),
                                                    ft.Text(tup[1],size=10,weight=ft.FontWeight.W_100)])
                                    ))
                mapTabs.append(ft.ExpansionTile(
                        title=ft.ListTile(leading=ft.Icon(icon),
                                        title=ft.Text(name),
                                        trailing=ft.PopupMenuButton(
                                        icon=ft.icons.MORE_VERT,
                                            items=[
                                                ft.PopupMenuItem(text="Modify",icon=ft.icons.EDIT),
                                                ft.PopupMenuItem(text="Remove",icon=ft.icons.REMOVE,on_click=lambda e, uuid=uuid: removeMapping(uuid)),
                                            ],
                                        )),
                        subtitle=ft.Text(description),
                        affinity=ft.TileAffinity.LEADING,
                        icon_color=MAIN_COLOR,
                        text_color=MAIN_COLOR,
                        controls=ListTiles,
                    ))
            if not mapTabs :
                mapTabs.append( ft.Column(spacing=10,controls=[ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                        ft.ListTile(
                                            leading=ft.Icon(ft.icons.HELP_OUTLINE,color=ft.colors.BLACK),
                                            title=ft.Text("Create your first Mapping !",color=ft.colors.BLACK),
                                            subtitle=ft.Container(content=ft.Text(
                                                "Click on the button down there to create your first SD card automation.",color=ft.colors.BLACK ),padding=ft.padding.symmetric(vertical=10))
                                        )]),   
                                padding=20,
                                ),
                            elevation=1,
                            color=ft.colors.INDIGO_100,
                            margin=ft.margin.only(top=60),
                            clip_behavior=ft.ClipBehavior.HARD_EDGE),
                        ft.Row(
                            [ft.Container(ft.Icon(name=icons.ARROW_RIGHT_ALT,size=65,color=ft.colors.INDIGO_100),rotate=3.14/2)],
                            alignment=ft.MainAxisAlignment.END
                            )]))
            return mapTabs

        ##################################### MODALS #############################################
        ####### SETTINGS 
       

        def exportConfiguration(e: FilePickerResultEvent):
            if e.path :
                result = settings.exportSettings(e.path)
                refreshUI(result)
        
        def importConfiguration(e : FilePickerResultEvent) :
            if e.files :
                result = settings.importSettings(e.files[0].path)
                refreshUI(result)

        get_export_dir = FilePicker(on_result=exportConfiguration)
        get_import_file = FilePicker(on_result=importConfiguration)
        page.overlay.extend([get_export_dir,get_import_file])

        settingsTile = ft.Column([
            ft.ListTile(
                leading= ft.Icon(icons.DOWNLOAD_OUTLINED),
                title= ft.Text("Export Configuration"),
                subtitle=ft.Text("Export mappings configuration to folder."),
                trailing=ft.TextButton("Select",icon=ft.icons.FOLDER,on_click=lambda e: get_export_dir.get_directory_path("Select a folder where settings.json will be saved"))
            ),
            ft.ListTile(
                leading= ft.Icon(icons.FILE_UPLOAD_OUTLINED),
                title= ft.Text("Import Configuration"),
                subtitle=ft.Text("Import mappings configuration from JSON file."),
                trailing=ft.TextButton("Select",icon=ft.icons.FILE_UPLOAD_OUTLINED,on_click=lambda e: get_import_file.pick_files("Import a JSON Configuration file",file_type=FilePickerFileType.CUSTOM,allowed_extensions=["json"]))
            ),
            ft.ListTile(
                leading= ft.Icon(icons.SPEAKER_NOTES_OUTLINED),
                title= ft.Text("Show Dialog"),
                subtitle=ft.Text("Show pop up when inserting SD card?"),
                trailing=ft.Checkbox(value=showDialog,on_change=lambda e: settings.toggleCheckbox("showDialog"))
            ),
            ft.ListTile(
                leading= ft.Icon(icons.EJECT_OUTLINED),
                title= ft.Text("Auto Eject"),
                subtitle=ft.Text("Automatically eject SD card after completion?"),
                trailing=ft.Checkbox(value=autoEject,on_change=lambda e: settings.toggleCheckbox("autoEject"))
            ),
            ft.ListTile(
                leading= ft.Icon(icons.HEADSET_OUTLINED),
                title= ft.Text("Play Sound"),
                subtitle=ft.Text("Play sound after completion?"),
                trailing=ft.Checkbox(value=playSound,on_change=lambda e: settings.toggleCheckbox("playSound"))
            ),
            ft.ListTile(
                leading= ft.Icon(icons.REFRESH_OUTLINED),
                title= ft.Text("Refresh UI"),
                subtitle=ft.Text("Get the freshest data out there"),
                trailing=ft.TextButton("Refresh",on_click=lambda e: refreshUI("UI refreshed."))
            )
        ])
        settingsManager = ft.AlertDialog(
                content=settingsTile,
                title=ft.Text("Settings"),
                actions=[ft.TextButton("Close", on_click=lambda e: page.close(settingsManager))],
                actions_alignment=ft.MainAxisAlignment.START,
                scrollable=True,
                surface_tint_color=MAIN_COLOR,
            )

        ####### UPDATE MANAGER
        updateTile = ft.ListTile(
                            leading= ft.Icon(ft.icons.UPDATE_OUTLINED),
                            title=ft.Text("Update manager"),
                            subtitle=ft.Text("Current version : ",[ft.TextSpan(versionData,style=TextStyle(weight=FontWeight.BOLD))]))
        updateActions = [
                    ft.TextButton("Close", on_click=lambda e: page.close(updateManager)),
                    ft.OutlinedButton("Check for update", on_click=lambda e: getUpdate(page))
                ]
        def getUpdate(page : ft.Page) :
            updateTile.leading = ft.ProgressRing(width=21, height=21)
            updateActions[1].text= "Fetching ..."
            updateActions[1].disabled = True
            page.update()
            time.sleep(5)
            updateTile.leading = ft.Icon(ft.icons.UPDATE_OUTLINED) 
            updateActions[1].text= "Check for update"
            updateActions[1].disabled = False
            page.update()
        updateManager = ft.AlertDialog(
                content=updateTile,
                actions=updateActions,
                actions_alignment=ft.MainAxisAlignment.END,
                surface_tint_color=MAIN_COLOR,
            )
        ####### ADD MAPPING MODAL
        def addIndicator(step) :
                    stackIndicator = ft.Row([],alignment=MainAxisAlignment.CENTER)
                    for i in range(3) :
                        if step-1 == i :
                            stackIndicator.controls.append(ft.Container(content=ft.CircleAvatar(bgcolor=colors.INDIGO_400, radius=5)))
                        else :
                            stackIndicator.controls.append(ft.Container(content=ft.CircleAvatar(bgcolor=colors.BLUE_GREY_200, radius=5)))
                    return stackIndicator
        
        
        
        
        pickedVolume = []
        pickedType = []
        def pickVolume(volumeFullPath) :
            pickedVolume.append(volumeFullPath)
            mappingController(2)

        def selectPathsAndType(fullPath,type) :
            pickedVolume.append(fullPath)
            pickedType.append(type)
            mappingController(3)

        mappingManager = ft.AlertDialog(
                title=ft.Text("Add a Mapping"),
                actions=[],
                actions_alignment=ft.MainAxisAlignment.START,
                content = ft.Column,
                surface_tint_color=MAIN_COLOR,
                scrollable=True,
                content_padding=ft.padding.only(30,30,30,90)
            )
        
        def mappingController(step) :
            initialContent = ft.Column([addIndicator(1),
                                    ft.ListTile(title=ft.Text("Insert at least one SD Card and refresh."),
                                    leading=ft.Icon(icons.SIM_CARD_DOWNLOAD_OUTLINED,color=MAIN_COLOR))],
                                    width=400,height=100,alignment=MainAxisAlignment.SPACE_BETWEEN)
            initialActions = [ft.TextButton("Close", on_click=lambda e: page.close(mappingManager)),
                          ft.TextButton("Refresh",icon=icons.REFRESH_OUTLINED,on_click= lambda e:mappingController(1))]
            
            def getPotentialMappings() :
                candidates = platforms.getPluggedVolumes()
                if len(candidates)>0 :

                    mappingManager.content.controls[1].title.value = "Choose one of the listed disk :"
                    mappingManager.content.controls[1].leading.name = icons.ARROW_CIRCLE_DOWN_ROUNDED
                    
                    sdGrid = ft.Row(wrap=True,spacing=30)
                    for volume in candidates :
                        sdGrid.controls.append(
                                            
                                                ft.Column(
                                                    [IconButton(icons.SD_CARD_OUTLINED,
                                                                icon_size=65,icon_color=MAIN_COLOR,
                                                                on_click=lambda e,volumeFullPath=volume: pickVolume(volumeFullPath),
                                                                visual_density=VisualDensity.COMFORTABLE),
                                                    Row([Text(volume.split("/")[-1],weight="bold",color=MAIN_COLOR)],wrap=True)]
                                                    ))
                    mappingManager.content.controls.append(sdGrid)


            if step == 1 :
                mappingManager.content = initialContent
                mappingManager.actions = initialActions
                getPotentialMappings()
            if step == 2 :
                
                fullPath = pickedVolume.pop()
                mappingManager.content.controls[0] = addIndicator(2)
                mappingManager.content.controls[1].title = Text("Select type for : ",spans=[ft.TextSpan(fullPath.split("/")[-1],style=TextStyle(weight="bold"))])
                mappingManager.content.controls[1].leading.name = icons.TYPE_SPECIMEN
                mappingManager.content.controls[2] = ft.Row([ft.SegmentedButton(
                    segments=[Segment("photo",label=Text("Photo"),icon=ft.Icon(icons.PHOTO)),Segment("video",label=Text("Video"),icon=ft.Icon(icons.VIDEO_CAMERA_FRONT_OUTLINED)),Segment("other",label=Text("Other"))],
                    allow_empty_selection=False,
                    selected={"photo"},
                    show_selected_icon=False,
                    on_change= lambda e : selectPathsAndType(fullPath,e.data)
                )],alignment=MainAxisAlignment.CENTER)
                mappingManager.actions = [ft.TextButton("Back",icon=icons.ARROW_BACK,on_click= lambda e:mappingController(1))]
            if step == 3 :
                fullPath = pickedVolume.pop()
                type = pickedType.pop()
                mappingManager.content.controls[0] = addIndicator(3)
                mappingManager.content.controls[1].title = Text("Select format for : ",spans=[ft.TextSpan(fullPath.split("/")[-1],style=TextStyle(weight="bold"))])
                mappingManager.content.controls[1].leading.name = icons.FORMAT_INDENT_INCREASE
                mappingManager.content.controls[2] = Text("selcted type :"+type)
                mappingManager.actions = [ft.TextButton("Back",icon=icons.ARROW_BACK,on_click= lambda e:mappingController(2))]
                
            refreshUI()
            page.open(mappingManager)

                
        
        
       
        ##################################### ACTION BUTTON - ADD MAPPING #######################
        
        page.floating_action_button = ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.ADD,color=ft.colors.WHITE), ft.Text("Add Mapping",color=ft.colors.WHITE)], alignment="center", spacing=5
        ),
        bgcolor=MAIN_COLOR,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=200,
        mini=True,
        on_click=lambda e: mappingController(1)
    )        
        ############################## APP BAR ##################################################        

        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.SD_CARD_SHARP,color=ft.colors.WHITE),
            title=ft.Text("SDcatcher",color=ft.colors.WHITE),
            center_title=True,
            bgcolor=MAIN_COLOR,
            actions=[
                ft.PopupMenuButton(
                    icon_color=ft.colors.WHITE,
                    items=[
                        ft.PopupMenuItem(text="Settings",icon=ft.icons.SETTINGS,on_click=lambda e: page.open(settingsManager)),
                        ft.PopupMenuItem(text="Github",icon=ft.icons.WEB),
                        ft.PopupMenuItem(text="Check update",icon=ft.icons.UPDATE,on_click=lambda e:  page.open(updateManager)),
                    ]
                ),
            ],
        )

    


        ##################################  TABS   ############################################
       

        t = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            scrollable=True,
            indicator_color=MAIN_COLOR,
            label_color=MAIN_COLOR,
            tabs=[
                ft.Tab(
                    text="My Mappings",
                    icon=ft.icons.LIST_ALT,
                    
                    
                ),
                ft.Tab(
                    text="Feedback",
                    icon=ft.icons.FEEDBACK,
                    content=ft.Column(                        
                        )
                ),
            ],
            expand=1,
        )
        
        ############################### BUILD #################################

        
        updateInterface()
        page.add(t)
        page.add(launcherButton)
        
    ft.app(main, assets_dir="assets")

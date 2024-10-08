import flet as ft
from flet import *
import launcher,dialog,settings
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
        launcherButton = ft.TextButton()

        def updateInterface() :
            t.tabs[0].content=ft.Column(dataLoader(),scroll=ft.ScrollMode.ADAPTIVE)
            launcherUpdate()
            page.update()


        def showNotification(notificationMessage,undo=None) :
            def undoManager(e,undo) :
                undo(e)
                snackbar.duration=1
                snackbar.show_close_icon=False
                snackbar.open=True
                updateInterface()
            textContent = ft.Text(notificationMessage,color=ft.colors.BLACK)
            undoButton = ft.TextButton("Undo",icon=ft.icons.UNDO_OUTLINED,style=ButtonStyle(color=MAIN_COLOR),on_click=lambda e:undoManager(e,undo))
            snackbar = ft.SnackBar(
                content="",
                bgcolor=ft.colors.INDIGO_50,
                show_close_icon=True,
                close_icon_color=ft.colors.BLACK,                
                #behavior=ft.SnackBarBehavior.FLOATING
                )
            if undo!=None :
                snackbar.content=ft.Row([textContent,undoButton],alignment=ft.MainAxisAlignment.START)
            else :
                snackbar.content = ft.Row([textContent],alignment=ft.MainAxisAlignment.START)
                
            page.overlay.append(snackbar)
            snackbar.open=True
            page.update()

        ##################################### MAPPING CONTROLS ##################################
       
        
        def fooCreate() :
            settings.createNewMapping("ZV1","/Volumes/ZV1/PRIVATE/M4ROOT/CLIP/","/Users/yehdar/Pictures/ZV1/CLIPS/","video",".mp4")
            settings.createNewMapping("ZV1","/Volumes/ZV1/DCIM/100MSDCF/","/Users/yehdar/Pictures/ZV1/PICS/","photo",".jpg")
            updateInterface()
            showNotification("Mappings Created")
        
        def removeMapping(uuid) :
            mapping = settings.getMapping(uuid)
            undo = lambda e: settings.createNewMapping(mapping["name"], mapping["sourcePath"], mapping["destinationPath"], mapping["type"], mapping["format"])
            settings.removeMapping(uuid)
            updateInterface()
            showNotification("Removed mapping for "+mapping["name"]+" of type "+mapping["type"],undo)
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
                                            leading=ft.Icon(ft.icons.SD_CARD_ALERT_OUTLINED,color=ft.colors.BLACK),
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
        
        
        
        
        
       
        

        ##################################### MODALS ################################################
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
            )
        
        ##################################### ACTION BUTTON - ADD MAPPING #######################
        
        page.floating_action_button = ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.ADD,color=ft.colors.WHITE), ft.Text("Add Mapping",color=ft.colors.WHITE)], alignment="center", spacing=5
        ),
        bgcolor=MAIN_COLOR,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=200,
        mini=True,
        on_click=lambda e: fooCreate()
    )        
        ############################## APP BAR ##################################################        

        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.SD_CARD_SHARP,color=MAIN_COLOR),
            leading_width=100,
            title=ft.Text("SDcatcher",color=MAIN_COLOR),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.PopupMenuButton(
                    icon_color=MAIN_COLOR,
                    items=[
                        ft.PopupMenuItem(text="Settings",icon=ft.icons.SETTINGS,on_click=lambda e: updateInterface()),
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
            updateInterface()
        
        updateInterface()
        page.add(t)
        page.add(launcherButton)
    ft.app(main)

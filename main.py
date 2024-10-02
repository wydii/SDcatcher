import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)
import launcher,dialog,settings
import os,sys

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
        
        MAIN_COLOR = ft.colors.TEAL_400

        ##################################### SETTINGS LOADER ###################################
        
        data = settings.load()
        versionData = data["version"]
        mapTabs = []
        for mapping in data["mappings"] :
            name = mapping["name"]
            source = mapping["sourcePath"]
            destination = mapping["destinationPath"]
            type = mapping["type"]
            format = mapping["format"]

            icon = ft.icons.PHOTO_CAMERA if type=="photo" else ft.icons.MOVIE
            description = "Picture Mapping" if type =="photo" else "Video Mapping"


            mapTabs.append(ft.ExpansionTile(
                    title=ft.ListTile(leading=ft.Icon(icon),
                                    title=ft.Text(name),
                                    trailing=ft.PopupMenuButton(
                                    icon=ft.icons.MORE_VERT,
                                        items=[
                                            ft.PopupMenuItem(text="Modify",icon=ft.icons.EDIT),
                                            ft.PopupMenuItem(text="Remove",icon=ft.icons.REMOVE),
                                        ],
                                    ),),
                    subtitle=ft.Text(description),
                    affinity=ft.TileAffinity.LEADING,
                    icon_color=MAIN_COLOR,
                    text_color=MAIN_COLOR,
                    controls=[
                        ft.ListTile(
                            #title=ft.Text("Source : " ,weight=ft.FontWeight.BOLD, spans=[ft.TextSpan(source,ft.TextStyle(weight=ft.FontWeight.NORMAL))])
                            title=ft.Row([ft.FilledTonalButton(text="Source :",style=ft.ButtonStyle(padding=4)),ft.Text(source)])
                            ),
                        ft.ListTile(
                            #title=ft.Text("Destination : ",weight=ft.FontWeight.BOLD, spans=[ft.TextSpan(destination,ft.TextStyle(weight=ft.FontWeight.NORMAL))])
                            title=ft.Row([ft.FilledTonalButton(text="Destination :",style=ft.ButtonStyle(padding=4)),ft.Text(destination)])
                            
    
                            ),
                        ft.ListTile(
                            #title=ft.Text("Format : ",weight=ft.FontWeight.BOLD, spans=[ft.TextSpan(format,ft.TextStyle(weight=ft.FontWeight.NORMAL))])
                            title=ft.Row([ft.FilledTonalButton(text="Format :",style=ft.ButtonStyle(padding=8)),ft.Text(format)])
                            ),
                    ],
                ))


        ############################## FUNCTION FOR MAPPING ADDER ###############################

        def selectedVideo(e) :
            addType = "video"
            wizard.value = "Please insert your SD card and choose the "+addType+" source folder"
            typeWizard.name = ft.icons.MOVIE
            page.update()

        def selectedPhoto(e) :
            addType = "photo"
            wizard.value = "Please insert your SD card and choose the "+addType+" source folder"
            typeWizard.name = ft.icons.PHOTO_CAMERA
            page.update()


        #############################  FILE PICKER   #####################################
        

        # Open directory dialog
        def get_directory_result(e: FilePickerResultEvent):
            if e.path :
                sourcePath = e.path
                wizard.value = "You chose : "+sourcePath+" \nNow choose destination folder"

            else :
                wizard.value = "You've canceled your choice, please try again"
            page.update()

        

        
        ##################################### VARIABLE FOR MAPPING ADDER ################################################

        wizard = ft.Text(value="Please select one")
        typeWizard = ft.Icon()

        get_directory_dialog = FilePicker(on_result=get_directory_result)
        directory_path = Text()
        sourcePath = None
        addType = None



        ############################## APP BAR ##################################################
        #### Check update
        uptodate = ft.AlertDialog(
            title=ft.Text("Check if there is a new update of SdCatcher "),
            
            content=ft.Column([
                ft.Row([
                    ft.Chip(
                        label=ft.Text("Current vesion : ",
                            spans=[ft.TextSpan(versionData,ft.TextStyle(weight=ft.FontWeight.BOLD))]),
                        bgcolor= ft.colors.LIGHT_GREEN_ACCENT_100)
                ],alignment=ft.MainAxisAlignment.CENTER)
            ],height="40%")
        )

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
                        ft.PopupMenuItem(text="Settings",icon=ft.icons.SETTINGS),
                        ft.PopupMenuItem(text="Github",icon=ft.icons.WEB),
                        ft.PopupMenuItem(text="Check update",icon=ft.icons.UPDATE,on_click=lambda e: page.open(uptodate)),
                    ]
                ),
            ],
        )

    


        ##################################  TABS   ############################################
        # hide all dialogs in overlay
        page.overlay.extend([get_directory_dialog])

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
                    content=ft.Column(mapTabs,scroll=ft.ScrollMode.ADAPTIVE),
                    
                    
                ),
                ft.Tab(
                    text="Add new Mapping",
                    icon=ft.icons.ADD,
                    content=ft.Column(
                        [
                            ft.Row([
                                ft.TextButton("Photo Mapping",icon=ft.icons.PHOTO_CAMERA, on_click=selectedPhoto),
                                ft.TextButton(text="Video Mapping",icon=ft.icons.MOVIE, on_click=selectedVideo),
                                    ],alignment=ft.MainAxisAlignment.CENTER),
                            typeWizard,
                            ElevatedButton(
                                    "Open directory",
                                    icon=icons.FOLDER_OPEN,
                                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                                    disabled=page.web, ),
                            directory_path,
                            wizard,
                                    
                        ]
                        
                        
                        )
                ),
            ],
            expand=1,
        )
        
        ############################### BUILD #################################

        page.add(t)
    ft.app(main)

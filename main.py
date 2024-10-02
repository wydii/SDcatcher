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
        
        MAIN_COLOR = ft.colors.INDIGO_300
        SECOND_COLOR = ft.colors.INDIGO_300

        ##################################### ACTION BUTTON - ADD MAPPING #######################

        page.floating_action_button = ft.FloatingActionButton(
        content=ft.Row(
            [ft.Icon(ft.icons.ADD,color=ft.colors.WHITE), ft.Text("Add Mapping",color=ft.colors.WHITE)], alignment="center", spacing=5
        ),
        bgcolor=MAIN_COLOR,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=200,
        mini=True,
    )


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
                                            ft.PopupMenuItem(text="Remove",icon=ft.icons.REMOVE),
                                        ],
                                    ),),
                    subtitle=ft.Text(description),
                    affinity=ft.TileAffinity.LEADING,
                    icon_color=MAIN_COLOR,
                    text_color=MAIN_COLOR,
                    controls=ListTiles,
                ))


        ############################## FUNCTION FOR MAPPING ADDER ###############################

        

        #############################  FILE PICKER   #####################################
        
        

        
        ##################################### VARIABLE FOR MAPPING ADDER ################################################



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
                    text="Feedback",
                    icon=ft.icons.FEEDBACK,
                    content=ft.Column(
                        [
                                    
                        ]
                        
                        
                        )
                ),
            ],
            expand=1,
        )
        
        ############################### BUILD #################################

        page.add(t)
    ft.app(main)

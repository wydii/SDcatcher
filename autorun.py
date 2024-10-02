import flet as ft
import os,platforms

def minimize(page: ft.Page) :
    page.window.minimized = True
    page.update()

def eject(page : ft.Page,volumeName) :
    if platforms.getPlatform() == "Darwin" :
        command = "diskutil eject "+volumeName
        print("Attempting : "+command)
        os.system(command)
    page.window.close()

def loader(mappings):
    def progressBar(page: ft.Page) :

        # Variables
        message = ft.Text("Copying media")
        ejectButton = ft.TextButton("",disabled=True)
        button = ft.TextButton("Minimize",on_click= lambda e: minimize(page))
        mappingTitle = ft.Text("")
        initialCard = ft.ListTile(
                                leading=ft.ProgressRing(width=24, height=24, stroke_width = 2),
                                title=mappingTitle,
                                subtitle=message,
                            )
        volumeName = ""
        
        #Settings
        page.window.bgcolor = ft.colors.TRANSPARENT
        page.bgcolor = ft.colors.TRANSPARENT
        page.window.always_on_top=True
        page.window.movable=False
        page.window.resizable=False
        page.window.title_bar_hidden = True
        page.window.frameless = True
        page.window.alignment= ft.alignment.top_right
        page.window.width=300
        page.window.height=300
        page.window.skip_task_bar=True
        page.add(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            initialCard,
                            ft.Row(
                                [ejectButton,button],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]))))
        



        for mapping in mappings :
            volumeName = mapping["name"]
            mappingTitle.value = mapping["name"] +" "+ mapping["type"] +" Mapping"
            page.update()
            for media in os.listdir(mapping["sourcePath"]) :
                # Finding clips in source directory that matches 
                if os.path.basename(media)[-4:].lower() in mapping["format"].split(',') and os.path.basename(media)[0] != '.' :
                    clipAbsPath = mapping["sourcePath"]+media
                    destAbsPath = mapping["destinationPath"]+media
                    print ("MEDIA FOUND :",media)
                    if not os.path.exists(destAbsPath) :
                        message.value = "Copying " + media 
                        page.update()
                        platforms.copy_with_progress(clipAbsPath, destAbsPath)

        
        mappingTitle.value = mapping["name"] +" Mapping"
        message.value = "Media were copied successfully"
        button.text = "Close"
        initialCard.leading = ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.GREEN)
        button.on_click = lambda e: page.window.close()
        ejectButton.text = "Eject"
        ejectButton.icon = ft.icons.EJECT
        ejectButton.disabled = False
        ejectButton.on_click = lambda e: eject(page,volumeName)
        
        page.update()

    ft.app(progressBar)
    



import flet as ft
import json
import os
from datetime import datetime, timedelta
DATA_FILE="data/notes.json"



def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def main(page:ft.Page):
    page.title="lumiChron"
    page.theme_mode=ft.ThemeMode.LIGHT
    page.window.width=500
    page.window.height=300
    page.window_resizable=True
    page.theme_mode="light"
    page.splash=ft.ProgressBar(visible=False)

    date_picker=ft.DatePicker(
            on_change=lambda e:set_date(date_picker.value)
            )
    current_date=f"{datetime.now().year}\n{datetime.now().month}/{datetime.now().day}({datetime.now().strftime('%a')})"

    
    def change_date(offset):
        current_date=datetime.strptime(date_display.value.replace("\n"," "), "%Y %m/%d(%a)")
        new_date=current_date+timedelta(days=offset)
        date_display.value=f"{new_date.year}\n{new_date.month}/{new_date.day}({new_date.strftime('%a')})"
        page.update()
    def pick_date(e):
        date_picker.pick_date()

    def change_theme(e):
        page.splash.visible=True
        page.theme_mode="light" if page.theme_mode=="dark" else "dark"
        theme_button.selected= not theme_button.selected
        page.splash.visible=False
        page.update()

    def switch_screen(target):
        note_input_screen.visible=(target=="input")
        history_screen.visible=(target=="history")
        if target=="input":
            note_input.focus()
        else:
            history_screen.content=ft.Column([
                ft.Row([prev_button,date_display,next_button,calendar_button],alignment=ft.MainAxisAlignment.CENTER),
                history_list
                ])
        page.update()


    date_display=ft.Text(current_date,size=20,text_align=ft.TextAlign.CENTER)
    prev_button=ft.IconButton(ft.Icons.ARROW_LEFT,icon_size=50,on_click=lambda e:change_date(-1))
    next_button=ft.IconButton(ft.Icons.ARROW_RIGHT,icon_size=50,on_click=lambda e: change_date(1))
    calendar_button=ft.IconButton(ft.Icons.CALENDAR_MONTH,on_click=pick_date)
    history_list=ft.Column([])
    history_screen=ft.Container(
            content=ft.Column([
                ft.Row([prev_button,date_display,next_button,calendar_button],alignment=ft.MainAxisAlignment.CENTER),
                       history_list
                       ]),
            expand=True,
            visible=False
            )

    page.overlay.append(date_picker)


    theme_button=ft.IconButton(
            on_click=change_theme,
            icon="dark_mode",
            selected_icon="light_mode",
            )
    side_menu=ft.Container(
            content=ft.Column(
                [
                    ft.IconButton(ft.Icons.EDIT,icon_size=30,on_click=lambda e:switch_screen("input")),
                    ft.IconButton(ft.Icons.MENU_BOOK,icon_size=30,on_click=lambda e:switch_screen("history")),
                    theme_button
                ],
                alignment=ft.MainAxisAlignment.START
                ),
            width=50,
            margin=ft.margin.only(left=0,top=10,bottom=10),
            )
    note_input=ft.TextField(
            label="Note",
            expand=True,
            multiline=True,
            min_lines=1000000,
            border_radius=15,
            autofocus=True
            )
    note_input_screen=ft.Container(
            content=note_input,
            expand=True,
            visible=True
            )

    history_screen=ft.Container(
            content=ft.Column([
                ft.Text("History View"),
                ft.Text("this is where saved notes will be displayed."),
                ]),
            expand=True,
            visible=False
            )

    def save_note(e):
        words=note_input.value
        if not words.strip():
            return
        date=get_date()
        notes={}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE,"r",encoding="utf-8")as f:
                try:
                    notes=json.load(f)
                except json.JSONDecodeError:
                    notes={}

        if date not in notes:
            notes[date]=[]
        notes[date].append(words)

        with open(DATA_FILE,"w",encoding="utf-8") as f:
            json.dump(notes,f,ensure_ascii=False,indent=4)
        note_input.value=""
        note_input.update()

    def on_keypress(e:ft.KeyboardEvent):
        if e.key=="Escape":
            page.window.close()
        elif e.alt and e.key=="Enter":
            save_note(None)

    page.on_keyboard_event=on_keypress
    page.add(
            ft.Row([
                side_menu,
                ft.Stack([note_input_screen,history_screen],expand=True)
                ],expand=True)
            )
ft.app(target=main)



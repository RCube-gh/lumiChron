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
    page.window.width=550
    page.window.height=350
    page.window_resizable=True
    page.theme_mode="light"
    page.splash=ft.ProgressBar(visible=False)

    date_picker=ft.DatePicker(
            on_change=lambda e:set_date(date_picker.value)
            )
    current_date=f"{datetime.now().year}\n{datetime.now().month}/{datetime.now().day}({datetime.now().strftime('%a')})"



    def load_notes():
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def load_notes_for_date(date):
        notes=load_notes()
        history_list.controls.clear()
        if date in notes:
            for entry in notes[date]:
                history_list.controls.append(ft.Text(f"- {entry}",selectable=True,size=20,weight=ft.FontWeight.W_500))
        else:
            history_list.controls.append(ft.Text("_No notes for this day._", italic=True))
        history_list.update()
        page.update()




    def set_date(date):
        date_display.value=f"{date.year}\n{date.month}/{date.day}({date.strftime('%a')})"
        load_notes_for_date(date.strftime("%Y-%m-%d"))
        page.update()

    
    def change_date(offset):
        current_date=datetime.strptime(date_display.value.replace("\n"," "), "%Y %m/%d(%a)")
        new_date=current_date+timedelta(days=offset)
        set_date(new_date)

    def pick_date(e):
        page.dialog=date_picker
        date_picker.open=True
        page.update()

    def change_theme(e):
        page.splash.visible=True
        page.theme_mode="light" if page.theme_mode=="dark" else "dark"
        theme_button.selected= not theme_button.selected
        page.splash.visible=False
        if note_input_screen.visible:
            note_input.focus()
        page.update()

    def switch_screen(target):
        note_input_screen.visible=(target=="input")
        history_screen.visible=(target=="history")
        if target=="input":
            note_input.focus()
        else:
            load_notes_for_date(get_date())
        page.update()


    date_display=ft.Text(current_date,size=20,text_align=ft.TextAlign.CENTER)
    prev_button=ft.IconButton(ft.Icons.ARROW_LEFT,icon_size=50,on_click=lambda e:change_date(-1))
    next_button=ft.IconButton(ft.Icons.ARROW_RIGHT,icon_size=50,on_click=lambda e: change_date(1))
    calendar_button=ft.IconButton(ft.Icons.CALENDAR_MONTH,on_click=pick_date)
    history_list=ft.ListView(
            expand=True,
            spacing=15,
            auto_scroll=False
            )

    history_container=ft.Container(
            content=history_list,
            border=ft.border.all(2),
            border_radius=10,
            padding=ft.padding.all(10),
            margin=ft.margin.all(10),
            expand=True,
            width=float("inf"),
            )
    history_screen=ft.Container(
            content=ft.Column([
                ft.Row([prev_button,date_display,next_button,calendar_button],alignment=ft.MainAxisAlignment.CENTER),
                history_container,
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
            text_size=20,
            text_style=ft.TextStyle(font_family="Consolas",weight=ft.FontWeight.BOLD),
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



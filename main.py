import flet as ft
from flet import Page, Row, Column, Container, Text, TextField, Checkbox, Slider, IconButton, NumbersOnlyInputFilter, KeyboardType
import random


NUMBERS = '0123456789'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
SYMBOLS_BASE = '!@#$%^&*'
SYMBOLS_ADVANCE = '()[]{}<>/|\\=+-_.,\'\":;?~'
SIMILAR = '1Il0Oo'

all_chars = ''
result = ''

length = 14
min_num = 1
min_sym = 1
quantity = 1

def main(page: Page):
    page.title = "Password generator"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.spacing = 30
    page.window_height = 600
    page.window_width = 400
    page.window_min_height = 500
    page.window_min_width = 300
    page.window_always_on_top = True # for development
    
    def checkbox_signs(text, value_cond=True):
        return Checkbox(label=text, value=value_cond, label_position='right')
    
    cb_numbers = checkbox_signs("Numbers")
    cb_upper = checkbox_signs("Uppercase")
    cb_lower = checkbox_signs("Lowercase")
    cb_symbols = checkbox_signs("Symbols")
    cb_exclude_similar = checkbox_signs("Exclude similar", value_cond=True)
    
    def text_signs(text):
        return Text(text, color=ft.colors.with_opacity(0.5, ft.colors.PRIMARY))
    
    text_numbers = text_signs('0-9')
    text_upper = text_signs('A-Z')
    text_lower = text_signs('a-z')
    text_symbols_base = text_signs('!@#$%^&*')
    text_similar = text_signs('1Il0Oo')
    
    numbers = Row([cb_numbers, text_numbers])
    upper = Row([cb_upper, text_upper])
    lower = Row([cb_lower, text_lower])
    symbols_base = Row([cb_symbols, text_symbols_base])
    
    table_checkboxes = ft.DataTable(
        horizontal_margin=0,
        column_spacing=0,
        data_row_max_height=35,
        divider_thickness=0.01,
        heading_row_height=0,
        columns=[
            ft.DataColumn(ft.Text("Checkbox"), numeric=True), 
            ft.DataColumn(ft.Text("Text"), numeric=True),
            ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(text_numbers),
                ft.DataCell(cb_numbers),
                ]),
            ft.DataRow(cells=[
                ft.DataCell(text_upper),
                ft.DataCell(cb_upper),
                ]),
            ft.DataRow(cells=[
                ft.DataCell(text_lower),
                ft.DataCell(cb_lower),
                ]),
            ft.DataRow(cells=[
                ft.DataCell(text_symbols_base),
                ft.DataCell(cb_symbols),
                ]),
            ft.DataRow(cells=[
                ft.DataCell(text_similar),
                ft.DataCell(cb_exclude_similar),
                ]),
            ],
    )
    
    text_all_chars = Text(f'{all_chars}')
    
    icon_button_gen = IconButton(icon=ft.icons.REPEAT_ROUNDED, tooltip="Generate")
    icon_button_copy = IconButton(icon=ft.icons.COPY_ROUNDED, tooltip="Copy")
    
    slider_length = Slider(min=4, max=28, value=length, divisions=24, label="{value}")
    input_length = TextField(
        label="Length", 
        value=f"{length}", 
        text_align="right", 
        width=80, 
        input_filter=NumbersOnlyInputFilter(), 
        keyboard_type=KeyboardType.NUMBER,
        )
    
    input_signs = TextField(
        label="Signs", 
        value=f"{all_chars}", 
        text_align="left", 
        multiline=True,
        #disabled=True,
        #width=400,
        )
    
    text_result = Text(f'{result}', font_family="Menlo", selectable=True)
    
    conteiner_result = Container(
        content=Row([text_result, icon_button_gen, icon_button_copy], spacing=0),
        padding=10,
        border_radius=10,
        border=ft.border.all(2, ft.colors.with_opacity(0.5, ft.colors.PRIMARY)),
        #bgcolor=ft.colors.with_opacity(0.1, ft.colors.PRIMARY)
        )
    
    
    def cb_handler(checkbox, VAR):
        global all_chars
        for char in VAR:
            if checkbox.value and char not in all_chars:
                all_chars += char
            elif not checkbox.value and char in all_chars:
                all_chars = all_chars.replace(char, '')
        page.update()
    
    def del_sim(checkbox, VAR):
        global all_chars
        if checkbox.value:
            for char in VAR:
                if char in all_chars:
                    all_chars = all_chars.replace(char, '')
    
    def chars_selection(e):
        cb_handler(cb_numbers, NUMBERS)
        cb_handler(cb_upper, UPPER)
        cb_handler(cb_lower, LOWER)
        cb_handler(cb_symbols, SYMBOLS_BASE)
        del_sim(cb_exclude_similar, SIMILAR)
        input_signs.value = all_chars
        #print(all_chars)
        generate_handler(None)
        page.update()
    
    def input_chars_handler(e):
        global all_chars
        all_chars = input_signs.value
        page.update()
    
    def lenght_change_input(e):
        global length
        if input_length.value == '':
            length = 4
            slider_length.value = 4
            input_length.value = '4'
            input_length.error_text = '4 min.'
        elif int(input_length.value) < 4:
            length = 4
            slider_length.value = 4
            input_length.value = '4'
            input_length.error_text = '4 min.'
        elif int(input_length.value) >= 4:
            length = int(input_length.value)
            slider_length.value = int(length)
            input_length.error_text = None
        generate_handler(None)
        page.update()
    
    def lenght_change_slider(e):
        global length
        length = int(slider_length.value)
        input_length.value = str(int(length))
        input_length.error_text = None
        generate_handler(None)
        page.update()
    
    def generate_password(length, all_chars):
        global result
        result = ''
        for i in range(length):
            result += random.choice(all_chars)
        return result
    
    def generate_handler(e):
        if all_chars != '':
            global result
            result = generate_password(length, all_chars)
            text_result.value = result
        page.update()
    
    def validate_checkboxes(e):
        if all([cb_numbers.value==False, cb_upper.value==False, cb_lower.value==False, cb_symbols.value==False]):
            icon_button_gen.disabled = True
            icon_button_copy.disabled = True
            text_result.color = ft.colors.RED
            text_result.value = 'Nothing selected'
        else:
            icon_button_gen.disabled = False
            icon_button_copy.disabled = False
            text_result.color = ft.colors.ON_BACKGROUND
        page.update
    
    def checkboh_handler(e):
        validate_checkboxes(None)
        chars_selection(None)
    
    def copy_result(e):
        page.set_clipboard(result)
    
    cb_numbers.on_change = checkboh_handler
    cb_upper.on_change = checkboh_handler
    cb_lower.on_change = checkboh_handler
    cb_symbols.on_change = checkboh_handler
    cb_exclude_similar.on_change = checkboh_handler
    
    input_length.on_change = lenght_change_input
    slider_length.on_change = lenght_change_slider
    input_signs.on_change = input_chars_handler
    
    icon_button_gen.on_click = generate_handler
    icon_button_copy.on_click = copy_result
    
    chars_selection(None)
    generate_handler(None)
    
    page.add(
        Row([conteiner_result], alignment="center"),
        #Row([icon_button_gen, icon_button_copy], alignment="center"),
        Row([table_checkboxes], alignment="center"),
        Row([Column([input_length, slider_length], spacing=0, horizontal_alignment="center")], alignment="center"),
        #Row([input_signs], alignment="center"),
        
        #Row([Column([numbers, upper, lower, symbols_base, similar], spacing=0, horizontal_alignment="start")], alignment="center"),
        # Row([
        #     Column([cb_numbers, cb_upper, cb_lower, cb_symbols], spacing=0, horizontal_alignment="end"),
        #     Column([text_numbers, text_upper, text_lower, text_symbols_base, text_similar], spacing=12), 
        #     ], spacing=0, alignment="center"),
        )

if __name__ == "__main__":
    ft.app(target=main)

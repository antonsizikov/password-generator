import flet as ft
from flet import Page, Row, Column, Container, Text, TextSpan, TextStyle, TextField, Checkbox, Slider, IconButton, NumbersOnlyInputFilter, KeyboardType
import random


NUMBERS = '0123456789'
UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER = 'abcdefghijklmnopqrstuvwxyz'
SYMBOLS_BASE = '!@#$%^&*'
SYMBOLS_ADVANCE = '()[]{}<>/|\\=+-_.,\'\":;?~'
SIMILAR = '1Il0Oo'

all_chars = ''
result = ''
colorized_results = Text()

length = 14
min_num = 1
min_sym = 1
quantity = 1

def main(page: Page):
    page.title = "Password generator"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.spacing = 15
    page.padding = 0
    page.window_height = 600
    page.window_width = 400
    page.window_min_height = 500
    page.window_min_width = 350
    #page.window_always_on_top = True # for development
    page.fonts = {"MonaspaceNeon": "/fonts/MonaspaceNeon-Regular.otf"}
    
    def checkbox_signs(text, value_cond=True):
        return Checkbox(label=text, value=value_cond, label_position='right')
    
    cb_numbers = checkbox_signs("Numbers")
    cb_upper = checkbox_signs("Uppercase")
    cb_lower = checkbox_signs("Lowercase")
    cb_symbols = checkbox_signs("Symbols")
    cb_exclude_similar = checkbox_signs("Exclude similar", value_cond=True)
    
    def text_signs(text):
        return Text(text, font_family="MonaspaceNeon", color=ft.colors.with_opacity(0.5, ft.colors.SECONDARY))
    
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
        border_color=ft.colors.ON_BACKGROUND,
        focused_border_color=ft.colors.PRIMARY,
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
    
    icon_rate = ft.Icon(name=None)
    conteiner_icon_rate = Container(content=icon_rate, padding=ft.padding.only(right=10))
    text_result = Text(f'{result}', font_family="MonaspaceNeon", selectable=True)
    conteiner_result_text = Container(content=text_result, alignment=ft.alignment.center, width=170)
    conteiner_result = Container(
        content=Row([conteiner_icon_rate, conteiner_result_text, icon_button_gen, icon_button_copy], alignment='end', spacing=0),
        padding=10,
        border_radius=10,
        height=80,
        alignment=ft.alignment.center_right,
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
        generate_handler(None)
        page.update()
    
    def lenght_change_slider(e):
        global length
        length = int(slider_length.value)
        input_length.value = str(int(length))
        input_length.error_text = None
        generate_handler(None)
        page.update()
    
    def lenght_change_input(e):
        global length
        if input_length.value == '':
            length = 4
            slider_length.value = 4
            #input_length.value = '4'
            input_length.error_text = '4 min.'
        elif int(input_length.value) < 4:
            length = 4
            slider_length.value = 4
            #input_length.value = '4'
            input_length.error_text = '4 min.'
        elif int(input_length.value) >= 4:
            length = int(input_length.value)
            slider_length.value = int(length)
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
            
            global colorized_results
            colorized_results = text_colorize(result)
        difficulty_rating(result)
        #print(result)
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
    
    def difficulty_rating(result):
        def dif_rate(icon, color):
            opas = 0.8
            icon_rate.name=icon
            icon_rate.color=ft.colors.with_opacity(opas, color)
            conteiner_result.border=ft.border.all(2, ft.colors.with_opacity(opas, color))
            conteiner_result.bgcolor=ft.colors.with_opacity(0.1, color)
            #page.theme = ft.Theme(color_scheme_seed=color)
        
        def rate_weak():
            dif_rate(ft.icons.DANGEROUS_ROUNDED, ft.colors.RED)
        
        def rate_medium():
            dif_rate(ft.icons.WARNING_ROUNDED, ft.colors.AMBER)
        
        def rate_strong():
            dif_rate(ft.icons.CHECK_CIRCLE_ROUNDED, ft.colors.GREEN)
        
        if len(result) < 10:
            rate_weak()
        elif len(result) >= 10 and len(result) < 14:
            rate_medium()
        elif len(result) >= 14:
            rate_strong()
    
    def text_colorize(result):
        def color_number(char):
            return TextSpan(f'{char}', TextStyle(color=ft.colors.BLUE)),
        
        def color_symbol(char):
            return TextSpan(f'{char}', TextStyle(color=ft.colors.RED)),
        
        def simple_text(char):
            return TextSpan(f'{char}'),
        
        colorized_result_spans = []
        
        for char in result:
            if char in NUMBERS:
                colorized_result_spans += color_number(char)
            elif char in SYMBOLS_BASE:
                colorized_result_spans += color_symbol(char)
            else:
                colorized_result_spans += simple_text(char)
        
        return Text(selectable=True, font_family="MonaspaceNeon", spans=colorized_result_spans)
    
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
    
    page.add(
        Row([conteiner_result], alignment="center"),
        Row([Column([slider_length, input_length], spacing=0, horizontal_alignment="center")], alignment="center"),
        Row([table_checkboxes], alignment="center"),
        #Row([input_signs], alignment="center"),
        #Row([colorized_results], alignment="center"),
        
        # Old Designs
        
        #Row([Column([numbers, upper, lower, symbols_base, similar], spacing=0, horizontal_alignment="start")], alignment="center"),
        
        # Row([
        #     Column([cb_numbers, cb_upper, cb_lower, cb_symbols], spacing=0, horizontal_alignment="end"),
        #     Column([text_numbers, text_upper, text_lower, text_symbols_base, text_similar], spacing=12), 
        #     ], spacing=0, alignment="center"),
        
        )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

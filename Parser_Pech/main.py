import connection_to_db as c
import functions as f
import PySimpleGUI as sg

sg.theme('DarkBrown5')
layout = [
    [sg.Text('Путь к вашему файлу с логами'), sg.InputText(), sg.FileBrowse()    
     ],
    [sg.Text('Название хоста'), sg.InputText(size=30),
     sg.Text('Введите ip'), sg.InputText(size=(20)), sg.Button(button_text='Отфильтровать по ip')   
     ],
    [sg.Text('Имя пользователя'), sg.InputText(size=20),
     sg.Text('Введите дату'), sg.InputText(size=12), sg.Button(button_text='Отфильтровать по дате')    
     ],
    [sg.Text('Пароль от MySQL'), sg.InputText(size=20), sg.Button(button_text='Подключиться к базе и файлу'),
     sg.Checkbox('Отобразить в формате JSON', key='_json_')
     ],
    [sg.Output(size=(100, 20), key = '_output_')],
    [sg.Cancel(), sg.Button(button_text='Очистить вывод')]
]

window = sg.Window('Parser', layout)

while True:
    event, values = window.read()
    json = window.FindElement('_json_').get()

    if event in (None, 'Exit', 'Cancel'):
        break
    
    elif event == 'Очистить вывод':
        window.FindElement('_output_').Update('')

    elif event == 'Отфильтровать по дате':
        date = values[4]
        try:
            window.FindElement('_output_').Update('')
            c.execute_select(c.select_date(date), connection, json)
        except:
            f.prompt('Упс, что-то пошло не так')

    elif event == 'Отфильтровать по ip':
        ip = values[2]
        try:
            window.FindElement('_output_').Update('')
            c.execute_select(c.select_ip(ip), connection, json)
        except:
            f.prompt('Упс, что-то пошло не так')

    elif event == 'Подключиться к базе и файлу':
        window.FindElement('_output_').Update('')

        file = values[0]
        hostname = values[1]
        username = values[3]
        user_password = values[5]
        
        
        connection = c.create_connection_with_server(hostname, username, user_password)
        connection = c.create_connection_with_bd(hostname, username, user_password)

        try:
            c.execute_sql(c.create_table_log(), connection)
        except:
            pass
        
        try:
            array_logs = f.file_into_array(file)
            for log in array_logs:
                c.execute_sql(f.seporator(log), connection)          
        except:
            f.prompt('Мы не можем найти ваш файлик :(')
        
        try:
            c.execute_select(c.select_all(), connection, json)
        except:
            f.prompt('Упс! Что-то пошло не так')

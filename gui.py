from audio_gen import main
import PySimpleGUI as sg

sg.theme('Light Blue 2')

layout = [
        [sg.Text('Choose an "audios" folder'), sg.Input(), sg.FolderBrowse()],
        [sg.Submit('Generate', key='generate'), sg.Cancel('Quit')],
        [sg.Text('Idle                          ', key='status')],
        [sg.Text('Choose output file'), sg.Input(), sg.FileSaveAs(
            'Browse...',
            file_types=[('Ogg Vorbis Audio File', '*.ogg')],
            disabled=True, key='save_browse'
        )],
        [sg.Submit('Save', key='save')],
]

window = sg.Window('File Compare', layout)

while True:
    event, values = window.read()
    print(f'You clicked {event}')
    if event == 'Quit': exit(0)
    if event == 'generate':
        window['generate'].update(disabled=True)
        window['save'].update(disabled=False)
        window['status'].update(value='Generating...')
    if event == 'save':
        window['save_browse'].update(value='Save complete!')
        window['status'].update(value='Save complete!')
    # main(audio_folder=values[0])

window.close()

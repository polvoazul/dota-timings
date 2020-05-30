#!/usr/bin/env python3
from audio_gen import main
import PySimpleGUI as sg
import threading, time, sys, queue, os


sg.theme('Light Blue 2')

layout = [
        [sg.Text('Choose an input audios folder'), sg.Input(key='input'), sg.FolderBrowse()],
        [sg.Text('Choose output file           '), sg.Input(key='output'), sg.FileSaveAs(
            'Browse', file_types=[('Ogg Vorbis Audio File', '*.ogg')], key='save_browse'
        )],
        [sg.Submit('Generate new audio', key='action'), sg.Cancel('Quit')],
        [sg.Text('Idle', key='status', size=(80, 5))],
]

window = sg.Window('Dota2 Timings Audio Generator', layout)
status = window['status']
action = window['action']
gui_queue = queue.Queue()

def main():
    while True:
        event, values = window.read(timeout=500)
        if event != '__TIMEOUT__':
            print(f'You clicked {event}')
        if event == 'Quit' or event is None: break
        if event == 'action': go()
        treat_messages()

    window.close()

def treat_messages():
    while True:
        try: message = gui_queue.get_nowait()
        except queue.Empty: break
        if isinstance(message, Exception):
            show_error(message)
        elif message == END:
            action.update(disabled=False)
        else:
            status.update(status.get() + message)

def show_error(e):
    status.update(value= f'ERROR: \n\t{e.__class__}\n\t{e.msg}\n\t{e.file}:{e.line}')

def pack_exception(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    e.type, e.file, e.line, e.msg = exc_type, fname, exc_tb.tb_lineno, str(exc_obj)

def go():
    input, output = window['input'].get(), window['output'].get()
    status.update(value=''); window.refresh(); time.sleep(0.1)
    try:
        assert input, 'Please fill input audio folder field'
        assert output, 'Please fill output audio field'
        thread = threading.Thread(target=audio_generator, args=(gui_queue, input, output), daemon=True)
        thread.start()
        action.update(disabled=True)
    except Exception as e:
        pack_exception(e)
        show_error(e)

class END: pass
def audio_generator(gui_queue, input, output):
    try:
        import audio_gen
        audio_gen.generate_file(input, output)
        time.sleep(2)  # sleep for a while as a simulation of a long-running computation
        # at the end of the work, before exiting, send a message back to the GUI indicating end
        gui_queue.put('done')
    except Exception as e:
        pack_exception(e)
        gui_queue.put(e)
    finally:
        gui_queue.put(END)

main()

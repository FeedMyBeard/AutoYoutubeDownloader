from typing import Text
from weakref import finalize
import PySimpleGUI as sg
from pytube import YouTube

sg.theme("Black")


def progress_check(stream, chunk, bytes_remain):
    progress_amount = 100 - round(bytes_remain / stream.filesize * 100)
    window['-DOWNLOADPROGRESS-'].update(progress_amount)
    # print(progress_amount)
    return progress_amount


def on_complete(stream, file_path):
    window['-DOWNLOADPROGRESS-'].update(0)


start_layout = [
    [sg.Input(key="-INPUT-"), sg.Button("Submit", key="-SUBMIT-")]
]

info_tab = [
    [sg.Text('Title:'), sg.Text('', key='-TITLE-')],
    [sg.Text('Length:'), sg.Text('', key='-LENGTH-')],
    [sg.Text('Views:'), sg.Text('', key='-VIEWS-')],
    [sg.Text('Author:'), sg.Text('', key='-AUTHOR-')],
    [sg.Text('Description:'),
     sg.Multiline('', key='-DESCRIPTION-', size=(40, 20), no_scrollbar=True, disabled=True)
     ]]
download_tab = [
    [sg.Frame('Best Quality',
              [[sg.Button('Download', key='-BEST-'), sg.Text('', key='-BESTRES-'), sg.Text('', key='-BESTSIZE-')]])],
    [sg.Frame('Worst Quality',
              [[sg.Button('Download', key='-WORST-'), sg.Text('', key='-WORSTRES-'), sg.Text('', key='-WORSTSIZE-')]])],
    [sg.Frame('Audio', [[sg.Button('Download', key='-AUDIO-'), sg.Text('', key='-AUDIOSIZE-')]])],
    [sg.VPush()],
    #[sg.Frame('Select Destination: ',
     #         [[sg.Input(key="-DESTINATION-"), sg.FileBrowse('Browse', key='-DESTINATION-')]])],
    [sg.Progress(100, orientation='h', size=(20, 20), key='-DOWNLOADPROGRESS-', expand_x=True)]
]

layout = [
    [
        sg.TabGroup([[sg.Tab("info", info_tab),
                      sg.Tab("download", download_tab)
                      ]])]

]

window = sg.Window('Youtube Video Downloader', start_layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "-SUBMIT-":
        video_object = YouTube(values["-INPUT-"], on_progress_callback=progress_check, on_complete_callback=on_complete)
        window.close()

        window = sg.Window('Youtube Video Downloader', layout, finalize=True)
        window["-TITLE-"].update(video_object.title)
        window['-LENGTH-'].update(f'{round(video_object.length / 60, 2)} minutes')
        window['-VIEWS-'].update(video_object.views)
        window['-AUTHOR-'].update(video_object.author)
        window['-DESCRIPTION-'].update(video_object.description)

        # main window download setup
        window['-BESTSIZE-'].update(f'{round(video_object.streams.get_highest_resolution().filesize / 1048576, 1)} MB')
        window['-BESTRES-'].update(video_object.streams.get_highest_resolution().resolution)

        window['-WORSTSIZE-'].update(f'{round(video_object.streams.get_lowest_resolution().filesize / 1048576, 1)} MB')
        window['-WORSTRES-'].update(video_object.streams.get_lowest_resolution().resolution)

        window['-AUDIOSIZE-'].update(f'{round(video_object.streams.get_audio_only().filesize / 1048576, 1)} MB')

    if event == "-BEST-":
        video_object.streams.get_highest_resolution().download()
    if event == "-WORST-":
        video_object.streams.get_lowest_resolution().download()
    if event == "-AUDIO-":
        video_object.streams.get_audio_only().download()

window.close()
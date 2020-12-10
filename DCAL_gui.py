import PySimpleGUI as sg
from DCAL import DCAL

sg.theme('Reddit')

## Defining layout of the GUI
## Defining top input layer
input_layer = [
    [
        sg.Text('Energy: '),
        sg.Combo(['6X', '10X'], size = (25,1), key='-ENERGY-', default_value='6X')
    ],
    [
        sg.Text('Field Size X (cm): '),
        sg.InputText(default_text= '0.0', size = (25,1), key='-FSX-', justification='left')
    ],
    [
        sg.Text('Field Size Y (cm): '),
        sg.InputText(default_text= '0.0', size = (25,1), key='-FSY-', justification='left')
    ],
    [
        sg.Text('Pin Depth (cm): '),
        sg.InputText(default_text= '0.0', size = (25,1), key='-DEPTH-', justification='left')
    ],
    [
        sg.Text('Shielding (%): '),
        sg.InputText(default_text= '0.0', size = (25,1), key='-SHIELDING-', justification='left')
    ],
    [
        sg.Button("Calculate", enable_events=True, key='-CALCULATE-', bind_return_key=True),
        sg.Text('Powered by DRO Physics (10/12/20): ',font=('Helvetica', 8), justification='right')
    ]
]

## Defining bottow output layer
output_layer = [
    [sg.Text('Equivalent Square Field (cm): ',font=('Helvetica', 14)), sg.Text(size=(12,1), key='-ESQ-',font=('Helvetica', 14))],
    [sg.Text('Tissue Maximum Ratio (TMR): ',font=('Helvetica', 14)), sg.Text(size=(12,1), key='-TMR-',font=('Helvetica', 14))],
    [sg.Text('Relative Output Factor (ROF): ',font=('Helvetica', 14)), sg.Text(size=(12,1), key='-ROF-',font=('Helvetica', 14))],
    [sg.Text('MU for 100 cGy: ', text_color='red',font=('Helvetica', 14)), sg.Text(size=(12,1), key='-MU-', text_color='red',font=('Helvetica', 14))]
]

## Defining total layout
layout = [
    [
        sg.Column(input_layer),
        sg.VSeparator(),
        sg.Column(output_layer)
    ]
]
# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

## Start the Window
window = sg.Window(title="DCal", layout=layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

    ## If CALCULATE
    if event == '-CALCULATE-':
        try:
            energy = values['-ENERGY-']
            depth = float(values['-DEPTH-'])
            fs_x = float(values['-FSX-'])
            fs_y = float(values['-FSY-'])
            shielding = float(values['-SHIELDING-'])
            dcal_output = DCAL(energy, depth, fs_x, fs_y, 1.0 , shielding).GrabResults()
        except:
            sg.popup('Invalid Values')

        if 'ESQ' in dcal_output:
            window['-ESQ-'].update('{:.1f}'.format(dcal_output['ESQ']))
            window['-TMR-'].update('{:.3f}'.format(dcal_output['TMR']))
            window['-ROF-'].update('{:.3f}'.format(dcal_output['ROF']))
            window['-MU-'].update('{:.1f}'.format(dcal_output['MU']))
        else:
            sg.popup(dcal_output)

window.close()

import PySimpleGUI as sg
from DCAL import DCAL

sg.theme('Reddit')

## Defining layout of the GUI
## Defining top input layer
input_layer = [
    [
        sg.Checkbox('Asymmetric Field (OAR)',  enable_events=True, default=False, key='-ASYM-', size = (25,1)), 
        sg.Checkbox('SSD Setup',  enable_events=True, default=False, key='-SSDBox-', size = (25,1))
    ],
    [
        sg.Text('Energy: '),
        sg.Combo(['6X', '10X'], size = (25,1), key='-ENERGY-', default_value='6X')
    ],
    [
        sg.Text('Field Size X (cm): '),
        sg.InputText(default_text= '0.0', size = (25,1), key='-FSX-', justification='left', disabled=False)
    ],
    [
        sg.Text('Field Size X1 (cm): '),
        sg.InputText(default_text= 'NA', size = (12,1), key='-FSX1-', justification='left', disabled=True),
        sg.Text('Field Size X2 (cm): '),
        sg.InputText(default_text= 'NA', size = (12,1), key='-FSX2-', justification='left', disabled=True)
    ],
    [
        sg.Text('Field Size Y (cm): '),
        sg.InputText(default_text= '0.0', size = (25,1), key='-FSY-', justification='left', disabled=False)
    ],
    [
        sg.Text('Field Size Y1 (cm): '),
        sg.InputText(default_text= 'NA', size = (12,1), key='-FSY1-', justification='left', disabled=True),
        sg.Text('Field Size Y2 (cm): '),
        sg.InputText(default_text= 'NA', size = (12,1), key='-FSY2-', justification='left', disabled=True)
    ],
    [
        sg.Text('Pin Depth (cm): '),
        sg.InputText(default_text= '0.0', size = (25,1), key='-DEPTH-', justification='left')
    ],
    [
        sg.Text('SSD (cm): '),
        sg.InputText(default_text= 'NA', size = (25,1), key='-SSD-', justification='left')
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
    [sg.Text('OAR: ',font=('Helvetica', 14)), sg.Text(size=(12,1), key='-OAR-',font=('Helvetica', 14))],
    [sg.Text('PDD at depth:                ',font=('Helvetica', 14), key='-PDD_text-'), sg.Text(size=(12,1), key='-PDD_value-',font=('Helvetica', 14))],
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

    ## If SSD setup
    if values['-SSDBox-'] == True: 
        window.FindElement('-SSD-').Update(disabled = False)
    else: 
        window.FindElement('-SSD-').Update(value='NA', disabled = True)

    ## if Asymmetric field and oar is required
    if values['-ASYM-'] == True: 
        window.FindElement('-FSX1-').Update(disabled = False)
        window.FindElement('-FSX2-').Update(disabled = False)
        window.FindElement('-FSY1-').Update(disabled = False)
        window.FindElement('-FSY2-').Update(disabled = False)
        window.FindElement('-FSX-').Update(value='NA', disabled = True)
        window.FindElement('-FSY-').Update(value='NA', disabled = True)
    else: 
        window.FindElement('-FSX1-').Update(value='NA', disabled = True)
        window.FindElement('-FSX2-').Update(value='NA', disabled = True)
        window.FindElement('-FSY1-').Update(value='NA', disabled = True)
        window.FindElement('-FSY2-').Update(value='NA', disabled = True)
        window.FindElement('-FSX-').Update(disabled = False)
        window.FindElement('-FSY-').Update(disabled = False)

    ## If CALCULATE
    if event == '-CALCULATE-':
        # try:
        if values['-ASYM-'] == False:
        ## Read in field size as a list of first and second jaw position
            fs_x = [float(values['-FSX-'])/2] * 2
            fs_y = [float(values['-FSY-'])/2] * 2 
        else: 
            fs_x = [float(values['-FSX1-']), float(values['-FSX2-'])]
            fs_y = [float(values['-FSY1-']), float(values['-FSY2-'])]

        energy = values['-ENERGY-']
        depth = float(values['-DEPTH-'])
        shielding = float(values['-SHIELDING-'])

        # Update Depth in SSD 
        if values['-SSDBox-'] == True: 
            window.FindElement('-PDD_text-').Update(value='PDD at depth ' + str(depth) + ' cm: ')
            # window.FindElement('-PDD_text-').Update(value='123')
        else: 
            window.FindElement('-PDD_text-').Update(value='PDD at depth : ')

        dcal_output = DCAL(energy, depth, fs_x, fs_y, shielding, [values['-SSDBox-'], values['-SSD-']]).GrabResults()
        # except:
        #     sg.popup('Invalid Values')

        if 'ESQ' in dcal_output:
            if values['-SSDBox-'] == True: 
                window['-PDD_value-'].update('{:.1f}'.format(dcal_output['PDD']))
            else: 
                window['-PDD_value-'].update('NA')

            window['-OAR-'].update('{:.3f}'.format(dcal_output['OAR']))
            window['-ESQ-'].update('{:.1f}'.format(dcal_output['ESQ']))
            window['-TMR-'].update('{:.3f}'.format(dcal_output['TMR']))
            window['-ROF-'].update('{:.3f}'.format(dcal_output['ROF']))
            window['-MU-'].update('{:.1f}'.format(dcal_output['MU']))
        else:
            sg.popup(dcal_output)

window.close()

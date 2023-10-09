import datetime
from openpyxl import load_workbook

spreadsheet_route = 'FOR-PS-03.xlsx'

workbook = load_workbook(spreadsheet_route)

if 'Datos' in workbook.sheetnames:
    workbook.remove(workbook['Datos'])

worksheet = workbook['Detalle']

headers = [
    'Timestamp',
    'Guia de seguimiento',
    'Devcognita evaluado',
    'Fecha del seguimiento',
    'Avance al plan de formacion',
    'Proactividad en el estudio',
    'Comunicacion en la sesion',
    'Desarrollo de acuerdos pendientes del seguimiento anterior',
    'Fit con el seniority',
    'Evolucion tecnica',
    'Capacidad recursiva y de investigacion',
    'Observaciones',
    'Promedio'
]

for column, header in zip(worksheet.iter_cols(min_row=1, max_row=1, max_col=len(headers)), headers):
    column[0].value = header

current_row = 2
for row in worksheet.iter_rows(min_row=2, min_col=1, max_col=13):
    cell_c = row[2]
    cell_d = row[3]
    cell_m = row[12]

    if cell_c.value is not None:
        cell_c_coordinate = cell_c.coordinate
        if cell_c_coordinate != 'C1':
            worksheet[cell_c_coordinate] = cell_c.value.strip()
    else:
        break

    if cell_d.value is not None:
        cell_d_coordinate = cell_d.coordinate
        if cell_d_coordinate != 'D1':
            worksheet[cell_d_coordinate].number_format = 'mm/dd/yyyy'

    if cell_c.value is not None:
        cell_m_coordinate = cell_m.coordinate
        if cell_m_coordinate != 'M1':
            worksheet[cell_m_coordinate] = f"=AVERAGE(E{current_row}:K{current_row})"
            current_row += 1

workbook.save('FOR-PS-03.xlsx')
workbook.close()

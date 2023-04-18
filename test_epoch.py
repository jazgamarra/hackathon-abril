import time
import datetime

fecha_str = '2003-04-17'
hora_str = '14:19'

# Convertir fecha y hora a objetos datetime
fecha_hora_str = fecha_str + ' ' + hora_str
fecha_hora = datetime.datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')

# Calcular epoch
epoch = int(time.mktime(fecha_hora.timetuple()))

print(epoch)



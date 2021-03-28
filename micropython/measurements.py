from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
from m5mqtt import M5mqtt
import ntptime
import json
import time
import unit
from secret import WIFI

setScreenColor(0x111111)
env20 = unit.get(unit.ENV2, unit.PORTA)


data = None

# write your wifi name and password in secret.py
wifiCfg.doConnect(WIFI["ap"], WIFI["pw"])
title0 = M5Title(title="Last measurement", x=3, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
label0 = M5TextBox(7, 216, "Status:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(0, 38, "Temp:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
status = M5TextBox(57, 217, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(7, 62, "Hum:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label3 = M5TextBox(7, 84, "Pres:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
temp = M5TextBox(53, 38, "0.0", lcd.FONT_Default, 0xFFFFFF, rotate=0)
hum = M5TextBox(53, 62, "0.0", lcd.FONT_Default, 0xFFFFFF, rotate=0)
pres = M5TextBox(53, 84, "0.0", lcd.FONT_Default, 0xFFFFFF, rotate=0)




status.setText('MQcnct?')
m5mqtt = M5mqtt('au676174', 'itwot.cs.au.dk', 1883, '', '', 300)
m5mqtt.set_last_will(str('au676174/M5SC0/status'),str('disconnected'))
m5mqtt.start()
status.setText('MQCnctd')
m5mqtt.publish(str('au676174/M5SC0/status'),str('connected'))
while True:
  temp.setText(str(env20.temperature))
  hum.setText(str(env20.humidity))
  pres.setText(str(env20.pressure))
  ntp = ntptime.client(host='cn.pool.ntp.org', timezone=2)
  data = {'temp':(env20.temperature),'hum':(env20.humidity),'pres':(env20.pressure),'time':(ntp.formatDatetime('-', ':'))}
  m5mqtt.publish(str('au676174/M5SC0/measurements/json'),str((json.dumps(data))))
  wait(60)
  wait_ms(2)
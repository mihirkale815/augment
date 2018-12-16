import sys
sys.path.append("../../")
import augment.data
from augment.data.instance import Instance

lines = """# text: Cambiar alarma de 7am a 7pm por favor 
# intent: alarm/modify_alarm 
# slots: 18:21:datetime,22:23:alarm/alarm_modifier,24:27:datetime 
1	cambiar	alarm/modify_alarm	NoLabel 
2	alarma	alarm/modify_alarm	NoLabel 
3	de	alarm/modify_alarm	NoLabel 
4	7am	alarm/modify_alarm	B-datetime 
5	a	alarm/modify_alarm	B-alarm/alarm_modifier 
6	7pm	alarm/modify_alarm	B-datetime 
7	por	alarm/modify_alarm	NoLabel 
8	favor	alarm/modify_alarm	NoLabel"""


lines2 = """# text: Recuérdame de escribirle un correo electrónico a mi jefe
# intent: reminder/set_reminder
# slots: 14:56:reminder/todo
1	recuérdame	reminder/set_reminder	NoLabel
2	de	reminder/set_reminder	NoLabel
3	escribirle	reminder/set_reminder	B-reminder/todo
4	un	reminder/set_reminder	I-reminder/todo
5	correo	reminder/set_reminder	I-reminder/todo
6	electrónico	reminder/set_reminder	I-reminder/todo
7	a	reminder/set_reminder	I-reminder/todo
8	mi	reminder/set_reminder	I-reminder/todo
9	jefe	reminder/set_reminder	I-reminder/todo"""

instance = Instance.from_lines(lines.split("\n"))
'''print(instance.text)
print(instance.intent)
print(instance.slot_labels)
print(instance.slot_pos_labels)
print(instance.slot_type_labels)
print(instance.spans)
'''


lines_clone = instance.to_lines()
instance_clone = Instance.from_lines(lines_clone.split("\n"))

print(instance.slot_labels)
print(instance_clone.slot_labels)
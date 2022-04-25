import time
from pynput.keyboard import Key, Controller

keyboard = Controller()
delay_time = 3  # s

print(f'Программа вставляет код КУДА УГОДНО, поэтому у вас есть {delay_time} секунды, чтобы переключиться на нужное '
      f'поле ввода')
print("Введите код программы. Для завершения введите символ '~' с новой строки:")

contents = []
while True:
    try:
        line = input()
        if line == '~':
            break
    except EOFError:
        break
    contents.append(line)

for i in range(len(contents)):
    contents[i] = contents[i].strip('\t')

time.sleep(delay_time)

for i in range(len(contents)):
    for j in range(len(contents[i])):
        print(contents[i][j])
        if contents[i][j] == '.':
            keyboard.press('.')
            keyboard.release('.')
        else:
            keyboard.press(contents[i][j])
            keyboard.release(contents[i][j])
            time.sleep(0.095)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

import RPi.GPIO as GPIO
from sys import exit
from time import sleep, time
from matplotlib import pyplot


GPIO.setmode(GPIO.BCM)

DAC=[26, 19, 13, 6, 5, 11, 9, 10]
LEDS=[21, 20, 16, 12, 7, 8, 25, 24]

GPIO.setup(DAC, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(LEDS, GPIO.OUT)

COMP=4
TROYKA=17

GPIO.setup(TROYKA,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(COMP, GPIO.IN)

def dec2bin(var, l=len(DAC)):
    result = []
    for i in range(l):
        result.append(0)
    for i in range(l-1,-1,-1):
        if var == 0:
            break
        result[i] = var%2
        var //= 2
    return result

def adc():
    k = 0
    for i in range(7,-1,-1):
        k += 2**i
        GPIO.output(DAC, dec2bin(k))
        sleep(0.05)
        if GPIO.input(COMP) == 0:
            k -= 2**i
    return k

try:
    k = 0
    result = []
    start = time()
    count = 0

    print('начало зарядки конденсатора')
    while k<256*0.25:
        k = adc()
        result.append(k)
        sleep(0)
        count += 1
        GPIO.output(LEDS,dec2bin(k))

    GPIO.setup(troyka,GPIO.OUT, initial=GPIO.LOW)

    print('начало разрядки конденсатора')
    while k>256*0.02:
        k = adc()
        result.append(k)
        sleep(0)
        count += 1
        GPIO.output(LEDS,dec2bin(k))

    finish = time() - start

    print('запись данных в файл')
    
    with open('data.txt', 'w') as f:
        for i in result:
            f.write(str(i) + '\n')

    with open('settings.txt', 'w') as f:
        f.write(str(1/finish/count) + '\n')
        f.write('0.01289')
    
    print('общая продолжительность эксперимента {}, период одного измерения {}, средняя частота дискретизации {}, шаг квантования АЦП {}'.format(finish, finish/count, 1/finish/count, 0.013))

    print('построение графиков')
    
    y = [ i/256*3.3 for i in result ]
    x = [ i*finish/count for i in range(len(result)) ]

    pyplot.plot(x, y)
    pyplot.xlabel('время')
    pyplot.ylabel('вольтаж')
    pyplot.show()

except KeyboardInterrupt:
    print('done')
finally:
    print('finally')
    GPIO.output(DAC, 0)
    GPIO.cleanup() 
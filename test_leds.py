result = 0
# We should go down from max 
for i in range(7, -1, -1):
    result += 2**i
    GPIO.output(dac, bin(result))
    if GPIO.input(comp) == 0:
        result -= 2**i
#We need that for seing how leds work
    sleep(0.01)
print(result)
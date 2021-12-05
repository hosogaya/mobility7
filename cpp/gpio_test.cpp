#include <wiringPi.h>

int main() {
    wiringPiSetupGpio() ;
    pinMode (0, PWM_OUTPUT) ;
    pwmSetMode(PWM_MODE_MS) ;
    pwmSetClock(40) ;
    pwmSetRange(256) ;
    
    pwmWrite(0 , 256) ;
    
    return 0 ;
}
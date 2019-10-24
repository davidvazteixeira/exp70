#include <SimpleDHT.h>

#define PIN1 49
#define VCC1 51
#define GND1 53

#define PIN2 33
#define VCC2 35
#define GND2 37

SimpleDHT11 ht;

void setup() {
  Serial.begin(115200);

  pinMode(GND1, OUTPUT);
  pinMode(GND2, OUTPUT);
  digitalWrite(GND1, LOW);
  digitalWrite(GND2, LOW);
  
  pinMode(VCC1, OUTPUT);
  pinMode(VCC2, OUTPUT);
  digitalWrite(VCC1, HIGH);
  digitalWrite(VCC2, HIGH);
}

byte tReturn, hReturn;
byte getData(int pin){
  byte t = 0;
  byte h = 0;

  int n=0;
  
  for(int i=0; i < 10; i++){
    n++;
    ht.read(pin, &t, &h, NULL);
    if(t==0 && h==0){
      delay(1000);
    } else {
      break;
    }
  }

  tReturn = t;
  hReturn = h;
}

void serialEvent(){
  while(Serial.available()) Serial.read();

  digitalWrite(13, HIGH);
  if(c == 'c') sendData();
  delay(500);
  digitalWrite(13, LOW);
}

void sendData(){
  byte t1, h1, t2, h2;   
    getData(PIN1);
    t1 = tReturn;
    h1 = hReturn;
    
    getData(PIN2);
    t2 = tReturn;
    h2 = hReturn;
  
    Serial.print(t1);Serial.print(' ');
    Serial.print(h1);Serial.print(' ');
    Serial.print(t2);Serial.print(' ');
    Serial.print(h2);Serial.println();
}


void loop() {
  //sendData();
}

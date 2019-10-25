#define RELAY 5

void setup() {
  Serial.begin(115200);
  pinMode(RELAY, OUTPUT);
}

void serialEvent(){
  char c = Serial.read();
  digitalWrite(13, HIGH);
  if(c == 'c') {
    digitalWrite(RELAY, !digitalRead(RELAY));
  }
  delay(500);
  digitalWrite(13, LOW);
  while(Serial.available()) Serial.read();
}

void loop() {

}

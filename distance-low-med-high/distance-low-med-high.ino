// defines pins numbers
const int vcc = 4;
const int trigPin = 5;
const int echoPin = 6;
const int gnd = 7;

void setup() {
  pinMode(vcc, OUTPUT);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(gnd, OUTPUT);

  digitalWrite(vcc, HIGH);
  digitalWrite(gnd, LOW);

  Serial.begin(57600); // Starts the serial communication

}

void serialEvent(){
  digitalWrite(13, HIGH);
  switch(Serial.read()){
  case 'c':
    int distance = sample();
    Serial.println(distance);
    break;
  }
  digitalWrite(13, LOW);
}

int sample(){
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);

  // Calculating the distance
  int distance= duration*0.034/2;

  // Prints the distance on the Serial Monitor
  return distance;
}

void loop() {
  //long distance = sample();
  //Serial.println(distance); 
  //delay(100);
}

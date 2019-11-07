// defines pins numbers
const int vcc = 4;
const int trigPin = 5;
const int echoPin = 6;
const int gnd = 7;

void setup() {
  pinMode(vcc, OUTPUT);     // Use pin as a Vcc to avoid jumpers
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT);  // Sets the echoPin as an Input
  pinMode(gnd, OUTPUT);     // Use pias as GND do avoid jumpers

  digitalWrite(vcc, HIGH);  // simulated Vcc pin ON
  digitalWrite(gnd, LOW);   // simulated GND pin OFF

  Serial.begin(57600);      // Starts the serial communication
}

void serialEvent(){
  digitalWrite(13, HIGH);
  switch(Serial.read()){
  case 'c':
    Serial.println(sample_distance());
    break;
  case 'r':
    Serial.println(sample_duration_raw());
    break;
  }
  digitalWrite(13, LOW);
}

int sample_distance(){
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH)/2;

  // Calculating the distance
  int distance = duration*0.034;

  // Prints the distance on the Serial Monitor
  return distance;
}

int sample_duration_raw(){
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  int duration = pulseIn(echoPin, HIGH)/2;

  // Prints the distance on the Serial Monitor
  return duration;
}

void loop() {
  //long distance = sample();
  //Serial.println(distance); 
  //delay(100);
}

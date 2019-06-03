int value;
int tmp_sensor = A1;
int ledPin = 13;

float voltage;
float temperatureC;

void setup(){
    Serial.begin(9600);
    pinMode(tmp_sensor,INPUT);
    pinMode(ledPin, OUTPUT);
}
void loop() {
    value = analogRead(tmp_sensor);
    voltage = value * 5.0 / 1024.0;
    temperatureC  = (voltage - 0.5) / 0.01;
    if(temperatureC >40){
        digitalWrite(ledPin,HIGH);
    }else{
        digitalWrite(ledPin,LOW);
    }
    Serial.println(temperatureC);
    delay(500);
}

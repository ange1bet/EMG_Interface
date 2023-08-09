// C++ code
//
  int sensorPin = A1;
  int y= 0;
  float alpha = 0.05;
  int s = y;

void setup()
{
Serial.begin(2400);
}

void loop()
{
y = (float)analogRead(sensorPin);
s = (alpha*y)+((1-alpha)*s);
  Serial.print(y);
  Serial.print(",");
  Serial.println(s);
}
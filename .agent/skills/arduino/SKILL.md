---
name: Arduino
description: C++, sensors, actuators, serial communication
---

# Arduino Skill

## Basic Structure

```cpp
void setup() {
  // Runs once at startup
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Runs repeatedly
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```

## Digital I/O

```cpp
// Output
pinMode(13, OUTPUT);
digitalWrite(13, HIGH);

// Input
pinMode(7, INPUT);
int value = digitalRead(7);

// Input with pullup
pinMode(7, INPUT_PULLUP);
```

## Analog I/O

```cpp
// Read (0-1023)
int sensorValue = analogRead(A0);

// Write PWM (0-255)
analogWrite(9, 128);  // 50% duty cycle
```

## Serial Communication

```cpp
Serial.begin(9600);
Serial.println("Hello");
Serial.print(value);

if (Serial.available() > 0) {
  char c = Serial.read();
}
```

## Common Sensors

| Sensor | Function |
|--------|----------|
| DHT11/22 | Temperature, humidity |
| HC-SR04 | Ultrasonic distance |
| LDR | Light level |
| PIR | Motion detection |
| MPU6050 | Accelerometer/gyro |

## When to Apply
Use when building Arduino projects or interfacing with sensors/actuators.

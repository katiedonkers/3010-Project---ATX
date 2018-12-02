/*

*/
//UNUSED

const int blueTrig = 13;
const int blueEcho = 4;

const int greenTrig = 1;
const int greenEcho = 0;

void setup() {
  
  pinMode(blueTrig, OUTPUT);        //set pin type
  pinMode(blueEcho, INPUT);
  
  pinMode(greenTrig, OUTPUT);
  pinMode(greenEcho, INPUT);
  
  Serial.begin(9600);
}

void loop() {
    
   int count = 0;                         //next part calculates distance between both straps 
   int distance[100];
   int duration; 
   while(count<100){                      //calculates 100 times for presision 
     //Serial.println(count);
     digitalWrite(greenTrig, HIGH);
     digitalWrite(blueTrig, HIGH);
     delayMicroseconds(10); 
     digitalWrite(greenTrig, LOW);
     digitalWrite(blueTrig, LOW);
     
     duration = pulseIn(blueEcho, HIGH);
     distance[count] = (duration * 0.034);
     count++; 
     delay(20); 
   }
    int averageDistance;
  for(int i =0; i<100; i++){                //traverces the 100 measurments to calculate average 
    averageDistance += distance[i];
  }
    
    averageDistance = averageDistance/100; //calculates average 
    
    Serial.println(averageDistance);
}

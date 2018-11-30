// Stepper - Version: 1.1.3
#include <Stepper.h>

/*

*/

int startStop; //to start the measuring process

//const long strapLength = 150; //temp length 
long lengthBlue;              //calculated length 
long lengthGreen;             // calculated length 
const long distanceStep = 5; //temp length


//motor set up
const int stepsPerRevolution = 200;   //step size
Stepper myBlueStepper(stepsPerRevolution, 5, 7, 6, 8); //middle pins inversed to allow movement in either direction
Stepper myGreenStepper(stepsPerRevolution, 9, 11, 10, 12); 
int stepTakenGreen = 0;               //number of steps taken
int stepTakenBlue = 0;

//Button Pins
const int buttonGreen = 3;          //setting pins to parts
const int buttonBlue = 2; 

//Ultrasonic sensor Pinss
const int blueTrig = 13;
const int blueEcho = 4;

const int greenTrig = 1;
const int greenEcho = 0;


void setup() {
  startStop = 0; 
  
  pinMode(blueTrig, OUTPUT);        //set pin type
  pinMode(blueEcho, INPUT);
  
  pinMode(greenTrig, OUTPUT);
  pinMode(greenEcho, INPUT);
  
  pinMode(buttonGreen, INPUT);
  pinMode(buttonBlue, INPUT); 
  
  myBlueStepper.setSpeed(60);     //set motor speed 
  myGreenStepper.setSpeed(60);
  
  digitalWrite(buttonGreen,LOW);  //initialize button pins to low 
  digitalWrite(buttonBlue,LOW);
  
  Serial.begin(9600);
}

void loop() {
  
  if(Serial.read() == 49){             //waiting on the pi so start process
    startStop = 1;            //start pi
  }
  
 if(startStop == 1) {         //only starts when pi says to 
  
  while(digitalRead(buttonBlue)!=HIGH {   //run stepper motors till tightened
    
                    //run blue stepper
    myBlueStepper.step(-stepsPerRevolution);
    stepTakenBlue++;
    delay(250);
    }
        
   while( digitalRead(buttonGreen)!=HIGH) {               //run green stepper 
    myGreenStepper.step(-stepsPerRevolution);
    stepTakenGreen++;
    delay(250);
    }
    
    
  
  lengthCalc();                           //calculates length of both circomference 

  Serial.println(lengthBlue);             //sends info back to pi that is waiting
  Serial.println(lengthGreen);
 
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
    int averageDistance=0;
  for(int i =0; i<100; i++){                //traverces the 100 measurments to calculate average 
    averageDistance += distance[i];
  }
    
    averageDistance = averageDistance/100; //calculates average 
    
    Serial.println(averageDistance);        //sends average distance back to pi
    
    startStop = 0;                        //ensures it doesnt rerun the loopp until told to 
    
    //unwind 
    while(stepTakenGreen != 0 ){
      
        myGreenStepper.step(stepsPerRevolution);
        stepTakenGreen--;
        delay(20);
      }
    while ( stepTakenBlue != 0){
        myBlueStepper.step(stepsPerRevolution);
        stepTakenBlue--;
        delay(20);
    }

 }  
}

void lengthCalc(){
  // lengthBlue = strapLength - (stepTakenBlue*distanceStep);  //calculates the circumfrance of the arm using the length of stap - the number of steps times the distance pre step
   //lengthGreen = strapLength - (stepTakenGreen*distanceStep);
  lengthBlue = stepTakenBlue;
  lengthGreen = stepTakenGreen;
}









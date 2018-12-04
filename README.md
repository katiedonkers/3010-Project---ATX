# 3010-Project---ATX
computer systems development project


//README
The following provides instruction for proper operation of ATX: The Automated
Tailor Experience. The first section includes steps for launching the application
and running all software in the correct order. The second section includes steps for
using the physical components of the system.

SECTION 1 (Software):
1. Launch the ATX application from Android Studio.
2. Run the Raspberry Pi 2 containing the database.
3. Run the headless Raspberry Pi controller (ensure it is connected to Arduion Uno via USB first)
4. Proceed to SECTION 2 to adjust physical components before returning to the next step.
5. Now that the physical straps are in place, and all components of the system are running, begin by
entering your 10 letter username into the homepage of the Android Application.
6. If your username already exists, your previous measurements will be displayed to you on another page.
7. If your username does not exist, the Application will create an entry in the database for you, and display
your username and measurements (all initialized to zero) to you on another page.
8. To begin take your measurements, click the button 'START MEASURING'.
9. The straps will tighten one at a time to take your circumference measurements, and the sensor will
measure the distance of your forearm. The straps will automatically unwind once they've completed their execution.
10. Once this process is complete, you will see your updated measurements appear on the Android Application, as well
as being added to the database.


SECTION 2 (Physical Components):
1. Turn palm of hand upward and place arm straps securely around wrist and just below the upper elbow.
2. Ensure that ultrasonic sensors are facing each other, it is best to lay arm on a flat surface.
3. Practise pressing down on the platform to ensure the STOP button beneath the surface is working - you
should hear a 'click' as this button presses against your arm. 
4. This button will be pressed automatically as the straps tighten to take your measurements, but if you
prefer to stop the winding sooner simply press the button.
5. Return to SECTION 1 

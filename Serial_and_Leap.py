import Leap, sys, thread, time, serial
from Leap import CircleGesture, SwipeGesture, ScreenTapGesture, KeyTapGesture




#=====================================

#  Function Definitions

#=====================================

ratio1 = 0.0
ratio2 = 0.0
ratio3 = 0.0
ratio4 = 0.0
ratio5 = 0.0
ratio6 = 0.0
		#testData = []
data = "<LED2," + str(ratio1) + "," + str(ratio2) + "," + str(ratio3) + "," + str(ratio4) + "," + str(ratio5) + "," + str(ratio6) + ">"

def sendToArduino(sendStr):
  ser.write(sendStr)


#======================================

def recvFromArduino():
  global startMarker, endMarker
  
  ck = ""
  x = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  while  ord(x) != startMarker: 
    x = ser.read()
  
  # save data until the end marker is found
  while ord(x) != endMarker:
    if ord(x) != startMarker:
      ck = ck + x 
      byteCount += 1
    x = ser.read()
  
  return(ck)


#============================

def waitForArduino():

   # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded
   
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:

      while ser.inWaiting() == 0:
        pass
        
      msg = recvFromArduino()

      print msg
      print
      
#======================================

def runTest(td):
  numLoops = len(td)
  waitingForReply = False

  n = 0
  while n < numLoops:

    teststr = td[n]

    if waitingForReply == False:
      sendToArduino(teststr)
      #print "Sent from PC -- LOOP NUM " + str(n) + " TEST STR " + teststr
      waitingForReply = True

    if waitingForReply == True:

      while ser.inWaiting() == 0:
        pass
        
      dataRecvd = recvFromArduino()
      #print "Reply Received  " + dataRecvd
      n += 1
      waitingForReply = False

      #print "==========="

    time.sleep(0.01)
print
print

# NOTE the user must ensure that the serial port and baudrate are correct
#baudRate = 9600
ser = serial.Serial('COM6', 115200, timeout=1)
#print "Serial port " + serPort + " opened  Baudrate " + str(baudRate)


startMarker = 60
endMarker = 62


waitForArduino()
#=============================

#Leap Motion

#=============================


class LeapMotionListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	joint_names = ['MCP', 'PIP', 'DIP', 'TIP']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	#Methods
	

	def on_init(self, controller):	
		print "Initialized"

	def on_connect(self, controller):
		print "Motion Sensor Connected!"

		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print "Motion Sensor Disconnected!"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		frame = controller.frame()
		
		global ratio1, ratio2, ratio3, ratio4, ratio5, ratio6, data

		for hand in frame.hands:

			
			for finger in hand.fingers:
				

				if(finger.type==1): #index finger
					#print "Type: " + self.finger_names[finger.type] + " ID: " + str(finger.id) + " Length(mm): " + str(finger.length) + " Width(mm): " + str(finger.width)
			
					testData = []

					MCP_position = finger.joint_position(0)
					PIP_position = finger.joint_position(1)	
					DIP_position = finger.joint_position(2)	
					MCP_y = MCP_position[1]
					#MCP_x = MCP_position[0]
					#index_x = MCP_x
					PIP_y = PIP_position[1]	
					DIP_y = DIP_position[1]
					distance = round(PIP_y - DIP_y)
					height = round(MCP_y - PIP_y)

					#print "distance1: " + str(distance)
					#print "distance2: " + str(height)
					print "MCP: " + str(MCP_y)
					print "PIP: " + str(PIP_y)
					print "DIP: " + str(DIP_y)
					if((distance >= 4) and (height<=30)):		#DIP lower than PIP thus finger is flexed
						ratio1 = round((((distance-4)*2.75)/100), 2)
						ratio6 = 0

					elif((distance >= 4) and (height>=31)):
						if(height<=36):
							ratio1 = round((((height-31)/5)*0.45 + 0.55), 2)
							ratio6 = 0

						else:
							ratio1 = 1
							ratio6 = 0
					else:
						ratio1 = 0
						ratio6 = 0
			
					data = "<LED2," + str(ratio1) + "," + str(ratio2) + "," + str(ratio3) + "," + str(ratio4) + "," + str(ratio5) + "," + str(ratio6) + ">"
					testData.append(data)
					runTest(testData)


				elif(finger.type==2):  #middle finger
					testData = []

					MCP_position = finger.joint_position(0)
					PIP_position = finger.joint_position(1)	
					DIP_position = finger.joint_position(2)	
					MCP_y = MCP_position[1]
					PIP_y = PIP_position[1]	
					DIP_y = DIP_position[1]
					distance = round(PIP_y - DIP_y)
					height = round(MCP_y - PIP_y)

					if((distance >= 5) and (height<=30)):		#DIP lower than PIP thus finger is flexed
						ratio2 = round((((distance-5)*2.4)/100), 2)
						#print "distance: " + str(distance)
						#print "height: " + str(height)
						#print "ratio2: " + str(ratio2)
					elif((distance >= 5) and (height>=31)):
						if(height<=40):
							ratio2 = round((((height-31)/9)*0.55 + 0.45), 2)
						#	print "distance: " + str(distance)
						#	print "height: " + str(height)
						#	print "ratio2: " + str(ratio2)
						else:
							ratio2 = 1
						#	print "distance: " + str(distance)
						#	print "height: " + str(height)
						#	print "ratio2: " + str(ratio2)
					else:
						ratio2 = 0
					data = "<LED2," + str(ratio1) + "," + str(ratio2) + "," + str(ratio3) + "," + str(ratio4) + "," + str(ratio5) + "," + str(ratio6) + ">"
					testData.append(data)
					runTest(testData)


				elif(finger.type==3):  #ring and pinky
					testData = []

					MCP_position = finger.joint_position(0)
					PIP_position = finger.joint_position(1)	
					DIP_position = finger.joint_position(2)	
					MCP_y = MCP_position[1]
					PIP_y = PIP_position[1]	
					DIP_y = DIP_position[1]
					distance = round(PIP_y - DIP_y)
					height = round(MCP_y - PIP_y)

					if((distance >= 5) and (height<=26)):		#DIP lower than PIP thus finger is flexed
						ratio3 = round((((distance-5)*3)/100), 2)
	
					elif((distance >= 5) and (height>=27)):
						if(height<=36):
							ratio3 = round((((height-27)/9)*0.45 + 0.55), 2)
							#print "distance: " + str(distance)
							#print "height: " + str(height)
							#print "ratio3: " + str(ratio3)
						else:
							ratio3 = 1
							#print "distance: " + str(distance)
							#print "height: " + str(height)
							#print "ratio3: " + str(ratio3)
					else:
						ratio3 = 0
						#print "distance: " + str(distance)
						#print "height: " + str(height)
						#print "ratio3: " + str(ratio3)
					data = "<LED2," + str(ratio1) + "," + str(ratio2) + "," + str(ratio3) + "," + str(ratio4) + "," + str(ratio5) + "," + str(ratio6) + ">"
					#time.sleep(0.5)
					testData.append(data)
					runTest(testData)

				elif(finger.type==0):    #thumb
					testData = []
					
					#for b in range(0, 2):
					#	bone = finger.bone(b)
					#	print "Bone: " + self.bone_names[bone.type] + "Start: " + str(bone.prev_joint) + "End: " + str(bone.next_joint)
					MCP_position = finger.joint_position(0)
					TIP_position = finger.joint_position(3)

					MCP_z = MCP_position[2]	
					TIP_z = TIP_position[2]

					MCP_x = MCP_position[0]	
					TIP_x = TIP_position[0]
					
					distance_z = round(MCP_z - TIP_z)
					distance_x = round(MCP_x - TIP_x)
					#print "TIP: " + str(TIP_z)
					#print "MCP: " + str(MCP_z)
					#print "distance: " + str(distance_z)
					if(distance_z<=40):
						ratio4 = 1					#thumb base
					elif(distance_z>=80):
						ratio4 = 0
					
					elif(distance_x>=70):
						ratio5 = 0					#thumb
						#print str(ratio5)

					elif(distance_x<=30):
						ratio5 = 1

						#print str(ratio5)
					else:
						ratio4 = round((1-((distance_z-40)/40)),2)
						ratio5 = round(1-((distance_x -30)/40), 2)
						#print str(ratio5)


					data = "<LED2," + str(ratio1) + "," + str(ratio2) + "," + str(ratio3) + "," + str(ratio4) + "," + str(ratio5) + "," + str(ratio6) + ">"
					testData.append(data)
					runTest(testData)
					#print "ratio4: " + str(ratio4)
				else:
					pass
				#time.sleep(0.2)
				#print(data)


def main():
	#ratio1 = 0.0
	#ratio2 = 0.0
	#ratio3 = 0.0
		#testData = []
	#data = "<LED2," + str(ratio1) + "," + str(ratio2) + "," + str(ratio3) + ">"

	listener = LeapMotionListener()
	controller = Leap.Controller()

	controller.add_listener(listener)

	print "Press enter to quit"
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(listener)


if __name__ == "__main__":
	main()
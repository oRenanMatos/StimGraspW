<h1>STIMGRASP and WT901BLECL50 Control </h1>

This repository contains Python code to control the STIMGRASP stimulator and read data from the WT901BLECL50 inertial measurement unit (IMU) using serial communication. The code is designed to run on a system with the necessary hardware connections to the STIMGRASP and the WT901BLECL50 IMU.

<h2>Dependencies</h2>
Python 3.x
Required Python packages: numpy, serial
Install the dependencies using:

<pre>
  pip install numpy pyserial
</pre>


<h2>Hardware Setup</h2>
Connect the STIMGRASP stimulator and the WT901BLECL50 IMU to the specified serial ports (stimgrasp_port and port variables in the code). Adjust the baud rates accordingly.

<h2>Usage</h2>

Configure STIMGRASP parameters using the provided examples in the script. Modify the values of current_CH0, frequency, and pulse_width as needed.

Trigger STIMGRASP actions such as configuration, starting, stopping, or shutting down by setting the corresponding flags (setStimGrasp, startStimGrasp, stopStimGrasp, shutdownStimGrasp) to True.

Update stimulation parameters or amplitude using the respective flags (updateStimGrasp, updateSetStimGrasp) and provide new values.

<h2>Example</h2>

<pre>

# Example Configuration and Stimulation

# Initialize STIMGRASP
current_CH0 = 10
frequency = 20
pulse_width = 200
setStimGrasp = True

# Start stimulation
startStimGrasp = True
time.sleep(10)

# Update current to 20 mA
current_CH0 = 20
updateStimGrasp = True
time.sleep(10)

# Update pulse width to 400 us
pulse_width = 400
updateSetStimGrasp = True
time.sleep(20)

# Stop stimulation
stopStimGrasp = True
time.sleep(10)

# Shutdown STIMGRASP
shutdownStimGrasp = True

# Close serial connection
input("Press Enter to exit.")
ser.close()

  
</pre>


Notes
Adjust the serial port names and baud rates in the script according to your system setup.
The script provides basic error checking for parameter values.
Ensure that the required hardware is properly connected before running the script.
Feel free to contribute and improve the code as needed!

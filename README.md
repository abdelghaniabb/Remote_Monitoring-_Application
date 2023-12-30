# Remote Lab Monitoring

### Video Demo: [link YouTube video](https://youtu.be/fO25eBljkxs)
### Description

The Remote Lab Monitoring system is a web-based application designed for temperature monitoring and control within a laboratory environment. Implemented on a Raspberry Pi, this system provides real-time access and interaction with lab components, focusing on features such as temperature measurement and light control.

- User authentication ensures secure access to the lab monitoring system. While the registration option is available for testing purposes, in a production environment, user credentials will be provided to authorized individuals, minimizing unauthorized access, after all, we don’t want for anyone to have access to control and monitor our lab. However, Registered users have the option to change their passwords, with the requirement that passwords must be at least 4 characters long, containing at least one digit and one special character.


- Features
    - **Light Control:** The Light Control feature allows users to manipulate the lab's lighting by turning bulbs on and off. Implemented using switch toggles, user requests are sent to the server via the POST method, triggering Python code execution on the Raspberry Pi. The system utilizes GPIO pins to set bulb states, and a GET request retrieves the current bulb status when loading the page. 

    - **Lab Temperature:** Lab Temperature provides real-time data on the current temperature and humidity within the lab. This information is gathered using a DHT11 sensor, and measurements are stored in an SQL table for future reference.
    
    - **Live:** The Live View feature offers users a real-time stream of the lab environment.

    - **History:** The History page enables users to navigate through historical lab temperature and humidity values based on the date of measurement.**


#### Setting up the Raspberry Pi

To set up the Raspberry Pi, follow these steps:
1. [Installing Raspberry Pi OS](https://www.raspberrypi.com/software/)

2. Update the Raspberry Pi and set the date
    ~~~bash
    sudo apt update
    sudo apt upgradde
    sudo date -s "11 Dec 2023 11:00:00"
    ~~~

3. Cabling the necessary circuits

    - Connect Bulbs to control over the web
        Bulbs|Raspberry Pi pin|Relay state
        :---:|:---:|:---:
        bulb1 |physical 15 (GPIO pin 22)|NC (Normally open)
        bulb2 |physical 16 (GPIO pin 23)|NC (Normally open)
        bulb3 |physical 22 (GPIO pin 25)|NO (Normally open)

    - Read the DHT11 sensor for the temperature of the room 

        DHT11 pin|Raspberry Pi pin
        :---:|:---:
        (+) pin|5V pin
        (-) pin|GND
        OUT pin |physical pin 40 (GPIO pin 21)


## CQR-UC: A Color QR Code-based Underwater Wireless Communication Method using Deep Image Enhancement

This is the repo for "CQR-UC: A Color QR Code-based Underwater Wireless Communication Method using Deep Image Enhancement"[[arXiv]](URL not available yet).

### Introduction
This project aims to implement data communication through color QR codes between two devices, specifically designed for underwater environments. Using a TCP-like continuous transmission method, it ensures reliable data transmission with an efficiency of up to 100 bits per second.

### Features
Transmit data by displaying color QR codes on the screen of one device.
Capture and decode QR codes displayed on the screen of the other device using a camera.
A reliable transmission protocol ensures data integrity.
Compatible with both Windows and Linux platforms.


### Installation and Running
1. Clone the Repository
bash
复制代码
    ~~~
    git clone https://github.com/your-repository.git  

    cd CQR_UC 
    ~~~

2. Install Dependencies
Ensure Python and pip are installed, then run the following command:

    ~~~
    pip install -r requirements.txt  
    ~~~

3. download WeChat QRCode 
Please download the resources from https://github.com/WeChatCV/opencv_3rdparty.git and place them into the "qr_mode" directory of each version.
For example:
~~~
├─v0
│  ├─receiver
│  │  ├─.history
│  │  ├─assets
│  │  ├─logs
│  │  ├─qr_mode (put into here)
~~~


3. Configure and Run
#### Configuration File
Before running the code, modify the config.json file according to your device setup, including camera device index and screen resolution.

#### Start the Code
Run the following commands on two separate devices:
test v0 for example:
~~~
cd v0
~~~

~~~
# For the sender
bash run_sender.sh
~~~
~~~
# For the receiver
bash run_receiver.sh
~~~
We have only created a simple human-computer interaction interface for testing our project. If you need a different interface, you can create your own using PyQt5 or utilize the methods in the CQRCode library, which has already been developed in this project, to build your own experimental code.

For the human-computer interaction interface in this project, you just need to enter the text or data you wish to transmit into the input window on the sender side. If no information is entered, random data will be used for the transmission test.

For detailed parameter information, please refer to the code.


### File Structure
~~~
├─v0
│  ├─receiver
│  │  ├─.history
│  │  ├─assets
│  │  ├─logs
│  │  ├─qr_mode
│  │  └─__pycache__
│  └─sender
│      ├─.history
│      ├─assets
│      ├─qr_mode
│      └─__pycache__
├─v1
│  ├─receiver
│  │  ├─.vscode
│  │  ├─assets
│  │  ├─logs
│  │  ├─qr_mode
│  │  └─__pycache__
│  └─sender
│      ├─.vscode
│      ├─assets
│      ├─qr_mode
│      ├─weights
│      └─__pycache__
└─v2
    ├─receiver
    │  ├─.history
    │  │  └─logs
    │  ├─assets
    │  ├─logs
    │  ├─qr_mode
    │  └─__pycache__
    └─sender
        ├─.history
        ├─assets
        ├─qr_mode
        └─__pycache__
~~~



### Future Plans
Enhance adaptability for underwater environments.
Increase transmission speed and resistance to interference.
Support more data formats for transmission.
You can customize and expand this further depending on your project's specifics!


### Citation(Not Completed)
If you use this code in your research, please consider citing the following paper:


 

### Acknowledgment(Not Completed)

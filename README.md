# LanChat

Python script/program intended for communicating with the systems in a LAN/WLAN connection.
It uses socket programming python to connect to each instance.

## LanChat.py
* This is the intial CLI version of the project and is pretty neat for all its worth.
* On startup, the user is asked for an ip. The user could also press enter and make the instance run as the central node.
![Initial prompt](/screencaps/screencapscli_01.png)
* The host/master is the central node and is necassary for all connections hence.
![Host/Master node](/screencaps/screencapscli_02.png)
![Host/Master node](/screencaps/screencapscli_03.png)
* Clients/Slaves are peer nodes and are limitted by the computing capacity of the master computer.<br>A list of 1000 peer nodes can still be easily connected.
![Client/Slave node](/screencaps/screencapscli_04.png)
* Clients can easily disconnect by sending a blank text and their disconnection will be shown in chat. Host instance should however wait until all other devices are disconnected or it could result in an error.
![Disconnection](/screencaps/screencapscli_05.png)

## LanChat.pyw
* the CLI version still needs some debugging. Although it could be used pretty well either way as of now.
* On startup, the user is prompted for an ip. The user could also press enter and make the instance run as the central node.
![Initial prompt](/screencaps/screencapsgui_01.png)
* Like the GUI version, the host/master is the central node and is necassary for all connections hence.
![Host/Master node](/screencaps/screencapsgui_02.png)
![Host/Master node](/screencaps/screencapsgui_03.png)
* Clients/Slaves are peer nodes and are limitted by the computing capacity of the master computer.<br>A list of 1000 peer nodes can still be easily connected.
![Client/Slave node](/screencaps/screencapsgui_04.png)
![Client/Slave node](/screencaps/screencapsgui_05.png)
![Client/Slave node](/screencaps/screencapsgui_06.png)
![Client/Slave node](/screencaps/screencapsgui_07.png)
* Clients can easily disconnect by sending a blank text and their disconnection will be shown in chat. Host instance should however wait until all other devices are disconnected or it could result in an error.
![Disconnection](/screencaps/screencapsgui_08.png)

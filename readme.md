# transmission-narodmon
Send Download/Upload speed statistic to narodmon.ru

### Required:
* Python 3
* requests lib
* socket lib

### Config file description:
* **_mac_addr_** - MAC adress of your transmission jail;
* **transmission_host** - path to your Transmission's RPC host;
* **rpc_login** - Transmission RPC username
* **rpc_pwd** - Transmission RPC password

### How to run:
Set run.sh to crontab every 5 (or less) minutes execution

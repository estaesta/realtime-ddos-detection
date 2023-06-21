# Python CICFlowMeter

> This project is cloned from [Python Wrapper CICflowmeter](https://gitlab.com/hieulw/cicflowmeter) and customized to fit my need. Therefore, it is not maintained actively. If there are any problems, please create an issue or a pull request.  


### Installation
* webserver
```sh
git clone https://github.com/estaesta/realtime-ddos-detection
cd realtime-ddos-detection
python3 setup.py install
```
* ml server
```sh
git clone https://github.com/estaesta/realtime-ddos-detection
```

### Usage
* webserver
```sh
usage: sudo python3 detector.py ml_endpoint
```
* ml server
```sh
cd realtime-ddos-detection
flask -A webapp.py run
```

- Reference: https://www.unb.ca/cic/research/applications.html#CICFlowMeter

# Cisco SD-WAN Qos Maps Viewer

QoS Maps viewer allows you to search by Qos map name and return the devices affected by the Qos map. You can also search by Localized Policy name and return the Qos maps used in the policy.

# Requirements

To use this code you will need:

- Python 3.7+
- vManage user login details.

# Install and Setup

- Clone the code to local machine.

```
git clone https://github.com/HusseinOmar/sd-wan-qos-map-viewer.git
cd sd-wan-qos-map-viewer
```

- Setup Python Virtual Environment (requires Python 3.7+)

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# Collecting Data

```
python data-collector.py
```

# Viewing and Searching Data

```
python data-viewer.py
```

Follow prompts to do multiple searches

# Video Demo

[![Watch the Demo Video](https://img.youtube.com/vi/pMjse6xL09Y/0.jpg)](https://www.youtube.com/watch?v=pMjse6xL09Y)

# License

[CISCO SAMPLE CODE LICENSE - Link](https://developer.cisco.com/docs/licenses)

[Cisco Sample Code License - Local File](LICENSE)

# Questions and Contact Info

If you have any issues or a pull request, you can submit a Issue or contact me directly。

My Cisco CEC ID is: husseino

My email address husseino@cisco.com

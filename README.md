# ha-custom_components
Some custom components for HA (Home Assistant).

# Gazpar
Gazpar custom component is using PyGazpar library to retrieve GrDF data.

## Installation steps of gazpar are :

1. Copy the gazpar directory in HA config/custom_components directory.

2. Update your HA configuration with :

```yaml
sensor:
- platform: gazpar
    username: ***
    password: ***
    pce_identifier: ***
    tmpdir: /config/tmp
    scan_interval: 01:00:00
```

Ensure that tmpdir already exists before starting HA.

5. Restart your HA application. In HA development panel, you should see the new Gazpar entities with their corresponding attributes:
- sensor.gazpar_daily_energy:
```yaml
attribution: Data provided by GrDF
username: stephane.senart@gmail.com
time_period: 19/04/2021
start_index_m3: 13708
end_index_m3: 13713
volume_m3: 4.7
energy_kwh: 52
converter_factor_kwh/m3: 11.268
temperature_degC: 12
type: MES
timestamp: 2021-04-21T07:50:09.505625
unit_of_measurement: kWh
friendly_name: Gazpar daily energy
icon: mdi:fire
```

- sensor.gazpar_weekly_energy:
```yaml
attribution: Data provided by GrDF
username: stephane.senart@gmail.com
current: 
  time_period: Du 19/04/2021 au 19/04/2021
  volume_m3: 4.7
  energy_kwh: 52
  timestamp: '2021-04-21T07:54:06.324645'

previous: 
  time_period: Du 12/04/2021 au 18/04/2021
  volume_m3: 57.1
  energy_kwh: 643
  timestamp: '2021-04-21T07:54:06.324645'

unit_of_measurement: kWh
friendly_name: Gazpar weekly energy
icon: mdi:fire
```

- sensor.gazpar_monthly_energy:
```yaml
attribution: Data provided by GrDF
username: stephane.senart@gmail.com
current: 
  time_period: Avril 2021
  volume_m3: 135.4
  energy_kwh: 1525
  timestamp: '2021-04-21T07:58:01.392893'

previous: 
  time_period: Mars 2021
  volume_m3: 261.1
  energy_kwh: 2937
  timestamp: '2021-04-21T07:58:01.392893'

unit_of_measurement: kWh
friendly_name: Gazpar monthly energy
icon: mdi:fire
```

6. If you want to keep entities from previous version, use the following template:
```yaml
- platform: template
  sensors:
    gazpar_last_period_start_time:
      friendly_name: "Gazpar last period start time"    
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'time_period') }}"
      icon_template: mdi:fire
    gazpar_last_period_end_time:
      friendly_name: "Gazpar last period end time"    
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'time_period') }}"
      icon_template: mdi:fire
    gazpar_last_start_index:
      friendly_name: "Gazpar last start index"
      unit_of_measurement: 'm³'      
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'start_index_m3') | float }}"
      icon_template: mdi:fire      
    gazpar_last_end_index:
      friendly_name: "Gazpar last end index"
      unit_of_measurement: 'm³'      
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'end_index_m3') | float }}"
      icon_template: mdi:fire      
    gazpar_last_volume:
      friendly_name: "Gazpar last volume"
      unit_of_measurement: 'm³'      
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'volume_m3') | float }}"
      icon_template: mdi:fire      
    gazpar_last_energy:
      friendly_name: "Gazpar last energy"
      unit_of_measurement: 'kWh'      
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'energy_kwh') | float }}"  
      icon_template: mdi:fire
    gazpar_last_converter_factor:
      friendly_name: "Gazpar last converter factor"
      unit_of_measurement: 'kWh/m³'      
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'converter_factor_kwh/m3') | float }}"
      icon_template: mdi:fire
    gazpar_last_temperature:
      friendly_name: "Gazpar last temperature"
      unit_of_measurement: '°C'      
      value_template: "{{ state_attr('sensor.gazpar_daily_energy', 'temperature_degC') | float }}"
      icon_template: mdi:fire      
```

## Data history import into HA database

The command line to import the daily data history into HA is :

```bash
$ python -m gazpar -u 'your login' -p 'your password' -w 'path/to/Selenium Web Driver' -s 30 -t 'temporary directory where to store XSLX file (ex: /tmp)' -f DAILY -l 0 import --connectionType Sql --connectionString 'ha_db_url'
```

Replace DAILY by WEEKLY or MONTHLY depending on the readings you want.

HA database connection string format is:
- Sqlite : sqlite:///path_to/ha_filename.db
- Mariadb : mariadb+mariadbconnector://user:password@ip:3306/ha_database_name?charset=utf8mb4

## Troubleshooting

1. If the Gazpar entities does not show up few minutes after restart, something goes wrong.
To troubleshoot what is wrong, you can activate Gazpar logging by adding the following in HA configuration :

```yaml
logger:
  default: warning
  logs:
    custom_components.gazpar: debug
    pygazpar: debug
```

2. If the problem seems to come from PyGazpar library integration, please refer to https://github.com/ssenart/PyGazpar and try to make the pygazpar command line work first and get your data. The pygazpar command line must work in the same runtime HA is running in (same host, same docker container or same VM...).

# Veoliaidf
TODO

# Netatmo
TODO

# Note about using geckodriver in a Docker container

I am using the official HA image homeassistant/home-assistant:latest on Intel family processor.
HA image is based on Alpine Linux distribution. The corresponding Alpine Hardware Architecture for me is x86_64 (see wiki.alpinelinux.org/wiki/Architecture).
I'm using the geckodriver built for this architecture exactly :
- See the geckodriver releases by architecture here : https://github.com/mozilla/geckodriver/releases.
- For HassIO users, refer the next note in this document.

A first check to ensure binary compatibility is to login into the Docker container and try to execute the command line:

```bash
/config/drivers/geckodriver --version
```

You should see something like :

```bash
geckodriver 0.27.0 (7b8c4f32cdde 2020-07-28 18:16 +0000)

The source code of this program is available from
testing/geckodriver in https://hg.mozilla.org/mozilla-central.

This program is subject to the terms of the Mozilla Public License 2.0.
You can obtain a copy of the license at https://mozilla.org/MPL/2.0/.
```

If you don't, two possible reasons :
1. Execution permission of the file is wrongly set. Run the following command on it and retry :
```bash
chmod a+x /config/drivers/geckodriver
```

2. Binary format of the file is not compatible. Double check what kind of binary your need depending on your processor architecture.

After geckodriver version has been found and validated, you have to install a compatible Firefox version in your Docker container. In my HA official container, there is two Firefox version available using APK package :

```bash
apk list | grep firefox
```

```bash
firefox-esr-78.6.1-r0 x86_64 {firefox-esr} (GPL-3.0-only AND LGPL-2.1-only AND LGPL-3.0-only AND MPL-2.0)
firefox-84.0.2-r0 x86_64 {firefox} (GPL-3.0-only AND LGPL-2.1-only AND LGPL-3.0-only AND MPL-2.0) [installed]
```

I tried both, but only firefox-84.0.2-r0 is working fine. The command line to install it is :

```bash
apk install firefox
```

Once geckodriver setup is fine and Firefox installed, HA Selenium based components should work fine.

# Note about using geckodriver in HassIO/RaspberryPi distribution

Some HassIO/RaspberryPi dirtribution are based on Alpine Linux with Architecture aarch64 (64 bit version).

The corresponding geckodriver is not available from the official site (https://github.com/mozilla/geckodriver/releases) and I had to recompile a dedicated version available here (from source code available here : https://hg.mozilla.org/mozilla-central/file and instructions here : https://firefox-source-docs.mozilla.org/testing/geckodriver/Building.html): 


https://github.com/ssenart/ha-custom_components/blob/master/drivers/geckodriver-0.29.0-0-aarch64.tgz


This version is compatible with firefox-84.x.
But, it is not compatible with firefox-esr-78.x.

You can install the corresponding firefox package with the command :

```bash
apk add firefox
```

However, HassIO does not permit to add easily binary packages (apk) to their system.

As a workaround, I invite you to patch the component code as following :

```diff
diff --git a/gazpar/sensor.py b/gazpar/sensor.py
index 4154c175e205f4cec02e65e002287507387d4e90..cb679d3e522acd72586e6cb63825bddb9d64a5c7 100644
--- a/gazpar/sensor.py
+++ b/gazpar/sensor.py
@@ -15,6 +15,7 @@ from homeassistant.const import (
 import homeassistant.helpers.config_validation as cv
 from homeassistant.helpers.entity import Entity
 from homeassistant.helpers.event import track_time_interval, call_later
+import os
 
 _LOGGER = logging.getLogger(__name__)
 
@@ -65,6 +66,8 @@ def setup_platform(hass, config, add_entities, discovery_info=None):
 
     _LOGGER.debug("Initializing Gazpar platform...")
 
+    os.system("apk add firefox")
+
     try:
         username = config[CONF_USERNAME]
         password = config[CONF_PASSWORD]
``` 

I know it is dirty and I don't have other cleaner solution yet.

Let me know if you have other ideas.
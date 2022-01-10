# ha-custom_components
Some custom components for HA (Home Assistant).

# Gazpar
Move GrDF Gazpar integration [here](https://github.com/ssenart/home-assistant-gazpar).

# Veoliaidf

Veoliaidf custom component is using PyVeoliaIDF library to retrieve Veolia data.
PyVeoliaIDF library relies on Selenium and geckodriver application (see https://github.com/ssenart/PyVeoliaIDF for details).

1. Copy the veoliaidf directory in HA config/custom_components directory.

2. Copy your Selenium geckodriver binary in HA config/drivers directory. Ensure it has the execution permission from the runtime environment HA is running on. Geckodriver releases are available here : https://github.com/mozilla/geckodriver/releases.

3. Install a compatible version Firefox on HA host. Ensure this version is in the PATH and HA can run it.

4. Update your HA configuration with :

```yaml
sensor:
- platform: veoliaidf
    username: ***
    password: ***
    webdriver: /config/drivers/geckodriver
    tmpdir: /tmp
    scan_interval: 01:00:00
```

5. Restart your HA application. In HA development panel, you should see the new Veolia entities :
- sensor.veolia_total_liter
- sensor.veolia_yesterday_liter
- sensor.veolia_period_start_time
- sensor.veolia_period_end_time

# Netatmo
Experimental fork that permits to stream camera while it is off.

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
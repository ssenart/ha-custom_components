# ha-custom_components
Some custom components for Home Assistant

gazpar and veoliaidf are using selenium with geckodriver to retrieve their data from the corresponding web site.

## Note about using geckodriver in HassIO/RaspberryPi distribution

Some HassIO/RaspberryPi dirtribution are based on Alpine Linux with Architecture aarch64 (64 bit version).

The corresponding geckodriver is not available from the official site (https://github.com/mozilla/geckodriver/releases) and I had to recompile a dedicated version available here (from source code available here : https://hg.mozilla.org/mozilla-central/file and instructions here : https://firefox-source-docs.mozilla.org/testing/geckodriver/Building.html): 

```
https://github.com/ssenart/ha-custom_components/blob/master/geckodriver-0.29.0-0-aarch64.tgz
```

This version is compatible with firefox-84.x.
But, it is not compatible with firefox-esr-78.x.

You can install the corresponding firefox package with the command :

```bash
# apk add firefox
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
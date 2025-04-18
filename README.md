# Electrolux Water Heater and more...

[![License][license-shield]][license]
[![ESPHome release][esphome-release-shield]][esphome-release]
[![Open in Visual Studio Code][open-in-vscode-shield]][open-in-vscode]
[![Community Forum][community-forum-shield]][community-forum]
[![Support author][donate-tinkoff-shield]][donate-tinkoff]
[![Support author][donate-boosty-shield]][donate-boosty]
[![PayPal.Me][donate-paypal-shield]][donate-paypal]

[license-shield]: https://img.shields.io/static/v1?label=License&message=MIT&color=orange&logo=license
[license]: https://opensource.org/licenses/MIT
[esphome-release-shield]: https://img.shields.io/static/v1?label=ESPHome&message=2024.12&color=green&logo=esphome
[esphome-release]: https://GitHub.com/esphome/esphome/releases/
[open-in-vscode-shield]: https://img.shields.io/static/v1?label=+&message=Open+in+VSCode&color=blue&logo=visualstudiocode
[open-in-vscode]: https://open.vscode.dev/dentra/esphome-components
[community-forum-shield]: https://img.shields.io/static/v1.svg?label=%20&message=Forum&style=popout&color=41bdf5&logo=HomeAssistant&logoColor=white
[community-forum]: https://community.home-assistant.io/t/electrolux-water-heater-integration/368498
[donate-tinkoff-shield]: https://img.shields.io/static/v1?label=Support+Author&message=Tinkoff&color=yellow
[donate-tinkoff]: https://www.tinkoff.ru/cf/3dZPaLYDBAI
[donate-boosty-shield]: https://img.shields.io/static/v1?label=Support+Author&message=Boosty&color=red
[donate-boosty]: https://boosty.to/dentra
[donate-paypal-shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal
[donate-paypal]: https://paypal.me/dentra0

This is a set of ESPHome components to control Rusklimat devices using UART protocol:

- Electrolux [Water Heater](#water-heater) (EWH)
- Ballu [Water Heater](#water-heater) (BWH)
- Zanussi [Water Heater](#water-heater) (ZWH)
- Electrolux [Humidifier](#humidifier) (EHU) (beta, help wanted with Ballu and Zanussi)
- Electrolux [Thermostat](#thermostat) (ETS) (experimental!)

Control is possible via custom dongle. You can make it yourself or buy a ready made.

> [!CAUTION]
>
> ## ⚠️ WARNING: Everything you do is done entirely at your own peril and risk!

## Water heater

For example you can try [Lilygo T-Dongle S3](https://github.com/Xinyuan-LilyGO/T-Dongle-S3), the easiest way is to do this is on Aliexpress.

| USB2 pin | USB2 color | USB2 signal name | ESP Connection | Lilygo T-Dongle S3 |
| -------- | ---------- | ---------------- | -------------- | ------------------ |
| 1        | Red        | VBUS             | 5V VIN         |
| 2        | White      | D- (DM)          | TX             | GPIO19             |
| 3        | Green      | D+ (DP)          | RX             | GPIO20             |
| 4        | Black      | GND              | GND            |

The communication UART protocol is 100% reversed for EWH and partially for BWH. It is fully described at [reverse.md](reverse.md) file.

Water heater components are build using `climate` platform and allows the following:

- Control current temperature
- Change target boil temperature
- Change boil power to 700W (EWH only, for BWH need help for reverse)
- Change boil power to 1300W
- Change boil power to 2000W
- Change BST (Bacteria Stop technology) mode (EWH only, for BWH need help for reverse)
- Sync and control internal clock (EWH only)
- Set and start internal timer (EWH only)
- Enter to "No Frost/Atifreeze" mode (EWH only)

### Help wanted

When the water is heated to the required temperature, the boiler can enter to an idle mode
(display shows 0 and temperature) but unfortunately I can't get this state yet. Obtaining
this state will allow to make energy calculation. If you know the command that can be sent
to the boiler to get this state or even grab internal boiler firmware binary - it will
be superior. Please let me know it.

## Humidifier

To control your Electrolux (Ballu and Zanussi also may work) humidifier you need [USB 3.0](https://en.wikipedia.org/wiki/USB_3.0) cable to success connection.
Connection with USB 2.0 may work or may not, depending on your device revision.

![USB 3.0](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/USB_3.0.png/640px-USB_3.0.png?download)

| USB3 pin | USB3 color | USB3 signal name | Connection           |
| -------- | ---------- | ---------------- | -------------------- |
| 1        | Red        | VBUS             | ESP 5V VIN           |
| 2        | White      | D- (DM)          | ESP TX               |
| 3        | Green      | D+ (DP)          | ESP RX               |
| 4        | Black      | GND              | ESP GND              |
| 5        | Blue       | SSRX-            | NC                   |
| 6        | Yellow     | SSRX+            | GND_DRAIN or ESP GND |
| 7        | -          | GND_DRAIN        | SSRX+ or ESP GND     |
| 8        | Purple     | SSTX-            | NC                   |
| 9        | Orange     | SSTX+            | NC                   |

> [!IMPORTANT]
>
> The important part of the connection that you need is to short SSRX+ and GND_DRAIN or simply try to short SSRX+ and GND.

Humidifier components allows the following:

- Control on/off
- Control fan speed
- Control target humidity
- Monitor current humidity
- Monitor current temperature
- Control presets
- Control warm mist
- Control UV
- Control ionizer
- Control lock
- Control mute
- Monitor empty water tank
- Monitor humidification
- Control LED mode, presets and brightness
- Adjust clock

> 100% worked with EHU-3810D, also should work with EHU-3815D.
> Please let me know your model to add support or number to description.

### Help wanted

Ballu and Zanussi humidifiers also may work. Please contact me or just leave feedback.

## Thermostat

The communication UART protocol is 100% know and implemented but connection part requires additional help and research.

## Build ESPHome firmware

You can download and use example configurations for:

- [EWH](ewh.yaml)
- [BWH](bwh.yaml)
- ZWH use EWH or BWH configuration
- [EHU](ehu.yaml)
- [ETS](ets.yaml)

You could use my video with [flashing instructions](https://t.me/esphome_tion/13868) from another project, but with your configuration.

## Experimental cloud support

Please see instructions [here](components/rka_cloud/README.md).

## Troubleshooting, new features and devices

Don't hesitate to open [issues](https://github.com/dentra/esphome-tion/issues) for bug reports and feature requests.

You can also use the [Telegram group](https://t.me/dentra_chat).

## Your thanks

If this project was useful to you, you can buy me a Cup of coffee via
[Card2Card][donate-tinkoff], [Boosty][donate-boosty] or [PayPal][donate-paypal]
and do not forget to star this project :)

## Commercial usage

For questions regarding commercial use or custom development/modification,
please contact me at [Telegram private messages](https://t.me/dtrachuk).

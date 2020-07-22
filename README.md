# IR Remote Controller with Raspberry Pi

## Install LIRC

```
sudo apt-get install lirc
```

## Setting

- Edit `/etc/modules` file and add:

```
lirc_dev
lirc_rpi gpio_in_pin=18 gpio_out_pin=27
```

- Edit `/boot/config.txt` file and add:

```
dtoverlay=lirc-rpi
dtparam=gpio_out_pin=27
dtparam=gpio_in_pin=18
dtparam=gpio_in_pull=up
```
- Change `/etc/lirc/hardware.conf` as:

```
# Run "lircd --driver=help" for a list of supported drivers.
DRIVER="default"
# usually /dev/lirc0 is the correct setting for systems using udev
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"
```

- Restart LIRC

```
sudo /etc/init.d/lircd stop
sudo /etc/init.d/lircd start
```

- Reboot raspberry pi

## Record IR Signal

### irrecord

Follow prompt and record only one button of remote controller with `irrecord`. The configure file will be created but the ir record will be not complete and not long enough for air conditioner. However, we still need the configure file just for a template.

```
irrecord -f -d /dev/lirc0 --disable-namespace <configure_file>
```

### mode2

Record complete ir signal with `mode2` for each status. 

- The air conditioner remote controller sends the whole information of the status when you press any button, for example: power on, 26 degree C, volume up...etc. 
- Evan you press the same button twice, the remote controller sends different information to the air condiioner.
- At least, record power on and off with the temperature you like.
- Steps:

1. Ececute
```
mode2 -d /dev/lirc0 > power_on
```
2. Push power button of the remote controller for turning on.
3. Ctrl + C
4. Ececute
```
mode2 -d /dev/lirc0 > power_ff
```
5. Push power button of the remote controller for turning off.
6. Ctrl + C


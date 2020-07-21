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
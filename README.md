# Netgear-munin
*Netgear wireless routers munin plugin*

## Usage
This plugin relies on [pynetgear](https://github.com/balloob/pynetgear):

```bash
pip3 install pynetgear
```

1. Clone this project on your server:
    
    ```bash
    git clone https://github.com/chteuchteu/Netgear-munin.git && cd Netgear-munin
    clone_path=$(pwd)
    ```

2. Install the plugins

    ```bash
    ln -s "$clone_path"/main.py /etc/munin/plugins/netgear-devices
    ln -s "$clone_path"/main.py /etc/munin/plugins/netgear-devices-signal-strength
    ln -s "$clone_path"/main.py /etc/munin/plugins/netgear-devices-link-rate
    
    service munin-node restart
    ```

3. Test it

    ```bash
    munin-run netgear-devices
    ```

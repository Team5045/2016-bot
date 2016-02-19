# Deploy instructions

## RoboRIO
Deploy as per standard RobotPy `pyfrc` procedure.

From `./py` directory,

```
python3 robot.py deploy --skip-tests
```

## Jetson
First copy the source code to the Jetson TK1.

From `./jetson` directory,

```
rsync -au . ubuntu@tegra-ubuntu.local:~/jetson --force
```

If you wish to manually run the jetson code, ssh into the jetson then run the server there.

```
ssh ubuntu@tegra-ubuntu.local
ubuntu@tegra-ubuntu.local's password: ubuntu

python /home/ubuntu/jetson/server.py PORT
```

Be sure to first copy necessary packages onto the jetson. While connected to the internet,

```
cd ~/jetson
pip install -r requirements.txt
```

If not connected to the internet, from root `2016-bot` directory:

```
mkdir transfer-me && cd transfer-me
pip install --download . -r ./jetson/requirements.txt
rsync -au . ubuntu@tegra-ubuntu.local:~/transfer-me --force
ssh ubuntu@tegra-ubuntu.local
pip install --no-index --find-links ~/transfer-me -r ~/jetson/requirements.txt
```

To run the server automatically on boot ([source](https://www.debian-administration.org/article/28/Making_scripts_run_at_boot_time_with_Debian)), create a file `jetson` in `/etc/init.d` on the TK1 with the contents of `./jetson-launcher` of this git repository. Then, on the Jetson, run:

```
update-rc.d jetson defaults
```

Poof, you're done!

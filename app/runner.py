#!/usr/bin/python

import base64
import boto3
import os
import subprocess
import sys
import threading
import time

from camlib.file_encryptor import FileEncryptor
from camlib.file_monitor import FileMonitor


def main():
    config = {"gpg_home": "/host/run/dbus/crypto",
              "drop_dir": "/data/",
              "s3_bucket": os.getenv("S3_BUCKET"),
              "img_ext": ".jpg",
              "vid_ext": ".avi",
              "recipients": os.getenv("RECIPIENTS").split(";"),
              "gpg_pubkeys": base64.b64decode(os.getenv("GPG_PUBKEYS"))}
    img_shipper = threading.Thread(target=image_shipper,
                                   args=[config],
                                   name="image_shipper")
    img_shipper.daemon = True
    img_shipper.start()
    vid_shipper = threading.Thread(target=video_shipper,
                                   args=[config],
                                   name="video_shipper")
    vid_shipper.daemon = True
    vid_shipper.start()
    if os.getenv("USE_PI_CAMERA") is not None:
        modprober1 = subprocess.Popen(["modprobe", "bcm2835-v4l2"])
        modprober2 = subprocess.Popen(["modprobe", "v4l2_common"])
    motion_process = subprocess.Popen("/usr/bin/motion")
    motion_pid = motion_process.pid

    print("PID for motion is %s" % motion_pid)
    while True:
        print "Motion detector running."
        if len(threading.enumerate()) < 3:
            print("Not running all threads, stopping...")
            sys.exit(1)
        if not motion_is_running(motion_pid):
            print("Motion is not running! KILL KILL KILL")
            sys.exit(2)
        time.sleep(60)


def motion_is_running(motion_pid):
    result = False
    try:
        os.kill(motion_pid, 0)
        result = True
    except OSError:
        pass
    return result


def image_shipper(config):
    s3 = boto3.resource('s3')
    bucket = config["s3_bucket"]
    mon = FileMonitor(config["drop_dir"], config["img_ext"])
    encryptor = FileEncryptor(config["gpg_home"],
                              config["gpg_pubkeys"],
                              config["recipients"])
    while True:
        one_file = mon.get_one_file()
        if one_file:
            print("Detected file: %s" % one_file)
            enc_file = encryptor.encrypt(one_file)
            if enc_file:
                with open(enc_file, "rb") as e_file:
                    print("Attempt to ship %s" % enc_file)
                    s3.Bucket(bucket).put_object(Key=enc_file, Body=e_file)
                os.remove(enc_file)
        else:
            time.sleep(5)  # Sleep 5s if no files to upload


def video_shipper(config):
    s3 = boto3.resource('s3')
    bucket = config["s3_bucket"]
    mon = FileMonitor(config["drop_dir"], config["vid_ext"])
    encryptor = FileEncryptor(config["gpg_home"],
                              config["gpg_pubkeys"],
                              config["recipients"])
    while True:
        one_file = mon.get_one_file()
        if one_file:
            print("Detected file: %s" % one_file)
            enc_file = encryptor.encrypt(one_file)
            if enc_file:
                with open(enc_file, "rb") as e_file:
                    print("Attempt to ship %s" % enc_file)
                    s3.Bucket(bucket).put_object(Key=enc_file, Body=e_file)
                    print("Shipped: %s" % enc_file)
                os.remove(enc_file)
        else:
            time.sleep(5)  # Sleep 5s if no files to upload


if __name__ == "__main__":
    main()

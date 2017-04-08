!#/usr/bin/python
from collections import deque
import threading
from camlib.camera import MotionDetector
import boto3


def main():
    global outbound_image_queue
    outbound_image_queue = deque([])
    cam_mon = threading.Thread(target=cam_monitor, name="camera_monitoy")
    cam_mon.daemon = True
    cam_mon.start()
    img_shipper = threading.Thread(target=img_shipper, name="image_shipper")
    img_shipper.daemon=True
    img_shipper.start()
    while True:
        print "Motion detector running."
        print "Health:\n\t %s" % str(threading.enumareate())

def cam_monitor():
    cam = MotionDetector()
    for image_path in cam:
        outbound_image_queue.append(image_path)


def img_shipper():
    s3 = boto3.resource('s3')
    bucket = os.getenv('S3_BUCKET')
    while True:
        if len(outbound_image_queue) == 0:
            time.sleep(1)
        else:
            ship_file = outbound_image_queue.pop()
            s3.meta.client.upload_file(ship_file, bucket, ship_file)

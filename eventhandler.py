import sys,time,logging,settings,os,random,string
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto
from boto.s3.key import Key


class S3UploadEventHandler(FileSystemEventHandler):
    def __init__(self, watchpath=None):
        self.watchpath = watchpath

    def on_moved(self, event):
        self.upload_file(event.dest_path)
        super(S3UploadEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        self.upload_file(event.src_path)
        super(S3UploadEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(S3UploadEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        self.upload_file(event.src_path)
        super(S3UploadEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)

    def get_s3_connection(self):
        return boto.connect_s3(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY) 

    def get_bucket(self, conn, bucket_name):
        return  self.get_s3_connection().get_bucket(settings.BUCKET_NAME) 

    def upload_file(self, path):
        try:
            conn = self.get_s3_connection()
            bucket = self.get_bucket(conn, settings.BUCKET_NAME)
            relative_path = path.replace(self.watchpath,'')
            k = Key(bucket)
            k.key = relative_path
            k.set_contents_from_filename(path)
            k.make_public()
        except:
            pass



This will watch a directory and all its sub directories, and upon creating, modifying, or moving a file underneath this structure it will upload the file to S3's CDN

This is intended to make cloud based hosting of a file as simple as an ftp drop

You will need to create a settings.py file containing the following:

AWS_ACCESS_KEY_ID = "youraccesskey"

AWS_SECRET_ACCESS_KEY = "yoursecretkey"

BUCKET_NAME = "bucketnameyouwishtouploadto"

USAGE:

python execute.py /path/to/directory/to/watch

It will wait for a keyboard interrupt, so you may want to daemonize the process

import paramiko
import sys
import time


def deploy(path, update):
    """
    Login to EC2 instance, clone the git repo for FindYourPath
    Update the mongo database if specified and launch the flask server
    :param path: path of the pemfile
    :param update: value provided as argument when script from shell
        (value 'update' willl update the mongo database)
    :return: None
    """
    PATH = "/home/ec2-user/findyourpath/code/"

    print("Connecting to box")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('ec2-54-245-157-1.us-west-2.compute.amazonaws.com',
                username='ec2-user', key_filename=path)
    print("Connected to server")

    print("cloning git")
    stdin, stdout, stderr = ssh.exec_command(
        "rm -rf findyourpath; \
        git clone git@github.com:MSDS698/findyourpath.git"
    )
    print('Logs when cloning: ', stderr.readlines())
    time.sleep(5)  # make sure the repo is cloned before moving on

    if(update):
        print("Storing data to MongoDB")
        stdin, stdout, stderr = ssh.exec_command(
            'python3 ' + PATH + 'upload_data_to_MongoDB.py')
        print('Logs when uploading to MongoDB: ', stderr.readlines())

    # kill previous flask server
    stdin, stdout, stderr = ssh.exec_command('pkill -9 python')
    print('Logs when terminating old flask server: ', stderr.readlines())

    print("Launch server")
    ssh.exec_command('python3 ' + PATH + 'flask_server.py')

    ssh.exec_command('logout')


if __name__ == '__main__':
    pem_file = sys.argv[1]
    update = False
    try:
        if(sys.argv[2] == 'update'):
            update = True  # indicate if the mongo database should be updated
    except BaseException:
        pass  # no argument given

    deploy(pem_file, update)

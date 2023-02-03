import boto3
import sys
import getopt

def create_bucket(argv):
    arg_bucket = ""
    arg_profile = ""
    arg_endpoint = ""
    arg_ssl = "y"
    arg_immutable = "y"
    arg_help = "{0} -b bucket <bucket> -p <profile> -e <endpoint> -s <ssl>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hb:p:e:s:i:", ["help", "bucket", "profile", 
        "endpoint", "ssl", "immutable"])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-b", "--bucket"):
            arg_bucket = arg
        elif opt in ("-p", "--profile"):
            arg_profile = arg
        elif opt in ("-e", "--endpoint"):
            arg_endpoint = arg
        elif opt in ("-s", "--ssl"):
            arg_ssl = arg
        elif opt in ("-i", "--immutable"):
            arg_immutable = arg

# Print the input variables - temp code to be removed    
    print('bucket:', arg_bucket)
    print('profile:', arg_profile)
    print('endpoint:', arg_endpoint)
    print('ssl:', arg_ssl)
    print('immutable:', arg_immutable)

# Connect to s3 endpoint using the profile from .aws/credentials file
    session = boto3.Session(profile_name=arg_profile)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    if arg_ssl == "y" or arg_ssl == "Y":
        secure_flag=True
    else:
        secure_flag=False

    if arg_immutable == "y" or arg_ssl == "Y":
        object_lock=True
    else:
        object_lock=False

    s3 = boto3.client('s3',
        endpoint_url=arg_endpoint,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        use_ssl=secure_flag,
        verify=False)

    bucket_name = arg_bucket

    s3.create_bucket(Bucket=bucket_name, ObjectLockEnabledForBucket=object_lock)

if __name__ == "__main__":
    create_bucket(sys.argv)

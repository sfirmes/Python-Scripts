import boto3
import sys
import getopt

# Parse the parameters entered and return the variable needed to create the bucket
def get_parms(argv):
    arg_bucket = ""
    arg_profile = ""
    arg_endpoint = ""
    arg_secured = ""
    arg_help = "{0} -b bucket <bucket> -p <profile> -e <endpoint> -s <security>".format(argv[0])
    
    try:
        opts, args = getopt.getopt(argv[1:], "hb:p:e:s:", ["help", "bucket=", "profile=", 
        "endpoint=", "secured="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
# print the help message
            print(arg_help)  
            sys.exit(2)
        elif opt in ("-b", "--bucket"):
            arg_bucket = arg
        elif opt in ("-p", "--profile"):
            arg_profile = arg
        elif opt in ("-e", "--endpoint"):
            arg_endpoint = arg
        elif opt in ("-s", "--security"):
            arg_secured = arg

    return [arg_bucket, arg_profile, arg_endpoint, arg_secured]

# Capture the parameters entered using the get_parms function
if __name__ == "__main__":
    arg_bucket, arg_profile, arg_endpoint, arg_secured = get_parms(sys.argv)

    
# Connect to s3 endpoint using the profile from .aws/credentials file
    print('bucket:', arg_bucket)
    print('profile:', arg_profile)
    print('endpoint:', arg_endpoint)
    print('secured:', arg_secured)

    session = boto3.Session(profile_name=arg_profile)
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    if arg_secured == "y" or arg_secured == "Y":
        secure_flag=True
    else:
        secure_flag=False

    s3 = boto3.client('s3',
        endpoint_url=arg_endpoint,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        use_ssl=secure_flag,
        verify=False)

    bucket_name = arg_bucket

    s3.create_bucket(Bucket=bucket_name, ObjectLockEnabledForBucket=True)
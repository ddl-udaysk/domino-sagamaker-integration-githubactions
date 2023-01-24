import boto3
import os
import time


client = boto3.client('sagemaker')

modelName = os.environ['MODELNAME']
instance_type = 'ml.t2.large'

try:

    create_model_api_response = client.create_model(
                                    ModelName=modelName,
                                    PrimaryContainer={
                                        'Image': '946429944765.dkr.ecr.us-west-2.amazonaws.com/bcs-sagemaker:'+ modelName,
                                        'ModelDataUrl': 's3://bcs-sagemaker-model-bucket/requirements_apps.tar.gz',
                                        'Environment': {}
                                    },
                                    ExecutionRoleArn='arn:aws:iam::946429944765:role/bcs-sagemaker-model-deploy'
                                    )
    print ("create_model API response", create_model_api_response)
except Exception:
    print("model already present")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    client.delete_model(ModelName=modelName)
    #client.delete_endpoint(EndpointName=modelName+  "endpoint" )
    #client.delete_endpoint_config(EndpointConfigName=modelName+  "endpoint-configuration")

    time.sleep(240)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    create_model_api_response = client.create_model(
                                    ModelName=modelName,
                                    PrimaryContainer={
                                    'Image': '946429944765.dkr.ecr.us-west-2.amazonaws.com/bcs-sagemaker:'+ modelName,
                                    'ModelDataUrl': 's3://bcs-sagemaker-model-bucket/requirements_apps.tar.gz',
                                    'Environment': {} 
                                    },
                                    ExecutionRoleArn='arn:aws:iam::946429944765:role/bcs-sagemaker-model-deploy'
                                    )


print ("create_model API response", create_model_api_response)

endpointconfiguration = modelName + "endpoint-configuration"
# create sagemaker endpoint config
try:

    create_endpoint_config_api_response = client.create_endpoint_config(
                                            EndpointConfigName=endpointconfiguration,
                                            ProductionVariants=[
                                                {
                                                    'VariantName': 'AllTraffic',
                                                    'ModelName': modelName,
                                                    'InitialInstanceCount': 1,
                                                    'InstanceType': instance_type
                                                },
                                            ]
                                       )

    print ("create_endpoint_config API response", create_endpoint_config_api_response)
    
except Exception:
    #client.delete_endpoint(EndpointName=modelName+  "endpoint" )
    client.delete_endpoint_config(EndpointConfigName=modelName+  "endpoint-configuration")
    
    time.sleep(120)
    create_endpoint_config_api_response = client.create_endpoint_config(
                                            EndpointConfigName=endpointconfiguration,
                                            ProductionVariants=[
                                                {
                                                    'VariantName': 'AllTraffic',
                                                    'ModelName': modelName,
                                                    'InitialInstanceCount': 1,
                                                    'InstanceType': instance_type
                                                },
                                            ]
                                       )


endpoint = modelName + "endpoint"
# create sagemaker endpoint

try:

    create_endpoint_api_response = client.create_endpoint(
                                    EndpointName=endpoint,
                                    EndpointConfigName=endpointconfiguration,
                                    )

    print ("create_endpoint API response", create_endpoint_api_response) 
except Exception:
    client.delete_endpoint(EndpointName=modelName+  "endpoint" )  
    time.sleep(60)
    create_endpoint_api_response = client.create_endpoint(
                                    EndpointName=endpoint,
                                    EndpointConfigName=endpointconfiguration,
                                    )         
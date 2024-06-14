from ..utils import input_or_output, get_asset_property
from dsioutilities import Dataset as alidaDataset
from datasets import Dataset
from datasets import load_from_disk
from s3fs import S3FileSystem


def load_from_minio(name):
    
    minio_url = get_asset_property(asset_name=name, property="minIO_URL")
    access_key = get_asset_property(asset_name=name, property="minIO_ACCESS_KEY")
    secret_key = get_asset_property(asset_name=name, property="minIO_SECRET_KEY")
    bucket_name = get_asset_property(asset_name=name, property="minio_bucket")

    use_ssl = get_asset_property(asset_name=name, property="use_ssl") if get_asset_property(asset_name=name, property="use_ssl") is not None else False
    use_ssl = True if use_ssl=="True" or use_ssl=="true" or use_ssl=="1" else False

    s3 = S3FileSystem(
        key=access_key, 
        secret=secret_key,
        client_kwargs={'endpoint_url': minio_url},
        use_ssl=use_ssl
    )
    
    return load_from_disk("s3://" + bucket_name + "/" + get_asset_property(name), storage_options=s3.storage_options)


def load(name)-> Dataset:
    if get_asset_property(asset_name=name, property="storage_type") is not None:
        storage_type = get_asset_property(asset_name=name, property="storage_type")
    else:
        storage_type= "filesystem"

    if storage_type == "minio":
        return load_from_minio(name)
    elif storage_type =="filesystem":
        return load_from_disk(get_asset_property(asset_name=name))


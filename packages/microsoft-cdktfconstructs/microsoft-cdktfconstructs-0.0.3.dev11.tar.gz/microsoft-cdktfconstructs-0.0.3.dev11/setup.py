import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "microsoft-cdktfconstructs",
    "version": "0.0.3.dev11",
    "description": "A collection of CDK modules for provisioning and managing Terraform resources efficiently.",
    "license": "MIT",
    "url": "https://github.com/azure/terraform-cdk-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Microsoft",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/azure/terraform-cdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "microsoft_cdktfconstructs",
        "microsoft_cdktfconstructs._jsii",
        "microsoft_cdktfconstructs.azure_applicationgateway",
        "microsoft_cdktfconstructs.azure_applicationinsights",
        "microsoft_cdktfconstructs.azure_containerregistry",
        "microsoft_cdktfconstructs.azure_eventhub",
        "microsoft_cdktfconstructs.azure_functionapp",
        "microsoft_cdktfconstructs.azure_keyvault",
        "microsoft_cdktfconstructs.azure_kubernetes",
        "microsoft_cdktfconstructs.azure_kusto",
        "microsoft_cdktfconstructs.azure_loganalytics",
        "microsoft_cdktfconstructs.azure_metricalert",
        "microsoft_cdktfconstructs.azure_networksecuritygroup",
        "microsoft_cdktfconstructs.azure_queryrulealert",
        "microsoft_cdktfconstructs.azure_resourcegroup",
        "microsoft_cdktfconstructs.azure_storageaccount",
        "microsoft_cdktfconstructs.azure_virtualmachine",
        "microsoft_cdktfconstructs.azure_virtualmachinescaleset",
        "microsoft_cdktfconstructs.azure_virtualnetwork",
        "microsoft_cdktfconstructs.core_azure"
    ],
    "package_data": {
        "microsoft_cdktfconstructs._jsii": [
            "terraform-cdk-constructs@0.0.3-pre.11.jsii.tgz"
        ],
        "microsoft_cdktfconstructs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf-cdktf-provider-azurerm==9.0.8",
        "cdktf==0.17.3",
        "constructs>=10.1.106, <11.0.0",
        "jsii>=1.98.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)

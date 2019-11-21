# Ref: https://cloud.google.com/compute/docs/tutorials/python-guide
import os
from googleapiclient import discovery
# from ..configuration import default_zone, default_project
# from ..instances.configs.preem1 import transient

transient = {
  "kind": "compute#instance",
  "name": "instance-1core-1gb-preem-1",
  "zone": "projects/gurjaspal-bedi/zones/us-east1-b",
  "machineType": "projects/gurjaspal-bedi/zones/us-east1-b/machineTypes/custom-1-1024",
  "displayDevice": {
    "enableDisplay": False
  },
  "metadata": {
    "kind": "compute#metadata",
    "items": []
  },
  "tags": {
    "items": []
  },
  "disks": [
    {
      "kind": "compute#attachedDisk",
      "type": "PERSISTENT",
      "boot": True,
      "mode": "READ_WRITE",
      "autoDelete": True,
      "deviceName": "instance-1core-1gb-preem-1",
      "initializeParams": {
        "sourceImage": "projects/debian-cloud/global/images/debian-9-stretch-v20191115",
        "diskType": "projects/gurjaspal-bedi/zones/us-east1-b/diskTypes/pd-standard",
        "diskSizeGb": "10"
      },
      "diskEncryptionKey": {}
    }
  ],
  "canIpForward": False,
  "networkInterfaces": [
    {
      "kind": "compute#networkInterface",
      "subnetwork": "projects/gurjaspal-bedi/regions/us-east1/subnetworks/default",
      "accessConfigs": [
        {
          "kind": "compute#accessConfig",
          "name": "External NAT",
          "type": "ONE_TO_ONE_NAT",
          "networkTier": "PREMIUM"
        }
      ],
      "aliasIpRanges": []
    }
  ],
  "description": "",
  "labels": {},
  "scheduling": {
    "preemptible": True,
    "onHostMaintenance": "TERMINATE",
    "automaticRestart": False,
    "nodeAffinities": []
  },
  "deletionProtection": False,
  "reservationAffinity": {
    "consumeReservationType": "ANY_RESERVATION"
  },
  "serviceAccounts": [
    {
      "email": "76984618152-compute@developer.gserviceaccount.com",
      "scopes": [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring.write",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/trace.append"
      ]
    }
  ]
}

def create_instance(compute, project, name, zone="us-east1-b"):
    config = transient

    return compute.instances().insert(project = project, zone = zone, body = config).execute()


if __name__ == "__main__":
  compute = discovery.build('compute', 'v1')
  project = "gurjaspal-bedi"
  name = "instance-1"
  create_instance(compute, project, name)

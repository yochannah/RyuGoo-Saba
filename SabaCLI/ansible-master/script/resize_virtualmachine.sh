#!/bin/bash

resource_group=$1
name=$2
gb_size=$3

function check_gb_size_virtualmachine() {
    resource_group=$1
    name=$2
    gb_size=$3

    JSON=$(az vm get-instance-view --resource-group $resource_group -n $name 2> /dev/null)
    if [ $? -gt 0 ]; then
        echo 0
        return 0
    fi

    current_gb_size=$(echo "$JSON" | jq .storageProfile.osDisk.diskSizeGb)

    if [ $current_gb_size -eq $gb_size ]; then
        echo 0
        return 0
    else
        echo 1
        return 1
    fi
}

function wait_azure_virtualmachine() {
    resource_group=$1
    name=$2
    except=$3

    case "$except" in
        "deallocated") ;;
        "starting") ;;
        "running") ;;
        *)
            return 1
        ;;
    esac

    while true
    do
        actual=$(az vm get-instance-view --resource-group $resource_group -n $name | jq -rc .instanceView.statuses[1].code)
        if [ "PowerState/$except" = "$actual" ]; then
            return 0;
        fi

        sleep 5
    done

    return 1;
}


if [ $(check_gb_size_virtualmachine $resource_group $name $gb_size) -eq 1 ]; then
    az vm deallocate --name $name --resource-group $resource_group
    wait_azure_virtualmachine $resource_group $name deallocated

    az disk update --resource-group $resource_group --name $name --size-gb $gb_size

    az vm start --name $name --resource-group $resource_group
    wait_azure_virtualmachine $resource_group $name running
fi

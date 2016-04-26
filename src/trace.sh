# Start vm if it's not yet started

VM=tvm
virsh list | grep -q "$VM" || virsh start "$VM"

if [[ $? != 0 ]]
then
    echo $VM not started
    exit 1
fi

sshu

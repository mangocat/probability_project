# 換mac address， 如果使用mac 和 wifi DHCP 可以在被 twse ban掉後重連
sudo /System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport --disassociate
sudo ifconfig en4 ether $(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/./0/2; s/.$//')
networksetup -detectnewhardware
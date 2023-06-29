# NETWORK CLI CONFIGURATION

The network configuration tool configures network devices using device configuration files in JSON format. The data provided in the configuration file is converted to a cli configuration string and this string is split into individual lines and sent to the network device over an SSH connection.

The configuration file can be divided into 4 parts.

1. Connection data.
    - device os.
    - devices ip address.
    - port number.
    - username.
    - password.
2. Global data.
    - data configured globally.
3. Interface data.
    - declares interfaces to be configured.
    - data to be configured at interface level.
4. Protocol data.
    - protocol global data.
    - protocol interface data.

# CONFIGURATION LAYOUT

    {
        "connection_data":{},
        "global":[],
        "interfaces":{},
        "port_security":{}
    }

# CONNECTION DATA

The connection data should contain the connection data required to connect to the given device.

    "connection_data":{
        "device":"cisco_switch",
        "device_type":"cisco_ios",
        "ip_address":"192.168.0.1",
        "port":"22",
        "username":"ciaran",
        "password":"admin",
        "secret":null
    },

# GLOBAL DATA

Global data is simply any lines that are configured at global level. This can be used for configuring commands that dont fall within a protocol such as a hostname.

    "global":[
        "vlan 2",
        "name group2",
        "exit",
        "vlan 3",
        "name group3",
        "exit",
        "vlan 4",
        "name group4",
        "exit"
    ],

# INTERFACES DATA

Any interface that is to be configured by any part of the configuration must be declared in interfaces. Each individual interface is declared under an interface name ie f0/1. In each interface the interface type and interface number must also be defined.

    "interfaces":{
        "f0/1":{
            "iface_id":"0/1",
            "iface_type":"fastEthernet",
            "lines":[
                "no shutdown"
            ]
        },
        "f0/2":{
            "iface_id":"0/2",
            "iface_type":"fastEthernet",
            "lines":[
                "no shutdown"
            ]
        },
    }

# PROTOCOL DATA

Protocol data is made up of global and interface level data. The global data is any lines that are configured at the global level. The interface data is any lines that are configured at the interface level. Each interface within a protocol configuration must have the same interface name as its interface declared in interfaces.

    "trunk":{
        "global":[],
        "interfaces":{
            "f0/13":[
                "switchport trunk allowed vlan 1,2"
            ],
            "f0/14":[
                "switchport trunk allowed vlan 1,2"
            ],
            "f0/15":[
                "switchport trunk allowed vlan 3,4"
            ],
            "f0/16":[
                "switchport trunk allowed vlan 3,4"
            ],
            "f0/17":[
                "switchport trunk allowed vlan 5,6"
            ],
            "f0/18":[
                "switchport trunk allowed vlan 5,6"
            ]
        }
    },

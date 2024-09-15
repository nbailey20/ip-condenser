# IP Condenser Script

Python script which takes a list of individual IP addresses and condenses them into a smaller group of subnets. The resulting subnets are guaranteed to contain all of the IPs in the provided list, however there may be additional IPs accounted for. Determination of whether 2 IPs can be condensed or whether 2 subnets can be further condensed is based on a utilization ratio.

Utilization ratio: the number of IPs from the input list actually present in a condensed subnet divided by the number of possible IPs in the subnet.

Example:
If the initial list of IPs is:
10.0.0.0
10.0.0.1
This can be condensed to 10.0.0.0/31, which has 2 possible IPs available. Since both of the IPs are present in the list, the calculated utilizattion is 2 present/2 possible = 100%

If the initial list is:
10.0.0.0
10.0.0.3
It's possible to condense this to 10.0.0.0/30. /30 subnets have 4 possible IPs, and since only 2 are in the list, the utilization is 50%.


As long as the calculated utilization ratio is above the MIN_UTILIZATION constant (set to 25% by default, can be changed to produce less or more resulting subnets based on need), the subnets can be condensed.

The script applies dynamic programming to determine the minimum number of resulting subnets that be produced given the MIN_UTILIZATION constraint, solving the problem in O(n^2) memory space and O(n^3) time complexity where n in the size of the input IP list.

## Requirements
* ipaddress.IPv4Network
* netaddr.spanning_cidr (can be installed with pip)
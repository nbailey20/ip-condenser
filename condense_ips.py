import ipaddress
from netaddr import spanning_cidr

UTILIZATION_RATIO = 25

## Helper class to keep track of min # of subnets possible in DP table
##   as well as the actual condensed subnets produced for the result
class Cell():
    def __init__(self, value=None, subnets=[]):
        self.value = value
        self.subnets = subnets


## Returns smallest CIDR range that contains both start and end IPs
def span(start, end):
    return spanning_cidr([start, end])


## Determines whether 2 subnets should be condensed based on utilization ratio
## E.g. 2 IPs used in a /30 is 50% utilization, 2 IPs used in a /29 is 25% utilization
def can_condense(start, end, num_ips):
    new_cidr = span(start, end)
    new_cidr_size = int(str(new_cidr).split("/")[1])

    possible_ips = 2 ** (32 - new_cidr_size)
    utilization = (num_ips / possible_ips) * 100
    if utilization >= UTILIZATION_RATIO:
        return True
    return False


## O(n^3) complexity to solve
def condense(ip_list):
    n = len(ip_list)

    ## Create empty dynamic-programming lookup table
    ## T[i][j] represents the minimum number of subnets that IPs i-j (inclusive) can be condensed to
    T = [[Cell() for i in ip_list] for j in ip_list]

    ## loop through table diagonally and fill in cells, answer will be contained in final cell T[0][n-1]
    for diff in range(n):
        for i in range(n-diff):

            ## first diagonal, min # of subnets for a single IP is 1
            if diff == 0:
                T[i][i].value = 1
                T[i][i].subnets = [ipaddress.IPv4Network(ip_list[i])]

            else:
                if can_condense(ip_list[i], ip_list[i+diff], diff+1):
                    T[i][i+diff].value = 1
                    T[i][i+diff].subnets = [ipaddress.IPv4Network(span(ip_list[i], ip_list[i+diff]))]
                ## if 2 single IPs can't be condensed, then we have 2 resulting subnets
                elif diff == 1:
                    T[i][i+diff].value = 2
                    T[i][i+diff].subnets = [ipaddress.IPv4Network(ip_list[i]), ipaddress.IPv4Network(ip_list[i+diff])]
                else:
                    min_val = 9999999
                    subnets = []
                    for l in range(i, i+diff):
                        val = T[i][l].value + T[l+1][i+diff].value
                        if val < min_val:
                            min_val = val
                            subnets = T[i][l].subnets + T[l+1][i+diff].subnets
                    T[i][i+diff].value = min_val
                    T[i][i+diff].subnets = subnets

    return [str(s) for s in T[0][n-1].subnets]




## Call function and pass in IP list
ip_list = [
    "10.0.0.0",
    "10.0.0.3",
    "10.0.0.5",
    "10.0.0.7",
    "10.0.0.8",
    "192.193.1.0",
    "192.193.1.2"
]
print(condense(ip_list))
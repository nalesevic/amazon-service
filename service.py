#  CLOUD SIMULATION COST
#
# Students:
#         Nizam Alesevic
#         Mehmed Tukulic
#

import numpy as np

# processing cost per 1ms in cents
PROCESSING_COST = 0.1
ONE_GB = 1073741824
ONE_MINUTE = 60000
THREE_MINUTE = 200000
TEN_MINUTE = 600000
FIFTEEN_MINUTE = 900000
THIRTY_MINUTE = 1800000
ONE_MONTH = 2592000000
yearly_cost = 0

for i in range(12):
    # month in miliseconds
    time = ONE_MONTH
    total_processing_time = 0
    processing_cost=0
    traffic_cost=0
    i_o_cost=0
    num_of_io=0
    volume_cost=10
    network_traffic = 0
    storage_device=0
    wan_traffic=0
    wan_cost=0
    total_cost = 0

    while(time > 0):
        #number of bytes
        num_bytes = 0
        # time between packets
        timeBetweenPackets = np.random.negative_binomial(n=TEN_MINUTE, p=0.5, size = 1)
        # calculate probability of packet
        packet_probability = np.random.random();

        # if it is packet for processing
        if(packet_probability < .7):
            # processing time up to 10 ms
            processing_time = np.random.uniform(low = 0, high = 10, size = 1)
            decimal = str(processing_time-int(processing_time))[3:][:1]
            decimal = int(decimal)

            if(decimal == 0):
                processing_time = int(processing_time)
                time -= (timeBetweenPackets + processing_time)
                total_processing_time+=processing_time
            else:
                processing_time = int(processing_time) + 1
                time -= (timeBetweenPackets + processing_time)
                total_processing_time+=processing_time

            # length of packet that leaves server
            wan_traffic += 100

        # if it is a packet for upload
        elif(packet_probability < .85):
            num_of_io+=1
            num_bytes = np.random.geometric(p=0.001, size = 1);
            if(num_bytes < 100):
                num_bytes += 100
            else:
                num_bytes = 1300

            # time for processing
            total_processing_time += 1
            time -= (timeBetweenPackets + 1)

            # send packet from server to storage device
            network_traffic+=num_bytes
            # increse storage device
            storage_device+=num_bytes
            if(time > 0):
                volume_cost += (10 * (storage_device / ONE_GB)  * ((ONE_MONTH - time) / ONE_MONTH))
        # if it is a packet for downlaod
        else:
            num_of_io+=1
            # send packet from server to storage device
            network_traffic += 100
            total_processing_time +=1
            time -= (timeBetweenPackets + 1)

            # reply from storage device
            num_bytes = np.random.poisson(lam=750, size = 1) + 100

            # storage device returns packet
            network_traffic+=num_bytes
            # packet leaves server
            wan_traffic+=num_bytes


    processing_cost = total_processing_time * PROCESSING_COST
    traffic_cost = network_traffic / ONE_GB
    i_o_cost = num_of_io / 100
    wan_cost = wan_traffic / ONE_GB
    total_cost = (processing_cost + traffic_cost + i_o_cost + volume_cost + wan_cost) / 100
    yearly_cost += total_cost

    print("Total cost for " + str(i + 1) + ". month = " + str(total_cost))

print("Yearly cost " + str(yearly_cost))

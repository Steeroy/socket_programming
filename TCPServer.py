#Siyanda Mvunyiswa
#4009043 - CSC311 Computer Networking Tut2
#TCP Server

import math
from heapq import heapify, heappush, heappop
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print('The server is ready to recieve')

#This seems alot but the basic idea is, we have dictionaries distances, route reports, times and weights
#so with each distionary, it will have depart and final destination
#The may be duplicates, so say 1. Bellville to 2. Nyanga and 2. Nyanga to bellville
#what we will assume is, the time, distance and route report it takes a trip from Bellville to Nyanga
#will be the same for a trip from Nyanga to Bellville, assuming the same route is taken


#this is the distances dictionary which reads like 1. Bellville to 3. SAPS-Int Airport is 10.1 km
distances = {
    '1':{'3': 10.1, '4': 2.7, '5': 17.3, '6': 12.4, '7': 5.7, '8': 27.5, '9': 23.9, '10': 7.7, '13': 8.5, '14': 23.1, '15': 22.9, '16': 9.4, '17': 22.4, '18': 5.1, '19': 8.3, '21': 22.7, '22': 12.5, '23': 17.4, '24': 21.1, '25': 14.6, '26': 4.9, '27': 13.5, '28': 27.8, '31': 9.4, '36': 21.1, '29': 13.1, '32': 12.8, '37': 34, '40': 33.1, '42': 38.5, '2': 13.8, '12': 27.4, '20': 7.6, '34': 24, '33': 24.8},
    '2': {'1': 13.8, '23': 11.6},'3': {'1': 10.1, '5': 11.1},'4': {'1': 2.7, '27': 12.6}, 
    '5': {'1': 17.3, '3': 11.1},'6': {'1': 12.4, '16': 25.4},'7': {'1': 5.7, '29': 11.6},
    '8': {'1': 27.5, '39': 22.6, '40': 8.2, '29': 14, '10': 28.2},'9': {'1': 23.9, '27': 13.4},
    '10': {'1': 7.7, '8': 28.2, '37': 43.6},'11': {'15': 19.6},'12': {'1': 27.4, '20': 24.2},
    '13': {'1': 8.5, '15': 19.9, '17': 11.9, '21': 19.7},'14': {'1': 23.1, '21': 2.7},'15': {'1': 22.9, '11': 19.6, '13': 19.9, '35': 34.4},
    '16': {'1': 9.4, '6': 25.4, '30': 20.6, '33': 12.8, '34': 12, '35': 6.1, '29': 11.5},
    '17': {'1': 22.4, '13': 11.9},'18': {'1': 5.1, '20': 4.1},'19': {'1': 8.3, '29': 10.4}, 
    '20': {'1': 7.6, '18': 4.1, '12': 24.2, '24': 18.3},'21': {'1': 22.7, '13': 19.7, '14': 2.7, '25': 8.8},
    '22': {'1': 12.5, '32': 7.8},'23': {'1': 17.4, '2': 11.6, '27': 9.4, '31': 32.4},
    '24': {'1': 21.1, '20': 18.3},'25': {'1': 14.6, '21': 8.8},'26': {'1': 4.9, '30': 20.5, '29': 11.1},
    '27': {'1': 13.5, '4': 12.6, '9': 13.4, '23': 9.4, '28': 8.5},'28': {'1': 27.8, '27': 8.5},
    '29': {'1': 13.1, '7': 11.6, '8': 14, '16': 11.5, '19': 10.4, '26': 11.1},'30': {'16': 20.6, '26': 20.5},
    '31': {'1': 9.4, '23': 32.4},'32': {'22': 7.8, '39': 28.4, '1': 12.8},'33': {'16': 12.8, '1': 24.8, '38': 20.9},
    '34': {'16': 12, '1': 24},'35': {'16': 6.1, '15': 34.4},'36': {'1': 21.1, '38': 10},
    '37': {'1': 34, '10': 43.6, '41': 5.2},'38': {'33': 20.9, '36': 10},'39': {'8': 22.6, '32': 28.4},
    '40': {'8': 8.2, '1': 33.1, '41': 5, '42': 7},'41': {'37': 5.2, '40': 5},'42': {'1': 38.5, '40': 7}
    }

#this is the route reports dictionary which reads like 1. Bellville to 3. SAPS-Int Airport has 0 reports
route_reports = {
    '1':{'3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 1, '9': 2, '10': 0, '13': 0, '14': 2, '15': 2, '16': 0, '17': 2, '18': 0, '19': 0, '21': 2, '22': 2, '23': 0, '24': 4, '25': 2, '26': 0, '27': 0, '28': 4, '31': 0, '36': 0, '29': 0, '32': 0, '37': 4, '40': 2, '42': 4, '2': 0, '12': 4, '20': 0, '34': 0, '33': 1},
    '2': {'1': 0, '23': 0},'3': {'1': 0, '5': 1},'4': {'1': 0, '27': 0},'5': {'1': 0, '3': 1},
    '6': {'1': 0, '16': 0},'7': {'1': 0, '29': 0},'8': {'1': 1, '39': 1, '40': 0, '29': 0, '10': 1},
    '9': {'1': 2, '27': 0},'10': {'1': 0, '8': 1, '37': 1},'11': {'15': 0},'12': {'1': 4, '20': 1},
    '13': {'1': 0, '15': 0, '17': 0, '21': 0},'14': {'1': 2, '21': 0},'15': {'1': 2, '11': 0, '13': 0, '35': 0},
    '16': {'1': 0, '6': 0, '30': 1, '33': 0, '34': 0, '35': 0, '29': 0},'17': {'1': 2, '13': 0},
    '18': {'1': 0, '20': 0},'19': {'1': 0, '29': 0},'20': {'1': 0, '18': 0, '12': 1, '24': 0},
    '21': {'1': 2, '13': 0, '14': 0, '25': 0},'22': {'1': 2, '32': 0},'23': {'1': 0, '2': 0, '27': 0, '31': 0},
    '24': {'1': 4, '20': 0},'25': {'1': 2, '21': 0},'26': {'1': 0, '30': 1, '29': 0},
    '27': {'1': 0, '4': 0, '9': 0, '23': 0, '28': 0},'28': {'1': 0, '27': 0},'29': {'1': 0, '7': 0, '8': 0, '16': 0, '19': 0, '26': 0},
    '30': {'16': 1, '26': 1},'31': {'1': 0, '23': 0},'32': {'22': 0, '39': 0, '1': 0},'33': {'16': 0, '1': 1, '38': 0},
    '34': {'16': 0, '1': 0},'35': {'16': 0, '15': 0},'36': {'1': 0, '38': 1},'37': {'1': 4, '10': 1, '41': 0},
    '38': {'33': 0, '36': 1},'39': {'8': 1, '32': 0},'40': {'8': 0, '1': 2, '41': 0, '42': 0},'41': {'37': 0, '40': 0},
    '42': {'1': 4, '40': 0}
    }

#this is the times dictionary which reads like 1. Bellville to 3. SAPS-Int Airport takes 14 minutes
times = {
    '1':{'3': 14, '4': 5, '5': 22, '6': 19, '7': 9, '8': 23, '9': 22, '10': 12,
         '13': 13, '14': 21, '15': 25, '16': 15, '17': 19, '18': 9, '19': 14, '21': 21,
         '22': 20, '23': 21, '24': 19, '25': 19, '26': 7, '27': 18, '28': 26, '31': 14,
         '36': 28, '29': 19, '32': 19, '37': 29, '40': 29, '42': 33, '2': 19, '12': 29,
         '20': 11, '34': 25, '33': 30},
    '2': {'1': 19, '23': 13},'3': {'1': 14, '5': 15},'4': {'1': 5, '27': 17}, 
    '5': {'1': 22, '3': 15},'6': {'1': 19, '16': 23},'7': {'1': 9, '29': 18},
    '8': {'1': 23, '39': 31, '40': 11, '29': 17, '10': 29},'9': {'1': 22, '27': 14},
    '10': {'1': 12, '8': 29, '37': 35},'11': {'15': 26},'12': {'1': 29, '20': 28},
    '13': {'1': 13, '15': 27, '17': 14, '21': 23},'14': {'1': 21, '21': 8},'15': {'1': 25, '11': 26, '13': 27, '35': 34},
    '16': {'1': 15, '6': 23, '30': 22, '33': 18, '34': 13, '35': 14, '29': 16},'17': {'1': 19, '13': 14},
    '18': {'1': 9, '20': 8},'19': {'1': 14, '29': 17},'20': {'1': 11, '18': 8, '12': 28, '24': 19},
    '21': {'1': 21, '13': 23, '14': 8, '25': 12},'22': {'1': 20, '32': 12},'23': {'1': 21, '2': 13, '27': 11, '31': 27},
    '24': {'1': 19, '20': 19},'25': {'1': 19, '21': 12},'26': {'1': 7, '30': 23, '29': 16},
    '27': {'1': 18, '4': 17, '9': 14, '23': 11, '28': 16},'28': {'1': 26, '27': 16},'29': {'1': 19, '7': 18, '8': 17, '16': 16, '19': 17, '26': 16},
    '30': {'16': 22, '26': 23},'31': {'1': 14, '23': 27},'32': {'22': 12, '39': 28, '1': 19},
    '33': {'16': 18, '1': 30, '38': 27},'34': {'16': 13, '1': 25},'35': {'16': 14, '15': 34},
    '36': {'1': 28, '38': 22},'37': {'1': 29, '10': 35, '41': 10},'38': {'33': 27, '36': 22},
    '39': {'8': 31, '32': 28},'40': {'8': 11, '1': 29, '41': 10, '42': 13},'41': {'37': 10, '40': 10},'42': {'1': 33, '40': 13}
    }

#this is the weights dictionary which reads like 1. Bellville to 3. SAPS-Int Airport is x
#take note we have zeros and ones, we have not done the neccessary computing, it will be done in a for loop below
weights = {
    '1':{'3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 1, '9': 2, '10': 0, '13': 0, '14': 2, '15': 2, '16': 0, '17': 2, '18': 0, '19': 0, '21': 2, '22': 2, '23': 0, '24': 4, '25': 2, '26': 0, '27': 0, '28': 4, '31': 0, '36': 0, '29': 0, '32': 0, '37': 4, '40': 2, '42': 4, '2': 0, '12': 4, '20': 0, '34': 0, '33': 1},
    '2': {'1': 0, '23': 0},'3': {'1': 0, '5': 1},'4': {'1': 0, '27': 0},'5': {'1': 0, '3': 1},
    '6': {'1': 0, '16': 0},'7': {'1': 0, '29': 0},'8': {'1': 1, '39': 1, '40': 0, '29': 0, '10': 1},
    '9': {'1': 2, '27': 0},'10': {'1': 0, '8': 1, '37': 1},'11': {'15': 0},'12': {'1': 4, '20': 1},
    '13': {'1': 0, '15': 0, '17': 0, '21': 0},'14': {'1': 2, '21': 0},'15': {'1': 2, '11': 0, '13': 0, '35': 0},
    '16': {'1': 0, '6': 0, '30': 1, '33': 0, '34': 0, '35': 0, '29': 0},'17': {'1': 2, '13': 0},
    '18': {'1': 0, '20': 0},'19': {'1': 0, '29': 0},'20': {'1': 0, '18': 0, '12': 1, '24': 0},
    '21': {'1': 2, '13': 0, '14': 0, '25': 0},'22': {'1': 2, '32': 0},'23': {'1': 0, '2': 0, '27': 0, '31': 0},
    '24': {'1': 4, '20': 0},'25': {'1': 2, '21': 0},'26': {'1': 0, '30': 1, '29': 0},
    '27': {'1': 0, '4': 0, '9': 0, '23': 0, '28': 0},'28': {'1': 0, '27': 0},'29': {'1': 0, '7': 0, '8': 0, '16': 0, '19': 0, '26': 0},
    '30': {'16': 1, '26': 1},'31': {'1': 0, '23': 0},'32': {'22': 0, '39': 0, '1': 0},'33': {'16': 0, '1': 1, '38': 0},
    '34': {'16': 0, '1': 0},'35': {'16': 0, '15': 0},'36': {'1': 0, '38': 1},'37': {'1': 4, '10': 1, '41': 0},
    '38': {'33': 0, '36': 1},'39': {'8': 1, '32': 0},'40': {'8': 0, '1': 2, '41': 0, '42': 0},'41': {'37': 0, '40': 0},
    '42': {'1': 4, '40': 0}
    }

#here this for loop computes the weight of the routes, using route reports as a guide
for i in distances:
    for j in distances[i]:
        if(route_reports[i][j] == 0):
            weight = (distances[i][j])/(times[i][j])
            weights[i][j] = round(weight, 2)
            
        elif(route_reports[i][j] >= 1):
            weight = ((distances[i][j])/(times[i][j]))*2*route_reports[i][j]
            weights[i][j] = round(weight, 2)
      
#this will calculate the shortest path from depart and destination nodes
def shortest_path(graph, depart, destin):
    infinity = math.inf
    
    #this dictionary will keep the updated distance and weights for shortest path
    node = {
        '1': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '2': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '3': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '4': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '5': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '6': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '7': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '8': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '9': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '10': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '11': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '12': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '13': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '14': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '15': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '16': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '17': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '18': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '19': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '20': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '21': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '22': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '23': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '24': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '25': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '26': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '27': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '28': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '29': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '30': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '31': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '32': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '33': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '34': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '35': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '36': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '37': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '38': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '39': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '40': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '41': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []},
        '42': {'cost': infinity, 'time': 0, 'distance': 0, 'reports': 0, 'prev': []}
        }
    
    node[depart]['cost'] = 0
    visited = []
    temp = depart
    
    min_heap = []
    for i in range(len(node) - 1):
        if temp not in visited:
            visited.append(temp)
            for j in graph[temp]:
                if j not in visited:
                    cost = node[temp]['cost'] + graph[temp][j]
                    distance = node[temp]['distance'] + distances[temp][j]
                    time = node[temp]['time'] + times[temp][j]
                    reports = node[temp]['reports'] + route_reports[temp][j]
                    
                    if cost < node[j]['cost']:
                        if (node[j]['cost'], j) in min_heap:
                            min_heap.remove((node[j]['cost'], j))
                            
                        node[j]['cost'] = round(cost, 2)
                        node[j]['distance'] = distance
                        node[j]['time'] = time
                        node[j]['prev'] = node[temp]['prev'] + list(temp)
                        node[j]['reports'] = reports
                    
                    if (node[j]['cost'], j) not in min_heap:
                        heappush(min_heap, (node[j]['cost'], j))
                    
        heapify(min_heap)
        temp = min_heap[0][1]
        heappop(min_heap)
    
    node[destin]['prev'] = node[destin]['prev'] + list(destin)
    return node[destin]['cost'], node[destin]['distance'], node[destin]['time'], node[destin]['prev'], node[destin]['reports']


while True:
    connectionSocket, addr = serverSocket.accept()
    print("Connected")
    depart, clientAddress = connectionSocket.recvfrom(2048)
    dest, clientAddress = connectionSocket.recvfrom(2048)
    
    #this is for a case where the diparture is the same as the destination
    if(depart.decode() == dest.decode()):
        modifiedMessage1 = "The shortest path from " + depart.decode() + " to " + dest.decode() + " is " + str(0) + ", which is " + str(0) + "km"
        modifiedMessage2 = "This path takes " + str(0) + " minutes, and weighs " + str(0) + ", it also has " + str(0) + " route reports."
       
    #this is for a case where the departure and destination are different
    else:
        weight_updated, distance_updated, time_updated, path_updated, reports_updated = shortest_path(weights, depart.decode(), dest.decode())
        modifiedMessage1 = "The shortest path from " + depart.decode() + " to " + dest.decode() + " is " + str(path_updated) + ", which is " + str(distance_updated) + "km"
        modifiedMessage2 = "This path takes " + str(time_updated) + " minutes, and weighs " + str(weight_updated) + ", it also has " + str(reports_updated) + " route reports."
    
    #here we will send the reply (modified message) to the client
    connectionSocket.send(modifiedMessage1.encode())
    connectionSocket.send(modifiedMessage2.encode())
    connectionSocket.close()

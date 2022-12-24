#Siyanda Mvunyiswa
#4009043 - CSC311 Computer Networking Tut2
#UDP Client

from socket import *
serverName = '127.1.1.0'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

print("""
             ....................Welcome to the Wizz Map....................
      """)
      
print("""
      Choose a number from the list for your departing location and destination:
      
      1. Bellville                            2. Nyanga
      3. SAPS-Int Airport                     4. Bellville South
      5. Philippi                             6. Maitland
      7. Parrow                               8. Lansdowne
      9. Rondebosch                           10. Kuilsriver
      11. Wynberg                             12. Seapoint
      13. Bishop Lavis                        14. Cape Town Central
      15. Table Bay Harbour                   16. Delft
      17. Mowbray                             18. Ravensmead
      19. Goodwood                            20. Elsies River
      21. Port of Entry                       22. Kensington
      23. Athlone                             24. Woodstock
      25. Pinelands                           26. Behlar
      27. Manenberg                           28. Claremont
      29. Gugulethu                           30. Durbanville
      31. Brackenfell                         32. langa
      33. Mitchells Plain                     34. Khayelitsha
      35. Mfuleni                             36. Lingelethu West
      37. Dieprivier                          38. Kleinvlei
      39. Harare                              40. Grassy Park
      41. Steenbrg                            42. Kirstenhof
      """)
    
depart = input("Please enter the departure: e.g enter 1 for Bellville\n")
destination = input("Please enter the detination: e.g enter 2 for Nyanga\n")

clientSocket.send(depart.encode())
clientSocket.send(destination.encode())

modifiedMessage1 = clientSocket.recv(2048)
modifiedMessage2 = clientSocket.recv(2048)

print(modifiedMessage1.decode())
print(modifiedMessage2.decode())

clientSocket.close()


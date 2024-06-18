# fungsiku.py
import math

def getDistance(lat1, lon1, lat2, lon2) -> float:
   # radius bumi
   R = 6373.0

   # konversi dari derajat ke radian
   lat1, lon1 = math.radians(lat1), math.radians(lon1)
   lat2, lon2 = math.radians(lat2), math.radians(lon2)

   # perubahan koordinat
   dlon = lon2 - lon1
   dlat = lat2 - lat1

   # formula haversine
   a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

   distance = R * c

   return distance
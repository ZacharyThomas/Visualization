'''
Created on Oct 29, 2014

@author: jeff
'''

# Open route_points and generate text to be used in html file

import sys

def main():
    # open first file containing original route points
    with open(sys.argv[1], 'r') as f1:
        # second file will contain paths
        with open(sys.argv[2], 'w') as f2:
            # third file will contain js to draw polylines
            with open(sys.argv[3], 'w') as f3:
                count=0
                for lines in f1:
                    count = count + 1
                    f2.write('path%d = '%count + lines[12:-2] + ';\n')
                    
                    f3.write("    map.drawPolyline({\n        path: path%d,\n        strokeColor: '#131540',\n        strokeOpacity: 0.3,\n        strokeWeight: 3\n      });\n" %count)

if __name__=="__main__":
    main()


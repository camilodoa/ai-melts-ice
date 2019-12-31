import pandas as pd
import numpy as np
from query import Syracuse

class Generator():

    def __init__(self):
        # Reinitialize dataset (T/F)
        self.reinit = False

        # City name to number mappings
        self.city_mappings = {
            'NEW ORLEANS INTERNATIONAL AIRPORT, NEW ORLEANS LA': 1, 'EL PASO, TX': 2, 'PORTLAND, OR': 3, 'NOGALES, AZ': 4, 'MIAMI INTERNATIONAL AIRPORT, MIAMI FLORIDA': 5, "CHICAGO-O'HARE INTERNATIONAL AIRPORT, CHICAGO IL": 6, 'LOS ANGELES, CA': 7, 'PHOENIX, AZ': 8, 'HOUSTON, TX': 9, 'LAREDO, TX': 10, 'PASO DEL NORTE, TX': 11, 'OTAY MESA, CA': 12, 'SAN FRANCISCO, CA': 13, 'DALLAS, TX': 14, 'BROWNSVILLE, TX': 15, 'RIO GRANDE CITY, TX': 16, 'TAMPA, FL': 17, 'HARTSFIELD INTERNATIONAL AIRPORT, ATLANTA, GA': 18, 'HIDALGO, TX': 19, 'NEW YORK, NY': 20, 'SAN YSIDRO, CA': 21, 'CALEXICO, CA': 22, 'DETROIT, MI': 23, 'DULLES INTERNATIONAL AIRPORT, WASHINGTON DC': 24, 'LOGAN INTERNATIONAL AIRPORT, BOSTON MA': 25, 'SAN DIEGO, CA (AIRPORT)': 26, 'DEL RIO, TX': 27, 'NEWARK INTERNATIONAL AIRPORT, NEWARK NJ': 28, 'PHILADELPHIA INTERNATIONAL AIRPORT, PHILADELPHIA, PA': 29, 'SAJ/A ANTONIO RIVERA-RODRIGUEZ AIRPORT': 30, 'CHARLOTTE AMALIE, ST. THOMAS, VI': 31, 'SAN LUIS, AZ': 32, 'MINNEAPOLIS/ST. PAUL, MN': 33, 'BUFFALO, NY': 34, 'CINCINNATI, OH': 35, 'HARLINGEN, TX': 36, 'COLUMBUS, NM': 37, 'YSLETA, TX': 38, 'AGANA, GUAM': 39, 'NIAGARA FALLS, NY': 40, 'DETROIT, MI (BRIDGE)': 41, 'ORLANDO, FL': 42, 'BALTIMORE, MD, SOUTH LOCUST POINT MARINE TERMINAL(SEAPORT)': 43, 'DULUTH, MN': 44, 'ST. PAUL, MN': 45, 'UNKNOWN': 46, 'SEATTLE, WA': 47, 'TACOMA, WA': 48, 'HARTFORD, CT': 49, 'ANCHORAGE, AK': 50, 'LAS VEGAS, NV': 51, 'DENVER, CO': 52, 'AGUADILLA, PR': 53, 'RENO, NV': 54, 'PEACE BRIDGE, NY': 55, 'OROVILLE, WA': 56, 'RAINBOW BRIDGE, NY': 57, 'JACKMAN, ME': 58, 'CHAMPLAIN, NY': 59, 'PRESIDIO, TX': 60, 'JUAREZ-LINCOLN BRIDGE, TX': 61, 'LOS INDIOS, TX (FREE TRADE BRIDGE)': 62, 'SARLES, ND': 63, 'BLAINE, WA': 64, 'NACO, AZ': 65, 'CLEVELAND, OH': 66, 'HONOLULU, HI': 67, 'DOUGLAS, AZ': 68, 'FORT LAUDERDALE, FL': 69, 'NORFOLK, VA': 70, 'BRIDGE OF AMERICAS, TX': 71, 'FALCON HEIGHTS, TX': 72, 'LOUISVILLE, KY': 73, 'CHRISTIANSTED, ST. CROIX, VI': 74, 'VANCOUVER, WA': 75, 'OMAHA, NE': 76, 'PROGRESO, TX': 77, 'LUKEVILLE, AZ': 78, 'TUCSON, AZ': 79, 'SAN PEDRO, CA': 80, 'WILMINGTON, NC': 81, 'MEMPHIS, TN': 82, 'PHARR, TX': 83, 'SALT LAKE CITY, UT': 84, 'TOLEDO, OH': 85, 'ST. ALBANS, VT': 86, 'MAYAGUEZ, PR': 87, 'TECATE, CA': 88, 'SUMAS, WA': 89, 'HELENA, MT': 90, 'MASSENA, NY': 91, 'DEL BONITA, MT': 92, 'PROVIDENCE, RI': 93, 'MAIDA, ND': 94, 'PORTLAND, ME': 95, 'SAN JOSE, CA': 96, 'PORT HURON, MI': 97, 'HIGHGATE SPRINGS, VT': 98, 'MCALLEN, TX': 99, 'CHARLOTTE, NC': 100, 'DETROIT, MI (AIRPORT)': 101, 'ROMA, TX': 102, 'ALEXANDRIA BAY, NY': 103, 'SAN ANTONIO, TX': 104, 'ALBANY, NY': 105, 'KANSAS CITY MO': 106, 'OVERTON CORNERS, NY': 107, 'BATON ROUGE, LA': 108, 'PEMBINA, ND': 109, 'RALEIGH/DURHAM, NC': 110, 'SASABE, AZ': 111, 'SEATTLE, WA, SEAPORT': 112, 'EAGLE PASS, TX': 113, 'PORT OF EL PASO, TX': 114, 'PITTSBURG INTERNATIONAL AIRPORT, PITTSBURG PA': 115, 'NORTH TROY, VT': 116, 'GULFPORT, MS': 117, 'OKLAHOMA CITY, OK': 118, 'ANDRADE, CA': 119, 'BAUDETTE, MN': 120, 'ST. LOUIS, MO': 121, 'JUNEAU, AK': 122, 'LAREDO COLUMBIA BRIDGE, TX': 123, 'BROWNSVILLE-MATAMOR, TX': 124, 'FRONTIER, WA': 125, 'LAKE CHARLES, LA': 126, 'SANTA TERESA, NM': 127, 'PACIFIC HIGHWAY, WA': 128, 'MADAWASKA, ME': 129, 'ST. JOHN, ND': 130, 'LEWISTON, NY (QUEENSTONE BRIDGE)': 131, 'EAGLE PASS, TX, INTL BRIDGE #2': 132, 'PORT EVERGLADES, FL': 133, 'TURNER, MT': 134, 'SWEETGRASS, MT': 135, 'FORT PIERCE, FL': 136, 'PASCAGUOLA, MS': 137, 'FABENS, TX': 138, 'TORONTO, CANADA': 139, 'NIGHTHAWK, WA': 140, 'CAPE CANAVERAL, FL': 141, 'DETROIT, MI (TUNNEL)': 142, 'CALGARY, ALBERTA, CANADA': 143, 'ANTLER, ND': 144, 'CARBURY, ND': 145, 'NASSAU, BAHAMAS': 146, 'LORAINE, OH': 147, 'CHARLESTON, SC': 148, 'ST. PAMPILE, ME': 149, 'COLUMBUS, OH': 150, 'ALBUQUERQUE, NM': 151, 'LONGVIEW, WA': 152, 'LYNDEN, WA': 153, 'SACRAMENTO, CA': 154, 'JACKSONVILLE, FL': 155, 'CALAIS, ME': 156, 'WEST PALM BEACH, FL': 157, 'SAULT ST. MARIE, MI': 158, 'PINE CREEK, MN': 159, 'FORT HANCOCK, TX': 160, 'BELLINGHAM, WA': 161, 'BRUNSWICK, GA': 162, 'HOULTON, ME': 163, 'FERRY, WA': 164, 'AUSTIN, TX': 165, 'INTERNATIONAL FALLS, MN': 166, 'ROUSES POINT, NY': 167, 'MORSES LINE, VT': 168, 'CALEXICO-EAST, CA': 169, 'DERBY LINE, VT (I-91)': 170, 'ALPENA, MI': 171, 'MILWAUKEE, WI': 172, 'CORPUS CHRISTI, TEXAS': 173, 'ERIE, PA': 174, 'OGDENSBURG, NY': 175, 'ELY, MN': 176, 'OAKLAND COUNTY INTERNATIONAL AIRPORT - USER FEE': 177, 'CLAYTON, NY': 178, 'Ontario International Airport': 179, 'LOS EBANOS, TX': 180, 'ALCAN, AK': 181, 'FORT MYERS, FL': 182, 'WALHALLA, ND': 183, 'THOUSAND ISLAND BRIDGE, NY': 184, 'NIKISKI, AK': 185, 'MONTREAL CANADA': 186, 'KEY WEST, FL': 187, 'BUTTE, MT': 188, 'EASTPORT, ID': 189, 'NEW ORLEANS, LA (AIRPORT)': 190, 'LINCOLN, NE': 191, 'NORTON, VT': 192, 'SAN DIEGO, CA': 193, 'FREEPORT, TX': 194, 'HAINES, AK': 195, 'SANFORD, FL': 196, 'CANAAN, VT': 197, 'BRIDGEWATER, ME': 198, 'WEST SUSSEX, ENGLAND': 199, 'NASHVILLE, TN': 200, 'NOME, AK (SEAPORT)': 201, 'YUMA, AZ': 202, 'DUBLIN, IRELAND': 203, 'PONCE, PR': 204, 'LANCASTER, MN': 205, 'PORTHILL, ID': 206, 'ALBURG SPRINGS, VT': 207, 'Saipan, MP': 208, 'PORTAL, ND': 209, 'LAURIER, WA': 210, 'BURLINGTON, VT': 211, 'OAKLAND, CA': 212, 'NEAH BAY, WA': 213, 'PANAMA CITY, FL': 214, 'PIEGAN, MT': 215, 'VICTORIA, CANADA': 216, 'VETERANS INTL BRIDGE, TX': 217, 'PENSACOLA, FL': 218, 'INDIANAPOLIS, IN': 219, 'MARIPOSA, AZ': 220, 'STANTON ST BRIDGE, TX': 221, 'VANCOUVER, CANADA': 222, 'ANZALDUAS CROSSING PORT OF ENTRY': 223, 'PORT ARTHUR, TX': 224, 'EDMONTON, CANADA': 225, 'KALAMA, WA': 226, 'ANACORTES, WA': 227, 'ASTORIA, OR': 228, 'BOUNDARY, WA': 229, 'JAMISONS LANE, NY': 230, 'METALINE FALLS, WA': 231, 'DANVILLE, WA': 232, 'FORT KENT, ME': 233, 'GALVESTON, TX': 234, 'MOBILE, AL': 235, 'SAVANNAH, GA': 236, 'HOBBY AIRPORT': 237, 'GRAND PORTAGE, MN': 238, 'GEORGETOWN, SC': 239, 'OTTAWA, CANADA': 240, 'ALBURG, VT': 241, 'TROUT RIVER, NY': 242, 'FRESNO, CA': 243, 'PITTSBURG, NH': 244, 'WARROAD, MN': 245, 'ABERDEEN, WA': 246, 'HOUSTON, TX (AIRPORT)': 247, 'BANGOR INTERNATIONAL AIRPORT, BANGOR ME': 248, 'HANSBORO, ND': 249, 'RICHFORD, VT': 250, 'AMISTAD DAM, TX': 251, 'GROTON, CT': 252, 'GRIFFING AIRPORT, SANDUSKY, OHIO': 253, 'MORLEY GATE, AZ': 254, 'DALTON CACHE, AK': 255, 'PORT ANGELES, WA': 256, 'NEW YORK, LAGUARDIA': 257, 'POINT ROBERTS, WA': 258, 'NEWPORT, OR': 259, 'NOYES, MN': 260, 'KETCHIKAN, AK': 261, 'ANTELOPE WELLS, NM': 262, 'NECHE, ND': 263, 'EAGLE, AK': 264, 'NOONAN, ND': 265, 'LONG BEACH CA SEAPORT/POE': 266, 'MARINE CITY, MI': 267, 'EASTPORT, ME': 268, 'FORTUNA, ND': 269, 'GRAND FORKS, ND': 270, 'COBURN GORE, ME': 271, 'FORT COVINGTON, NY': 272, 'HAMILTON, BERMUDA': 273, 'WILLOW CREEK, MT': 274, 'CHERRY HILL, NJ': 275, 'NEWPORT NEWS, VA': 276, 'ARUBA, NETH ANTILLES': 277, 'MORGAN, MT': 278, 'CHATEAUGAY, NY': 279, 'WILD HORSE, MT': 280, 'MIDDLESEX, ENGLAND': 281, 'LUBEC, ME': 282, 'VANCEBORO, ME': 283, 'WINNIPEG, CANADA': 284, 'FREEPORT, BAHAMAS': 285, 'ROSEAU, MN': 286, 'DAAQUAM, ME': 287, 'MIDWAY (CHICAGO), IL': 288, 'CHIEF MOUNTAIN, MT': 289, 'PINNACLE ROAD, VT': 290, 'RAYMOND, MT': 291, 'PORT OF CHATTANOOGA': 292, 'WEST BERKSHIRE, VT': 293, 'ANDREWS AFB, MD': 294, 'CRANE LAKE, MN': 295, 'SYRACUSE, NY': 296, 'ROOSVILLE, MT': 297, 'SKAGWAY, AK': 298, 'HALIFAX INTERNATIONAL AIRPORT - PRECLEARANCE': 299, 'ORIENT, ME': 300, 'NEWPORT, VT': 301, 'VALLEY INTERNATIONAL AIRPORT': 302, 'ST. CLAIR, MI': 303, 'BEECHER FALLS, VT': 304, 'EAST RICHFORD, VT': 305, 'DES MOINES, IA': 306, 'VAN BUREN, ME': 307, 'PATUXENT RIVER, MD': 308, 'MEDFORD, OR': 309, 'CANNON CORNERS, NY': 310, 'KEAHOLE-KONA, HI': 311, 'DOVER AFB, DE': 312, 'ESTCOURT, ME': 313, 'CRUZ BAY, ST. JOHN, VI': 314, 'AMBROSE, ND': 315, 'WHIRLPOOL BRIDGE, NY': 316, 'LAREDO, TX, WORLD TRADE BRIDGE': 317, 'MILLTOWN, ME': 318, 'BEEBE PLAIN, VT': 319, 'MOREHEAD CITY, NC': 320, 'NORTHGATE, ND': 321, 'FAIRBANKS, AK': 322, 'ALGONAC, MI': 323, 'GREER, SC': 324, 'SPOKANE, WA': 325, 'VENTURA, CA': 326, 'WHITETAIL, MT': 327, 'DUTCH HARBOR, AK': 328, 'MINOT, ND': 329, 'HANNAH, ND': 330, 'DONNA, TX': 331, 'DERBY LINE, VT (RT. 5)': 332, 'Tinian International Airport': 333, 'CHURUBUSCO, NY': 334, 'WELLESLEY ISLAND, NY': 335, 'FORT FAIRFIELD, ME': 336, 'BENJAMIN RIVERA NORIEGA AIRPORT - CULEBRA': 337, 'BAR HARBOR, ME': 338, 'HAMLIN, ME': 339, 'LIMESTONE, ME': 340, 'CAPE VINCENT, NY': 341, 'POKER CREEK, AK': 342, 'PRINCE RUPERT, CANADA': 343, 'NEW YORK, NY (KENNEDY)': 344, "Luis Munoz Marin Int'l Airport": 345, 'ATLANTA, GA, AIRPORT': 346, 'SAN JUAN, PR': 347, 'LOS ANGELES, CA, AIRPORT': 348, 'PORT ISABEL, TX': 349, 'MIAMI SEAPORT FL': 350, 'NEW HAVEN, CT': 351, 'BOSTON, MA (LOGAN)': 352, 'NEW LONDON, CT': 353, 'HARRISBURG, PA': 354, 'SCOBEY, MT': 355, 'SHANNON, IRELAND': 356, 'Atlantic City International Airport': 357, 'ROCHESTER, NY': 358, 'GRAND RAPIDS PORT OF ENTRY': 359, 'Pinecreek Port of Entry': 360, 'ALEXANDRIA INTERNATIONAL AIRPORT': 361, 'FORT STREET CARGO FACILITY': 362, 'BALTIMORE, MD (AIRPORT)': 363, 'RICHMOND, VA': 364, 'Sitka, Alaska - Port Code 3115 (CBP Seaport POE)': 365, 'AKRON, OH': 366, 'LIHUE, HI': 367, 'ASHTABULA, OH': 368, 'BRIDGEPORT, CT': 369, 'NAPLES, FL PORT OF ENTRY': 370, 'EASTON, ME': 371, 'John Wayne Airport': 372, 'Otay Cross Border Express': 373, 'DUNSEITH, ND': 374, 'CAMPO, CA': 375, 'WILMINGTON, DE': 376, 'Port Manatee, FL Port of Entry': 377, 'EVERETT, WA': 378, 'FOREST CITY, ME': 379, 'PORT OF BATTLE CREEK': 380, 'BUCKPORT, ME': 381, 'Appleton International Airport': 382, 'LAKELAND USER FEE AIRPORT': 383, 'PORTSMOUTH, NH': 384
        }

    '''
    Dataset initialization functions
    '''
    def fetch(self, city):
        'Queries Syracuse DB for data on a particular city, based on #'
        s = Syracuse()
        return s.query(str(city))

    def fill(self):
        'Fills out empty Pandas DF with Syracuse data'
        s = Syracuse()
        df = pd.DataFrame()

        'Create dictionary to make the transition to dataset easier'
        dict = {}

        for city in range(s.cities):
            json = self.fetch(city)
            print(json['title'])

            if json['title'] == '':
                continue

            for point in json['timeline']:
                date = pd.to_datetime(point['fymon'])
                city = json['title'].replace(', POE', '')

                if dict.get(date) == None:
                    dict[date] = {'Date' : date}

                dict[date][city] = int(point['number'])

        'Transfer dictionary layout to dataset'
        for data in dict.values():
            df = df.append(data, ignore_index = True, sort = False)

        df = df.fillna(0)
        df.sort_values(by='Date')
        return df

    def initialize(self):
        'Initializes and saves Syracuse data to file (data.csv)'
        df = self.fill()

        ok = ''
        while ok != 'y' and ok != 'n':
            ok = input('Overwrite data.csv? Y/N: ').lower().strip()

        if ok.lower() == 'n':
            return None

        df.to_csv('data.csv')
        return df

    def split(self, df):
        data = df.values
        train_size = int(len(data) * 0.67)
        test_size = len(data) - train_size
        train, test = data[0:train_size, :], data[train_size:len(df), :]

        return train, test

    def LSTM_convert(self, df, look_back=1):
    	dataX, dataY = [], []
    	for i in range(len(df) - look_back - 1):
    		a = df[i : (i+look_back), 0]

    		dataX.append(a)
    		dataY.append(df[i + look_back, 0])

    	return np.array(dataX), np.array(dataY)

if __name__ == '__main__':
    g = Generator()
    print(g.initialize().values)

###################
# whois - guess IP country location
#
# Copyright Jean-Michel Philippe (c) 2007
#   <http://philipjm.free.fr/blog/>
#
# This is open source software released under the GPL license.
# The full text of this license is found in the file 'LICENSE',
# included with this source code package.
###################

"""
whois Python module
-------------------

Guess host location from their IP, based on whois services.

2 method are implemented:

* IP searched in a local database
* IP searched on an Internet whois service

Search results are stored in a local database to speedup further identical
searches. Use of former results can be disabled. Internet whois search can
be disabled too.

Local databases can be downloaded/updated from:
   http://software77.net/cgi-bin/ip-country/geo-ip.pl
   http://ip-to-country.webhosting.info/node/view/6

Full Internet whois queries may also be accessed.

Usage
-----

Import whois module:

 >>> import whois
 > loaded 79552 IP ranges from /usr/lib/.../whois/db/IpToCountry.csv.db

Query host country:

 >>> print whois.guessIPcountry('194.109.137.218')
 NETHERLANDS

Full Internet whois query:

 >>> Whois = whois.WhoisConsumer('194.109.137.218')
 >>> whois.WhoisRequest(Whois, whois.WhoisServer)
 <whois._whois.WhoisRequest at -0x4a62ce74>
 >>> whois.asyncore.loop()
 >>> print Whois.text
 
 OrgName:    RIPE Network Coordination Centre
 OrgID:      RIPE
 Address:    P.O. Box 10096
 City:       Amsterdam
 StateProv:
 PostalCode: 1001EB
 Country:    NL
 
 ReferralServer: whois://whois.ripe.net:43
 
 NetRange:   194.0.0.0 - 194.255.255.255
 CIDR:       194.0.0.0/8
 NetName:    RIPE-CBLK2
 NetHandle:  NET-194-0-0-0-1
 Parent:
 NetType:    Allocated to RIPE NCC
 NameServer: NS-PRI.RIPE.NET
 NameServer: NS3.NIC.FR
 NameServer: SUNIC.SUNET.SE
 NameServer: NS-EXT.ISC.ORG
 NameServer: SEC1.APNIC.NET
 NameServer: SEC3.APNIC.NET
 NameServer: TINNIE.ARIN.NET
 Comment:    These addresses have been further assigned to users in
 Comment:    the RIPE NCC region. Contact information can be found in
 Comment:    the RIPE database at http://www.ripe.net/whois
 RegDate:    1993-07-21
 Updated:    2005-08-03
 
 # ARIN WHOIS database, last updated 2007-03-24 19:10
 # Enter ? for additional hints on searching ARIN's WHOIS database.

Querying coordinates of a single country:

 >>> whois.geomap.getLongLat('SPAIN')
 (40.0, -4.0)

Drawing the world map with circles at given countries:

 >>> from pylab import show
 >>> whois.geomap.world({'CANADA': 48, 'FRANCE': 4, 'INDIA': 570})
 >>> show()
"""

###################
# versionning
__author__ = "jean-michel.philippe@libertysurf.fr"
__url__ = "http://philipjm.free.fr/blog/"
__version__ = "0.2.0"

###################
# importations
import os, csv, asyncore, re, cPickle, md5
from types import *
from requester import WhoisRequest, WhoisConsumer


###################
# constants

# whois server (see http://www.frameip.com/whois/)
WhoisServer = "whois.arin.net"
#WhoisServer = "whois.ripe.net"
#WhoisServer = "whois.apnic.net"
#WhoisServer = "whois.lacnic.net"
#WhoisServer = "whois.registro.br"
#WhoisServer = "whois.nic.ad.jp"



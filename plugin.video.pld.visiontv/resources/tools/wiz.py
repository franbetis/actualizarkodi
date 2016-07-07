# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  Unpack para PLD.VisionTV
# Version 0.0.4 (29.11.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *

def unpack(sJavascript,iteration=1, totaliterations=1  ):
 aSplit = sJavascript.split("rn p}('")
 p1,a1,c1,k1=('','0','0','')
 ss="p1,a1,c1,k1=(\'"+aSplit[1].split(".spli")[0]+')';exec(ss)
 k1=k1.split('|')
 aSplit = aSplit[1].split("))'")
 e = '';d = ''
 sUnpacked1 = str(__unpack(p1, a1, c1, k1, e, d,iteration))
 if iteration>=totaliterations: return sUnpacked1
 else: return unpack(sUnpacked1,iteration+1)
def __unpack(p, a, c, k, e, d, iteration,v=1):
 while (c >= 1):
  c = c -1
  if (k[c]):
   aa=str(__itoaNew(c, a))
   p=re.sub('\\b' + aa +'\\b', k[c], p)
 return p
def __itoa(num, radix):
 result = ""
 if num==0: return '0'
 while num > 0: result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result;num /= radix
 return result
def __itoaNew(cc, a):
 aa="" if cc < a else __itoaNew(int(cc / a),a)
 cc = (cc % a)
 bb=chr(cc + 29) if cc> 35 else str(__itoa(cc,36))
 return aa+bb
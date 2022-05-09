import re
import csv 
if __name__ == '__main__':

    pus = re.compile(r'\bUnited States of America\b',re.I)
    pus1 = re.compile(r'\bUnited States\b',re.I)
    psp = re.compile(r' *, *')
    def fix_address(address):
        address = address.strip(', ')
        address = pus.sub('USA',address)
        address = pus1.sub('USA',address)
        address = psp.sub(', ',address)
        return address
test = [0, 1, 2, 10, 12, 17, 18, 20, 27, 28, 30, 1589, 1590, 1596, 1600, 1602, 1607, 1612, 1618, 1619, 1620, 1622, 1624, 1631, 1632, 1635, 1636, 1640, 1642, 1648, 1650, 1651, 1654, 1656, 1657, 1665, 1669, 1670, 1675, 1676, 1685, 1688, 1691, 1693, 1695, 1699, 1704, 1712, 1715, 1716, 1719, 1720, 1725, 1726, 1728, 1729, 1730, 1733, 1734, 1736, 1739, 1740, 1742, 1745, 1750, 1754, 1755, 1758, 1760, 1763, 1765, 1767, 1768, 1780, 1781, 1783, 1787, 1789, 1790, 1791, 1793, 1794, 1795, 1803, 1805, 1808, 1810, 1811, 1815, 1818, 1822, 1824, 1825, 1826, 1827, 1829, 1832, 1837, 1840, 1841, 1848, 1850, 1853, 1855, 1856, 1857, 1860, 1861, 1862, 1864, 1865, 1866, 1876, 1878, 1881, 1884, 1886, 1890, 1906, 1924, 1925, 1926, 1928, 1945, 1954, 1976, 2013]

with open('C:/Users/j/xtmp.lst') as f:
    for line in f:
        line = line.strip()
        with open(line, newline='', encoding='utf-8') as csvfile:
            ahnreader = csv.reader(csvfile) 
            for row in ahnreader:
               for i in [3,5]:
                   try:
                      ad = row[i]
                      if ad:
                          ad = fix_address(ad)
                      if ad in test:
                          print (row)
                   except:
                       print("err",line,row)


import hemipy as hp

zentih = hp.zenith([4608, 3456], [2304, 1728], cal_fun=[1,1,1])
azimuth = hp.azimuth([4608, 3456], [2304, 1728])
result = hp.process('/Users/wangbin/PythonSpace/PythonEX/FLApy/HI/djb', zentih, azimuth, '2023-10-22', 24)
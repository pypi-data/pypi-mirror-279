# -*- coding: utf-8 -*-

#---------------------------------------------------------------------#
#   FLApy:A Calculator of Illumination factor within Understory  #
#   IA:Illumination factors calculator/interpolation/change analysis  #
#   Virsion: 1.0                                                      #
#   Developer: Wang Bin (Yunnan University, Kunming, China)           #
#   Latest modification time: 2021-5-20                               #
#---------------------------------------------------------------------#

import FLApy as fp
import numpy as np
import healpy as hp
import open3d as o3d
import utm
import pyvista as pv


from scipy.spatial import Delaunay
from astropy.time import Time
from astropy import units as u



def extractByOnePoints(inPoints, centerP, radius, method = 'square', considerZ = False):


    CPX = centerP[0]
    CPY = centerP[1]
    CPZ = centerP[2]

    if method == 'square':

        Xmin = CPX - radius
        Xmax = CPX + radius
        Ymin = CPY - radius
        Ymax = CPY + radius
        Zmin = CPZ - radius
        Zmax = CPZ + radius

        if considerZ == True:

            xInvalid = np.logical_and((inPoints[:, 0] >= Xmin), (inPoints[:, 0] <= Xmax))
            yInvalid = np.logical_and((inPoints[:, 1] >= Ymin), (inPoints[:, 1] <= Ymax))
            zInvalid = np.logical_and((inPoints[:, 2] >= Zmin), (inPoints[:, 2] <= Zmax))

            keptIndices = np.where(np.logical_and(xInvalid, yInvalid, zInvalid))
            keptPoints = inPoints[keptIndices]

        elif considerZ == False:
            xInvalid = np.logical_and((inPoints[:, 0] >= Xmin), (inPoints[:, 0] <= Xmax))
            yInvalid = np.logical_and((inPoints[:, 1] >= Ymin), (inPoints[:, 1] <= Ymax))

            keptIndices = np.where(np.logical_and(xInvalid, yInvalid))
            keptPoints = inPoints[keptIndices]

        return keptPoints


    elif method == 'cylinder':

        if considerZ == True:
            return

    elif method == 'sphere':
        disT = np.sum((inPoints - centerP) ** 2, axis = 1)
        keptP = disT <= radius
        pKept = inPoints[keptP]
        return (pKept)

def extractByObs(inPoints, inObs):

    x_obs_min, x_obs_max = np.min(inObs[:, 0]), np.max(inObs[:, 0])
    y_obs_min, y_obs_max = np.min(inObs[:, 1]), np.max(inObs[:, 1])

    xInvalid = np.logical_and((inPoints[:, 0] >= x_obs_min), (inPoints[:, 0] <= x_obs_max))
    yInvalid = np.logical_and((inPoints[:, 1] >= y_obs_min), (inPoints[:, 1] <= y_obs_max))

    keptIndices = np.where(np.logical_and(xInvalid, yInvalid))

    keptPoints = inPoints[keptIndices]

    return keptPoints

def refer2HealSys(inPhi):

    ex = inPhi[np.where(inPhi < 0)]
    modified = 2 * np.pi + ex
    kept = inPhi[np.where(inPhi>=0)]

    return  np.append(kept, modified)

def removeOutliers(inPoints, nb = 20, std_ratio = 15.0):
    pointCloudInit = o3d.geometry.PointCloud()
    pointCloudInit.points = o3d.utility.Vector3dVector(inPoints)
    cl, ind = pointCloudInit.remove_statistical_outlier(nb_neighbors = nb, std_ratio = std_ratio)
    keptPoints = inPoints[ind]
    return keptPoints

def utm2latlon(inLat, inLon, inZone):
    return utm.to_latlon(inLat, inLon, inZone, 'U')

def latlon2utm(inLat, inLon, inZone):
    return utm.from_latlon(inLat, inLon, inZone, 'U')


def sphereGridGenerator(nside, step = 1):
    numPixl = hp.nside2npix(nside)
    list1 = []
    for index_read in range(numPixl):
        a = hp.boundaries(nside, index_read, step=step, nest=False)
        b = np.transpose(a)
        list1.append(b)

    xl = []
    yl = []
    zl = []
    for index_merge in range(len(list1)):
        for index_into in range(4):
            x = list1[index_merge][index_into][0]
            y = list1[index_merge][index_into][1]
            z = list1[index_merge][index_into][2]

            xl.append(x)
            yl.append(y)
            zl.append(z)

    merge = np.vstack((xl, yl, zl)).transpose()
    mergeE = np.unique(merge, axis=0)
    return mergeE

def healpixCenterPointsGenerator(nside):
    healpixIndex = np.arange(hp.nside2npix(nside))
    allHealpixCP = hp.pix2ang(nside = nside, ipix=healpixIndex)
    allHealpixCP_theta = allHealpixCP[0]
    allHealpixCP_phi = allHealpixCP[1]
    allHealpixCP_phi_adjusted = np.where(allHealpixCP_phi > np.pi, allHealpixCP_phi - 2 * np.pi, allHealpixCP_phi)


    r = np.ones(len(allHealpixCP_theta))
    return np.vstack((allHealpixCP_theta, allHealpixCP_phi_adjusted, r)).transpose()


def getSkyPixelPoints(inM, nside = int(fp.nsideConfig)):
    skyIndex = np.where(inM == 1)
    obscuredIndex = np.where(inM == 0)

    listSky = []
    listObscured = []

    for index_sky in skyIndex[0]:
        a = hp.boundaries(nside, index_sky, 1, nest=False)
        b = np.transpose(a)
        listSky.append(b)

    xl_sky = []
    yl_sky = []
    zl_sky = []

    for index_merge_sky in range(len(listSky)):
        for index_into_sky in range(4):
            x_sky = listSky[index_merge_sky][index_into_sky][0]
            y_sky = listSky[index_merge_sky][index_into_sky][1]
            z_sky = listSky[index_merge_sky][index_into_sky][2]

            xl_sky.append(x_sky)
            yl_sky.append(y_sky)
            zl_sky.append(z_sky)

    mergeSky = np.vstack((xl_sky, yl_sky, zl_sky)).transpose()
    mergeSkyE = np.unique(mergeSky, axis = 0)

    return mergeSkyE

def in_hull(p, hull):
    if not isinstance(hull, Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0

def judgeRelativePosition_label(inAllPoints, testedPoints, radius = 10):

    judgeResultlist = []



    if len(testedPoints) == 0:
        raise OSError('At least one tested point is required.')
    else:
        for indexJRP in range(len(testedPoints)):
            hullPoints = fp.Tools.extractByOnePoints(inAllPoints, centerP=testedPoints[indexJRP], radius=radius)
            judgeResult = in_hull(testedPoints[indexJRP], hullPoints)
            judgeResultlist.append(judgeResult)

    return judgeResultlist




def timeSeriesGenerator(timeStart, timeNo, unit = 'h', step = 1):

    timeS = Time(timeStart)

    timeList = []

    if unit == 'h':
        for timeGenerate in range(int(timeNo + 1)):
            timeA = timeS + u.hour * timeGenerate * step
            timeList.append(str(timeA))

    elif unit == 'm':
        for timeGenerate in range(int(timeNo + 1)):
            timeA = timeS + u.minute * timeGenerate * step
            timeList.append(str(timeA))

    elif unit == 's':
        for timeGenerate in range(int(timeNo + 1)):
            timeA = timeS + u.second * timeGenerate * step
            timeList.append(str(timeA))

    elif unit == 'd':
        for timeGenerate in range(int(timeNo + 1)):
            timeA = timeS + u.day * timeGenerate * step
            timeList.append(str(timeA))

    elif unit == 'y':
        for timeGenerate in range(int(timeNo + 1)):
            timeA = timeS + u.year * timeGenerate * step
            timeList.append(str(timeA))



    return timeList



def pointSize(SizeMin, SizeMax, inAllPointsCBO):
    if SizeMax > SizeMin:
        distance = np.sqrt(np.sum(inAllPointsCBO ** 2, axis=1))
        Dmin, Dmax = np.min(distance), np.max(distance)
        position = (distance - Dmin) / (Dmax - Dmin)
        r = ((1 - position) * (SizeMax - SizeMin)) + SizeMin
    else:
        raise OSError('The value of point size is incorrect.')

    return r

def pointSize_n(SizeMin, delta, inAllPointsCBO):
    rmin = SizeMin
    rmax = rmin + delta

    distance = np.sqrt(np.sum(inAllPointsCBO ** 2, axis=1))
    Dmin, Dmax = np.min(distance), np.max(distance)
    position = (distance - Dmin) / (Dmax - Dmin)
    r = ((1 - position) * (rmax - rmin)) + rmin

    return r

def maxDistance(inAllPoints):
    Xmax, Xmin = np.max(inAllPoints[:, 0]), np.min(inAllPoints[:, 0])
    Ymax, Ymin = np.max(inAllPoints[:, 1]), np.min(inAllPoints[:, 1])
    Zmax, Zmin = np.max(inAllPoints[:, 2]), np.min(inAllPoints[:, 2])

    return np.sqrt(((Xmax - Xmin) ** 2) + ((Ymax - Ymin) ** 2) + ((Zmax - Zmin) ** 2))

def voxelDownsampling(inPoints, resolution = 0.5):
    pointCloudInit = o3d.geometry.PointCloud()
    pointCloudInit.points = o3d.utility.Vector3dVector(inPoints)
    vd = pointCloudInit.voxel_down_sample(voxel_size=resolution)
    return np.array(vd.points)



def verticalObsWithinForestGenerator(inPoints,
                                     inLocation = (float(fp.dXlocation),
                                                   float(fp.dYlocation)),
                                     resolution = 10):

    inObsX = inLocation[0]
    inObsY = inLocation[1]

    Xmin = inObsX - 2
    Xmax = inObsX + 2
    Ymin = inObsY - 2
    Ymax = inObsY + 2



    xInvalid = np.logical_and((inPoints[:, 0] >= Xmin), (inPoints[:, 0] <= Xmax))
    yInvalid = np.logical_and((inPoints[:, 1] >= Ymin), (inPoints[:, 1] <= Ymax))

    keptIndices = np.where(np.logical_and(xInvalid, yInvalid))
    keptPoints = inPoints[keptIndices]

    keptPoints_Z_min = np.min(keptPoints[:, 2])
    keptPoints_Z_max = np.max(keptPoints[:, 2])

    zFull = np.linspace(keptPoints_Z_min, keptPoints_Z_max, num = resolution)

    num = np.arange(resolution, dtype = int)
    xFull = np.full_like(num, inObsX, dtype = np.double)
    yFull = np.full_like(num, inObsY, dtype = np.double)

    xyz = np.vstack((xFull, yFull, zFull)).transpose()

    if len(inLocation) < 4:

        return xyz

    if len(inLocation) == 4:
        import pandas as pd
        name  = str(inLocation[3])
        df = pd.DataFrame(xyz)
        df.columns = ['x','y','z']

        df['Name'] = name
        #nameFull = pd.full_like(num, name, dtype = '<U30').transpose()
        #dtype = np.dtype([('x', '<U30'), ('y', '<U30'), ('z', '<U30')])
        #xyz = np.array(([xFull, yFull, zFull]), dtype=dtype).transpose()
        #xyzn = np.c_[xyz, nameFull]
        xyzn = df


        return xyzn

def verticalObsWithinForestGenerator_multiPoints(inPoints, multiPoints, resolution = 10):
    if len(multiPoints[0]) == 4:
        import pandas as pd
        #dtype = np.dtype([('x', np.float32), ('y', np.float32), ('z', np.float32), ('NAME', np.str_, 30)])

        #b = np.array([(0, 0, 0, 'name'), (0, 0, 0, 'name'), (0, 0, 0, 'name')], dtype=dtype)

        #b = pd.DataFrame([(0,0,0,'c'),(0,0,0,'c')],columns=('x', 'y', 'z', 'Name'))
        b = pd.DataFrame(columns=('x', 'y', 'z', 'Name'))
        for index in range(len(multiPoints)):

            a = fp.Tools.verticalObsWithinForestGenerator(inPoints, multiPoints[index], resolution=resolution)

            b = pd.concat([b, a])



    else:
        b = np.array([(0., 0., 0.), (0., 0., 0.), (0., 0., 0.)])

        for index in range(len(multiPoints)):
            a = fp.Tools.verticalObsWithinForestGenerator(inPoints, multiPoints[index], resolution=resolution)
            b = np.r_[b, a]

        b = np.delete(b, [0, 1], axis=0)

    return b

def get_RandomPointsWithinGivenPointCloud(inAllPoints, Num):
    Xmax, Xmin = np.max(inAllPoints[:, 0]), np.min(inAllPoints[:, 0])
    Ymax, Ymin = np.max(inAllPoints[:, 1]), np.min(inAllPoints[:, 1])
    Zmax, Zmin = np.max(inAllPoints[:, 2]), np.min(inAllPoints[:, 2])

    X_sequence = np.random.uniform(Xmax, Xmin, Num)
    Y_sequence = np.random.uniform(Ymax, Ymin, Num)
    Z_sequence = np.random.uniform(Zmax, Zmin, Num)

    XYZ_random = np.vstack((X_sequence, Y_sequence, Z_sequence)).transpose()

    return XYZ_random

def get_UniformPointsWithinGivenPointCloud(inAllPoints, resolution):


    Xv, Yv, Zv = inAllPoints[:, 0], inAllPoints[:, 1], inAllPoints[:, 2]

    minX, maxX = np.min(Xv), np.max(Xv)
    minY, maxY = np.min(Yv), np.max(Yv)
    minZ, maxZ = np.min(Zv), np.max(Zv)

    xZoneR = np.arange(minX, maxX + resolution, resolution)
    yZoneR = np.arange(minY, maxY + resolution, resolution)
    zZoneR = np.arange(minZ, maxZ + resolution, resolution)

    grided = np.meshgrid(xZoneR, yZoneR, zZoneR)

    x = grided[0]
    y = grided[1]
    z = grided[2]
    n = []
    for i in zip(x.flat, y.flat, z.flat):
        n.append(i)

    return n

def get_UniformPointsWithinGivenPointCloud_voxels(inAllPoints, resolution):
    inAllPoints_vd = fp.Tools.voxelDownsampling(inAllPoints, resolution)
    return inAllPoints_vd

def judge_IfPointIsInsideTheForest(givenPoint, method = 'points', AP = None, DSM = None, DEM = None):
    #This function is used to judge if one given point is inside forest.
    #parameter:
    #+inPoint: Import the coordinate (xyz) of one given point

    #Return: A one-dimension array constructed by one bool

    inPoint = np.array((givenPoint))

    #if len(inPoint.shape) == 1:
    inPoint_X = inPoint[0]
    inPoint_Y = inPoint[1]
    inPoint_Z = inPoint[2]

    if method == 'points':
        if AP is None:
            raise OSError('Point clouds are required as reference data.')
        else:
            try:
                extratPoints = fp.Tools.extractByOnePoints(AP,
                                                           centerP=[inPoint_X, inPoint_Y, inPoint_Z],
                                                           radius=2)
                minZ_extracted = np.min(extratPoints[:, 2])
                maxZ_extracted = np.max(extratPoints[:, 2])

                if inPoint_Z >= minZ_extracted and inPoint_Z <= maxZ_extracted:
                    return True
                else: return False
            except Exception as e:
                pass


    elif method == 'raster':
        if DEM is None or DEM is None:
            raise OSError('Both of DSM and DEM are required as reference data.')
        else:
            DEM_matrix = fp.dataManagement.getRasterMatrix(DEM)
            DSM_matrix = fp.dataManagement.getRasterMatrix(DSM)

            ExtractValue_DSM = get_ValueByGivenPointOnRasterMatrix([inPoint_X, inPoint_Y], DSM_matrix)
            ExtractValue_DEM = get_ValueByGivenPointOnRasterMatrix([inPoint_X, inPoint_Y], DEM_matrix)

            if inPoint_Z >= ExtractValue_DEM and inPoint_Z <= ExtractValue_DSM:
                return True
            else: return False

    #elif len(inPoint.shape) != 2: raise OSError('This function can only judge one point!')


def get_ValueByGivenPointOnRasterMatrix(xy, raster):
    # This function is used to get a value by given point xy coordinate.
    # parameter:
    # +xy: Import the xy coordinate of given point
    # +raster: Import the raster which want to query

    # Return: A value in the raster where the given point is.

    x = xy[0]
    y = xy[1]

    raster_cor_x = raster['x']
    raster_cor_y = raster['y']

    x_diff = np.array(raster_cor_x - x)
    y_diff = np.array(raster_cor_y - y)

    x_index = raster_cor_x[np.argmin(np.abs(x_diff))]
    y_index = raster_cor_y[np.argmin(np.abs(y_diff))]

    value = raster.sel(x = x_index, y = y_index)

    return value.data

def get_VerticalObsBasedOnPoints():

    return




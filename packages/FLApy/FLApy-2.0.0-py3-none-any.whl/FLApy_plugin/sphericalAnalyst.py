import numpy as np
import os
import pyvista as pv
import healpy as hp
import matplotlib.pyplot as plt


class sphAna(object):

    def __init__(self, inSFL = None,nsideset = None, pointSizeRange = (0.5,7), numAziRing = 360):

        if inSFL is None:
            raise ValueError('Please input a SFL data container!')

        elif inSFL is not None and os.path.isfile(inSFL) is True:
            self._DataContainer = pv.read(inSFL)
            self.tempSFL = str(self._DataContainer.field_data['temPath'][0])

        elif inSFL is not None and os.path.isfile(inSFL) is False:
            self._DataContainer = inSFL._SFL
            self.tempSFL = str(self._DataContainer.field_data['temPath'][0])

        self.nsideSet = int(nsideset)
        self.inAP       = self._DataContainer.field_data['PTS']
        self.inTP       = np.concatenate((self._DataContainer.field_data['DEM'], self._DataContainer.field_data['DTM']), axis=0)
        self._obsSet_VSA      = self._DataContainer.field_data['OBS_SFL']
        self.pointSizeMin = pointSizeRange[0]
        self.pointSizeDelta = pointSizeRange[1]
        self.numAziRing = numAziRing
        self.obscuredValue = 0

        obsXcenter = np.mean(self._obsSet_VSA[:, 0])
        obsYcenter = np.mean(self._obsSet_VSA[:, 1])
        obsZcenter = np.mean(self._obsSet_VSA[:, 2])
        obsCenter = np.array([obsXcenter, obsYcenter, obsZcenter])
        self.centerTerrainDrawed_VSA = self.draw_Terrain(self.inTP, obsCenter)

    def draw_Vegtation(self, inPoints, obsIn):
        # Draw the vegetation map based on the input points and the observation points.
        # Parameters:
        #   inPoints: The input points, which is a numpy array with shape (n, 3).
        #   obsIn: The observation points, which is a numpy array with shape (1, 3).
        #   pointSizeRangeSet: The range of the point size, which is a tuple with two elements.
        # Return:
        #   veg_baseMap: The vegetation obscured map, which is a numpy array with shape (n, 1).

        # 1. Create a base spherical map.
        self.veg_baseMap = np.ones(hp.nside2npix(self.nsideSet))

        # 2. Convert the input points to the relative coordinate system for the observation points.
        veg_CBOed = inPoints - obsIn

        # 3. Convert the relative coordinate system (Cartesion) to the spherical coordinate system.
        _, veg2sph_theta, veg2sph_phi = self.cart2sph(veg_CBOed[:, 0], veg_CBOed[:, 1], veg_CBOed[:, 2])
        veg2sph_r = np.ones(len(veg2sph_theta))

        # 4. Calculate the distance between the observation points and the input points.
        distanceLabel = self.cal_pointSize(SizeMin=self.pointSizeMin, delta=self.pointSizeDelta,
                                           inAllPointsCBO=veg_CBOed)

        # 5. Convert the spherical coordinate system to the vector.
        discCenterArray_VEC = hp.ang2vec(theta=veg2sph_theta, phi=veg2sph_phi)

        # 6. Calculate the pixels that are obscured by the vegetation.
        for indexAllMapWithPointSize_Veg in range(len(distanceLabel)):
            ipix_withPointsSize_Veg = hp.query_disc(nside=self.nsideSet,
                                                    vec=discCenterArray_VEC[indexAllMapWithPointSize_Veg],
                                                    radius=np.radians(distanceLabel[indexAllMapWithPointSize_Veg]),
                                                    inclusive=False)
            self.veg_baseMap[ipix_withPointsSize_Veg] = self.obscuredValue

        return self.veg_baseMap

    def draw_Terrain(self,inPoints, obsIn):
        # Draw the terrain map based on the input points and the observation points.
        # Parameters:
        #   inPoints: The input terrain points, which is a numpy array with shape (n, 3).
        #   obsIn: The observation points, which is a numpy array with shape (1, 3).
        # Return:
        #   ter_baseMap: The terrain obscured map, which is a numpy array with shape (n, 1).

        # 1. Create a base spherical map.
        self.ter_baseMap = np.ones(hp.nside2npix(self.nsideSet))

        # 2. Convert the input terrain points to the relative coordinate system for the observation points.
        ter_CBOed = inPoints - obsIn

        # 3. Convert the relative coordinate system (Cartesion) to the spherical coordinate system.
        _, ter2sph_theta, ter2sph_phi = self.cart2sph(ter_CBOed[:, 0], ter_CBOed[:, 1], ter_CBOed[:, 2])

        # 4. Convert the spherical coordinate system to the vector.
        discCenterArray_VEC = hp.ang2vec(theta=ter2sph_theta, phi=ter2sph_phi)

        # 5. Estimate the width of one pixel in the virtual sphere. And calculate the center point coordinates  of each pixel.
        healpixCenterPoints_C2Sed = self.healpixCenterPointsGenerator(self.nsideSet)

        # 6. Draw the terrain map. Traverse all the azimuth sub-zones. For each sub-zone, judge whether the center point of the pixel is under the ground.
        keptCorPointsStorage = np.array(((0., 0., 0.), (0., 0., 0.)))
        for index_JUT in range(self.numAziRing):
            aziRingMin = np.min(healpixCenterPoints_C2Sed[:, 1]) + index_JUT * np.radians(360 / self.numAziRing)
            aziRingMax = np.min(healpixCenterPoints_C2Sed[:, 1]) + (index_JUT + 2) * np.radians(360 / self.numAziRing)

            judgement_ar_TP = np.logical_and(ter2sph_phi <= aziRingMax, ter2sph_phi > aziRingMin)
            judgement_ar_CP = np.logical_and(healpixCenterPoints_C2Sed[:, 1] <= aziRingMax, healpixCenterPoints_C2Sed[:, 1] > aziRingMin)

            thetaKept_inar = ter2sph_theta[judgement_ar_TP]

            if len(thetaKept_inar) == 0:
                aLoop = 1
                while len(thetaKept_inar) == 0:
                    aziRingMin = aziRingMin
                    aziRingMax = np.min(healpixCenterPoints_C2Sed[:, 1]) + (index_JUT + 2 + aLoop) * np.radians(360 / self.numAziRing)

                    judgement_ar_loop = np.logical_and(ter2sph_phi <= aziRingMax, ter2sph_phi > aziRingMin)

                    thetaKept_inar = ter2sph_theta[judgement_ar_loop]
                    aLoop = aLoop + 1

                thetaKept_inar_min = np.min(thetaKept_inar)
            else:

                thetaKept_inar_min = np.min(thetaKept_inar)



            CP_kept_inar = healpixCenterPoints_C2Sed[judgement_ar_CP]

            thetaKeptCP_inar = CP_kept_inar[:, 0]

            CP_kept_inar_thetaFilter = CP_kept_inar[thetaKeptCP_inar >= thetaKept_inar_min]

            keptCorPointsStorage = np.r_[keptCorPointsStorage, CP_kept_inar_thetaFilter]

        keptCorPointsStorage = np.delete(keptCorPointsStorage, [0, 1], axis=0)

        theta_keptCorPointsStorage = keptCorPointsStorage[:, 0]
        phi_keptCorPointsStorage = keptCorPointsStorage[:, 1]

        underGroundPix = hp.ang2pix(nside=self.nsideSet, theta=theta_keptCorPointsStorage, phi=phi_keptCorPointsStorage)

        self.ter_baseMap[underGroundPix] = self.obscuredValue

        return self.ter_baseMap


    def cal_pointSize(self, SizeMin, delta, inAllPointsCBO):
        # Calculate the point size of the input points. Based on the distance between the observation points and the input points.
        # Parameters:
        #   SizeMin: The minimum point size.
        #   delta: The range of the point size.
        #   inAllPointsCBO: The input points in the relative coordinate system for the observation points.
        # Return:
        #   r: The point size of the input points.

        rmin = SizeMin
        rmax = rmin + delta
        distance = np.sqrt(np.sum(inAllPointsCBO ** 2, axis=1))
        Dmin, Dmax = np.min(distance), np.max(distance)
        position = (distance - Dmin) / (Dmax - Dmin)
        r = ((1 - position) * (rmax - rmin)) + rmin

        return r


    @staticmethod
    def healpixCenterPointsGenerator(nside):
        healpixIndex = np.arange(hp.nside2npix(nside))
        allHealpixCP = hp.pix2ang(nside=nside, ipix=healpixIndex)
        allHealpixCP_theta = allHealpixCP[0]
        allHealpixCP_phi = allHealpixCP[1]
        allHealpixCP_phi_adjusted = np.where(allHealpixCP_phi > np.pi, allHealpixCP_phi - 2 * np.pi, allHealpixCP_phi)

        r = np.ones(len(allHealpixCP_theta))
        return np.vstack((allHealpixCP_theta, allHealpixCP_phi_adjusted, r)).transpose()


    def com_oneObs(self, index):
        obsIn = self._obsSet_VSA[index]
        vegMap = self.draw_Vegtation(self.inAP, obsIn)
        terMap = self.draw_Terrain(self.inTP, obsIn)

        self.mergeMap = vegMap + terMap
        self.mergeMap[self.mergeMap == 2] = 1
        return self.mergeMap


    def compute_Batch(self, save = None, multiPro = 'p_map', CPU_count = None):
        if CPU_count is None:
            numCPU = os.cpu_count() - 1
        else:
            numCPU = int(CPU_count)

        obsIdx = np.arange(len(self._obsSet_VSA))

        if multiPro == 'p_map':
            from p_tqdm import p_map
            result = p_map(self.com_oneObs, obsIdx, num_cpus=numCPU, desc='Calculating...', ncols=100)
        elif multiPro == 'joblib':
            from joblib import Parallel, delayed
            result = Parallel(n_jobs=numCPU, verbose=100)(delayed(self.com_oneObs)(i) for i in obsIdx)

        SVFCell = np.array(result)

        self._DataContainer.field_data['SVF'] = SVFCell

        if save is None:
            self._DataContainer.save(self.tempSFL)
        elif save is not None:
            self._DataContainer.save(save)


    def cart2sph(self, x, y, z):
        # Convert Cartesian coordinates (x, y, z) to spherical coordinates (theta, phi, r).
        # Parameters:
        #   x: the x coordinate of the point in a Cartesian coordinate system.
        #   y: the y coordinate of the point in a Cartesian coordinate system.
        #   z: the z coordinate of the point in a Cartesian coordinate system.
        # Return:
        #   theta: the zenith angle of the point in a spherical coordinate system.
        #   phi: the azimuth of the point in a spherical coordinate system.
        #   r: the radius of the point in a spherical coordinate system.

        coords = np.vstack((x, y, z)).transpose()
        r = np.sqrt(np.sum((coords) ** 2, axis=1))
        theta = np.arccos(z / (r))
        phi = np.arctan2(y, x)
        #r = self._mapRadius*np.ones(len(phi))
        return r, theta, phi

def visSphereMap(inMap, method = 'Orthographic'):
    if method == 'Mollweide':
        return hp.mollview(inMap)
    elif method == 'Gnomonic':
        return hp.gnomview(inMap)
    elif method == 'Orthographic':
        return hp.orthview(inMap, rot=(0, 90 , 180), half_sky= True)
        #return hp.visufunc.orthview(inMap)
    elif method == 'Cartesian':
        return hp.cartview(inMap)





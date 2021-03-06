""" Utility functions for run.py """

import sys
import os
import shutil
import subprocess

sys.path.append('../..')
import prepLib

def cleanup(dicSetting):
    """ Cleanup leftovers from previous run, if any.
    Args:
        dicSetting: settings dictionary which contains necessary directories
    """

    if os.path.exists(dicSetting['strDirPrepDataTmp']):
        shutil.rmtree(dicSetting['strDirPrepDataTmp'])

    if os.path.exists(dicSetting['strDirSparseData']):
        shutil.rmtree(dicSetting['strDirSparseData'])

    os.mkdir(dicSetting['strDirSparseData'])


def prepData(dicSetting):
    """ Create data in format needed for training SparseBlock NN.abs
    Args:
        dicSetting: dictionary containing necessary paths.
    Returns:
        number of training records.
    """

    protDic, pepDic = prepLib.loadProtPeptideDic(dicSetting['strFilePathIdentification'])
    prepLib.breakFasta(dicSetting['strFastaDB'],
                       dicSetting['strDirPrepDataTmp'], 
                       protDic)
    listProtRefFileName = prepLib.getProtRefFileNames(
        dicSetting['strDirPrepDataTmp'])

    # match peptides with proteins
    prepLib.searchAll(
        listProtRefFileName, dicSetting['strDirPrepDataTmp'], dicSetting['strDirSparseData'], protDic)

    strMetaInfoFilename = '{!s}/metaInfo.csv'.format(
        dicSetting['strDirSparseData'])
    prepLib.saveMetaInfo(
        dicSetting['strDirSparseData'], strMetaInfoFilename, dicSetting['strDirPrepDataTmp'])

    # it is necessary to sort as sparse info saved into protein files assume
    # targets are sorted according to peptide id.
    pepProbsList = sorted(list(pepDic.values()), key=lambda x: x[0])
    pepProbsList = [pepProbsList[i][1:3] for i in range(0, len(pepProbsList))]
    prepLib.savePepProbsTargetFromList(
        '{!s}/target.csv'.format(dicSetting['strDirSparseData']), pepProbsList)
    
    return len(pepProbsList)

def updateTrainPredSettings(dicSetting):
    """ Update settings in trainPredSetting.csv with dicSettings
    Args:
        dicSettings
    Returns:
        path to the generated .csv file
    """

    strFilePath = '{:s}/trainPredSetting.csv'.format(dicSetting['strDatasetDir'])
    with open(strFilePath, 'w') as bfFile:
        bfFile.write('strBaseDir,{:s}\n'.format(dicSetting['strDirSparseData']))
        bfFile.write('strFilenameTarget,{:s}/target.csv\n'.format(dicSetting['strDirSparseData']))
        bfFile.write('strFilenameMetaInfo,{:s}/metaInfo.csv\n'.format(dicSetting['strDirSparseData']))
        bfFile.write('strFilenameProtInfo,{:s}\n'.format(dicSetting['strFilePathPredOutput']))
        bfFile.write('strFilenameExprDescription,{:s}.desc\n'.format(dicSetting['strFilePathPredOutput']))
        bfFile.write('strFilenameExprParams,{:s}.params\n'.format(dicSetting['strFilePathPredOutput']))
        bfFile.write('nRows,{:d}\n'.format(dicSetting['nRows']))
        
        for strKey, value in dicSetting['dicTrainPredArgs'].items():
            bfFile.write('{:s},{:s}\n'.format(strKey, str(value)))
        
        return strFilePath

def trainPred(dicSetting):
    """ Run trainPred.lua
    Args:
        dicSetting
    """

    strFilePathTrainPred = updateTrainPredSettings(dicSetting)
    strCommand = "th trainPred.lua {:s}".format(strFilePathTrainPred)
    print("Run:{:s}".format(strCommand))
    subprocess.call([strCommand], shell=True)

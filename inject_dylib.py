#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zipfile
import subprocess
import os.path
import os
import shutil
import time

#拷贝文件并且修改依赖
def copyandmodifydepend(originpath,substratePath,injectDylibPath,insertToolPath):
	dependPathPrefix = '@executable_path%sFrameworks' % os.sep
	for dirpath, dirnames, filenames in os.walk(originpath):
		if dirpath[dirpath.rfind('.'):] == '.app':
			executableName = dirpath[dirpath.rfind(os.sep)+1:dirpath.rfind('.')]
			executablePath = '%s%s%s' % (dirpath,os.sep,executableName)
			for dirname in dirnames:
				if 'Frameworks' in dirname:
					#拷贝待注入dylib和libstrate.dylib到Frameworks目录
					frameworksPath = '%s%s%s' % (dirpath,os.sep,dirname)
					copySubstratePath = '%s%s' % (frameworksPath,substratePath[substratePath.rfind(os.sep):])
					copyInjectPath = '%s%s' % (frameworksPath,injectDylibPath[injectDylibPath.rfind(os.sep):])
					shutil.copy(substratePath,copySubstratePath)
					shutil.copy(injectDylibPath,copyInjectPath)
					#修改注入dylib的依赖
					(status, output) = subprocess.getstatusoutput('install_name_tool -change /Library/Frameworks/CydiaSubstrate.framework/CydiaSubstrate %s%s %s' % (dependPathPrefix,substratePath[substratePath.rfind(os.sep):],copySubstratePath))
					if status != 0:
						print('install_name_tool execute failed!')
						return False
					else:
						print('install_name_tool execute successed!')
					break;
			insertCmd = '%s %s%s %s --no-strip-codesig --all-yes' % (insertToolPath,dependPathPrefix,injectDylibPath[injectDylibPath.rfind(os.sep):],executablePath)
			(status, output) = subprocess.getstatusoutput(insertCmd)
			if status != 0 :
				print('insert_dylib execute failed!')
				return False
			else:
				print('insert_dylib execute successed!')
				#修改xxx_patched为xxx
				(status, output) = subprocess.getstatusoutput('mv -f %s %s' % (executablePath+'_patched',executablePath))
				if status != 0:
					print('remove command execute failed!')
					return False
				else:
					print('remove command execute successed!')
			break;
	return True

#打包成ipa
def package(originpath,destinationpath):
	for dirpath, dirnames, filenames in os.walk(originpath):
		if dirpath[dirpath.rfind('.'):] == '.app':
			(status,output) = subprocess.getstatusoutput('xcrun -sdk iphoneos PackageApplication -v %s -o %s' % (os.path.join(originpath,dirpath),destinationpath))
			return status == 0

def main():
	#准备参数
	zipFilePath = input('请拖拽ipa到此：').strip()
	if not os.path.isfile(zipFilePath):
		print('ipa路径不正确，请仔细检查！')
		sys.exit(0)
	substratePath = input('请拖拽libsubstrate.dylib到此：').strip()
	if not os.path.isfile(substratePath):
		print('libsubstrate.dylib路径不正确，请仔细检查！')
		sys.exit(0)
	injectDylibPath = input('请拖拽待注入的dylib到此：').strip()
	if not os.path.isfile(injectDylibPath):
		print('待注入的dylib路径不正确，请仔细检查！')
		sys.exit(0)
	insertToolPath = input('请拖拽Insert_Dylib到此：').strip()
	if not os.path.isfile(insertToolPath):
		print('Insert_Dylib路径不正确，请仔细检查！')
		sys.exit(0)

	homedir = os.environ['HOME']
	extrapath = '%s/Payload_temp_%s/' % (homedir,str(time.time()))

	outputPath = zipFilePath[:zipFilePath.rfind('.')] + '_rejected.ipa'

	originzfile = zipfile.ZipFile(zipFilePath,'r')

	#解压到临时目录
	originzfile.extractall(extrapath)

	try:
		#拷贝文件并且修改依赖
		print('开始注入dylib...')
		if not copyandmodifydepend(extrapath,substratePath,injectDylibPath,insertToolPath):
			print('注入dylib失败，请重试！')
		else:
			print('注入dylib成功！')
			#打包ipa
			print('开始打包ipa...')
			if not package(extrapath,outputPath):
				print('打包ipa失败!')
			else:
				print('打包ipa成功!')
				print('注入成功，请查看：'+outputPath)
	finally:
		#关闭zipfile
		originzfile.close()
		#删除临时解压目录
		shutil.rmtree(extrapath)

if __name__ == '__main__':
	main()
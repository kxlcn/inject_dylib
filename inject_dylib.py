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
						print('install_name_tool execute failed!' + output)
						exit(0)
					else:
						print('install_name_tool execute successed!')
					break;
			insertCmd = '%s %s%s %s --all-yes' % (insertToolPath,dependPathPrefix,injectDylibPath[injectDylibPath.rfind(os.sep):],executablePath)
			print(insertCmd)
			(status, output) = subprocess.getstatusoutput(insertCmd)
			if status != 0 :
				print('insert_dylib execute failed!')
				exit(0)
			else:
				print('insert_dylib execute successed!')
				#修改xxx_patched为xxx
				(status, output) = subprocess.getstatusoutput('mv -f %s %s' % (executablePath+'_patched',executablePath))
				if (status != 0):
					print('remove command execute failed!')
				else:
					print('remove command execute successed!')
			break;

#zip压缩
def zipcompress(originpath,destinationzfile):
	resignedzfile = zipfile.ZipFile(destinationzfile,'w',zipfile.ZIP_DEFLATED)
	for dirpath, dirnames, filenames in os.walk(originpath):
		fpath = dirpath.replace(originpath,'')
		fpath = fpath and fpath + os.sep or ''
		for filename in filenames:
			resignedzfile.write(os.path.join(dirpath, filename), fpath+filename)
	resignedzfile.close()

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
	zfilelist = originzfile.namelist()
	zfilelist.reverse()

	#解压到临时目录
	originzfile.extractall(extrapath)

	try:
		#拷贝文件并且修改依赖
		print('开始注入...')
		copyandmodifydepend(extrapath,substratePath,injectDylibPath,insertToolPath)
		#压缩
		print('开始压缩文件...')
		zipcompress(extrapath,outputPath)
		print('注入成功，请查看：'+outputPath)
	finally:
		#关闭zipfile
		originzfile.close()
		#删除临时解压目录
		shutil.rmtree(extrapath)

if __name__ == '__main__':
	main()
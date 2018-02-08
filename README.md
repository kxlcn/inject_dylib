# inject_dylib
向ipa注入dylib，并同时修改dylib对substrate依赖

# 使用演示
![inject](https://github.com/kevll/inject_dylib/blob/master/screenshots/inject.gif)

# 依赖环境
1.因新版Xcode已废弃PackageApplication，所以请先确保安装PackageApplication环境，可参考[没有PackageApplication指令的解决方法](http://blog.csdn.net/zhuzhiqiang_zhu/article/details/70210794) </br>
2.请先下载[insert_dylib](https://github.com/Tyilo/insert_dylib)，或者使用直接使用仓库的insert_dylib</br>
3.越狱设备提取libsubstrate.dylib，或者直接使用仓库的libsubstrate.dylib

# 使用方法
1.下载[inject_dylib.tar.gz](https://github.com/kevll/inject_dylib/releases/download/0.0.1/inject_dylib.tar.gz)，解压缩得到inject_dylib</br>
2.双击运行inject_dylib，依次拖拽源ipa、libsubstrate.dylib、xxx.dylib、insert_dylib到终端</br>
3.在源ipa目录会生成xxx_injected.ipa文件，即被注入dylib的ipa文件。

# 注意事项
1.注意生成的xxx_injected.ipa还未签名，请使用[resign](https://github.com/kevll/resign)自行签名，或者使用[impactor](http://www.cydiaimpactor.com/)自动签名。签名后即可通过XX助手或者Xcode安装(impactor暂时不支持签名包含Watchs的ipa)</br>
2.源ipa可以直接从XX助手下载越狱版ipa即可使用，或者自行砸壳。

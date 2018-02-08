# inject_dylib
向ipa注入dylib，并同时修改dylib对substrate依赖

# 依赖环境
1.因新版Xcode已废弃PackageApplication，所以请先确保安装PackageApplication环境，可参考["没有PackageApplication指令的解决方法"](http://blog.csdn.net/zhuzhiqiang_zhu/article/details/70210794)
2.请先下载(insert_dylib)[https://github.com/Tyilo/insert_dylib]

# 使用方法
1.下载inject_dylib
2.双击运行，依次拖拽源ipa、libsubstrate.dylib、xxx.dylib、insert_dylib到终端
3.在源ipa目录会生成xxx_injected.ipa文件(注意此ipa还未签名，请使用[resign](https://github.com/kevll/resign)自行签名，或者使用[impactor](http://www.cydiaimpactor.com/)自动签名。签名后即可通过XX助手或者Xcode安装)

# 使用演示
[inject](https://github.com/kevll/inject_dylib/blob/master/screenshots/inject.gif)

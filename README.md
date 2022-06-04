# MailPush
For English users, there is a nice [post](https://www.reddit.com/r/kindle/comments/uvp41l/howto_email_kfx_books_from_calibre_to_a/).  

这是个Kindle的`KUAL`插件，实现了邮箱推送功能，类似于亚马逊的`Send-to-Kindle`，但是并不依赖于在亚马逊官方注册的Kindle邮箱，可以使用任何邮箱。在使用本插件前请确保你已经把设备越狱而且安装了[`KUAL`和`Python3`](https://www.mobileread.com/forums/showthread.php?t=225030)。当然，由于本插件主体基于`Python3`的标准库完成，因此`src`文件夹里的程序实际上是跨平台的，可以运行于任何安装了`Python3`的操作系统和平台。
## 特点
* 支持通过邮件附件推送文件
* 支持通过在邮件里填写文件下载链接推送文件。这有时更方便而且可以突破邮箱的文件大小的限制
* 支持以压缩包的方式推送，插件会自动完成解压，支持zip, tar, gztar, bztar等格式
* 支持在邮件中指定文件要保存的路径或文件名
* 不同于亚马逊官方服务，我们没有“已认可的发件人”或其它白名单的概念，任何邮箱都可以向你推送文件
* 不同于亚马逊官方服务，我们支持推送任意格式的文件到任意目录（不限于图书），插件不会进行检测，除了压缩包解压也不会进行任何格式转换  

这里可能会有一些安全隐患（例如可以通过这种方法推送固件升级的文件），所以你最好申请一个名称相对复杂的邮箱并且不要公开。另外，你可以在`config.json`文件中为`root`设置一个更严格的路径，邮件推送的文件将不允许下载到`root`目录及其子目录之外的地方。`root`默认为Kindle USB磁盘根目录（/mnt/us/），请谨慎修改。
## 安装和配置
1. 注册一个新邮箱账户并根据你邮箱服务商的要求在邮箱管理页面开启`IMAP`服务。不同邮箱的方法不同，如outlook邮箱默认开启IMAP服务，无需进一步设置；而新注册的QQ邮箱则需要14天后才能开启IMAP服务
2. 某些邮箱（例如Yahoo、Google、QQ）需要你创建专门的应用程序密码（授权码），使用常规密码将登录失败，插件将无法正常工作
3. `git clone`本项目或前往[发布页面](https://github.com/guo-yong-zhi/MailPush/releases)下载压缩包并解压到你电脑的任意目录下
4. 在`MailPush/src`文件夹里找到并编辑`config.json`文件
   * 将`user`改为刚刚申请的新邮箱
   * 将`password`改为登录密码（也可能是IMAP授权码）。因为是明文存储，请注意安全
   * 将`host`、`port`改为你邮箱服务商的IMAP host和port。可以参考文末的对照表
   * 其它参数按需修改。`downloaddir`为默认下载路径；`maxage`为下载几天内的邮件；`maxnum`为一次最多下载几封邮件
5. 通过USB把`MailPush`文件夹拷贝到你Kindle设备根目录下的`extensions`目录中
## 使用方法
1. 用其它邮箱向你填在`user`的邮箱发邮件
   * 可以选择添加任意附件
   * 主题或正文都可以为空
   * 主题或正文的一行可以是文件下载链接，多个链接可用空格或`|`隔开，或者分别用`<`和`>`框住，但不支持逗号或分号分隔。当然，多个链接也可以直接写到多行。
   * 主题或正文的一行可以以`saveto`关键字开头，用于指定下载到Kindle中的路径或文件名，多个文件名用`|`隔开，或者分别用`<`和`>`框住，不可以用空格分隔。当然，多个文件名也可以直接写到多行。缺省路径通过参数`downloaddir`配置，默认是`/mnt/us/documents/downloads`。格式如：
      > * `saveto abc.pdf` #意为第一个文件保存到 /mnt/us/documents/downloads/abc.pdf
      > * `saveto books/` #意为第一个文件保存到 /mnt/us/documents/downloads/books/ 中，文件名不变
      > * `saveto /mnt/us/123.epub` #意为第一个文件保存到 /mnt/us/123.epub
      > * `saveto abc.pdf | ../def.pdf` #意为前两个文件分别保存到 /mnt/us/documents/downloads/abc.pdf 和 /mnt/us/documents/def.pdf
2. 在Kindle上打开KUAL，在菜单中找到`MailPush`。点击`Fetch unseen mails`系列可以获取未读，或点击`Fetch the latest mails`系列可以获取最新邮件中的文件。
## 故障排除
1. 运行日志保存在Kindle磁盘根目录下`extensions/MailPush/`中的`log.txt`和`result.txt`，可以通过USB连接电脑查看。如果装有插件`Leafpad`，也可以直接在Kindle上通过KUAL菜单按钮打开查看。
2. 如果提示`Operation failed`，请先检查`log.txt`中的内容。检查`Python3`的安装状态及`config.json`中的配置（如`password`）
3. 如果屏幕上方长时间跳动`Fetching...`或提示`Time out`，则可能是网络问题，如果你使用的是国外邮箱服务，可以尝试换用国内的
4. 如果提示`Operation success`却找不到文件，请先检查`result.txt`中的文件路径，如果没有任何下载则可以点击`Fetch junk mails`系列，尝试在垃圾邮件中寻找
## 附：常见邮箱类型和host对照表
|邮箱类型|host|port|
|----|----|----|
|gmail|imap.gmail.com|993|
|yahoo|imap.mail.yahoo.com|993|
|outlook|imap-mail.outlook.com|993|
|hotmail|outlook.office365.com|993|
|qq|imap.qq.com|993|
|126|imap.126.com|993|
|163|imap.163.com|993|
|yeah|imap.yeah.net|993|
|sina|imap.sina.com|993|
## 我的更多Kindle插件
* [**kindle-filebrowser**](https://github.com/guo-yong-zhi/kindle-filebrowser) 网页文件管理器 
* [**MailPush**](https://github.com/guo-yong-zhi/MailPush) 使用第三方邮箱推送文件
* [**BlockKindleOTA**](https://github.com/guo-yong-zhi/BlockKindleOTA) 阻止Kindle升级
* [**KOSSH**](https://github.com/guo-yong-zhi/KOSSH) WiFi连接的轻量ssh服务器
* [**ShuffleSS**](https://github.com/guo-yong-zhi/ShuffleSS) 打乱锁屏图片顺序

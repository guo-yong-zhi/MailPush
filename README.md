# MailPush
这是个Kindle的`KUAL`插件，实现了邮箱推送功能，类似于亚马逊的`Send-to-Kindle`，但是并不依赖于在亚马逊官方注册的Kindle邮箱，可以使用任何邮箱。在使用本插件前请确保你已经把设备越狱而且安装了`KUAL`和`Python3`。当然，由于本插件主体基于`Python3`的标准库完成，因此`src`文件夹里的程序实际上是跨平台的，可以运行于任何安装了`Python3`的操作系统和平台。
## 特点
* 支持通过邮件附件推送文件
* 支持通过在邮件里填写文件下载链接推送文件。这有时更方便而且可以突破邮箱的文件大小的限制
* 支持以压缩包的方式推送，插件会自动完成解压，支持zip, tar, gztar, bztar等格式
* 支持在邮件中指定文件要保存的路径或文件名
* 不同于亚马逊官方服务，我们没有“已认可的发件人”或其它白名单的概念，任何邮箱都可以向你推送文件
* 不同于亚马逊官方服务，我们支持推送任意格式的文件到任意目录（不限于图书），插件不会进行检测，除了压缩包解压也不会进行任何格式转换  

这里可能会有一些安全隐患，所以你最好申请一个名称相对复杂的邮箱而且不要把它告诉太多人。另外，可以在`config.json`文件中为`root`设置一个更严格的路径，邮件推送的文件将不允许下载到`root`目录及其子目录之外的地方。`root`默认为Kindle USB磁盘根目录（/mnt/us/），请谨慎修改。
## 安装
1. 前往[发布页面](https://github.com/guo-yong-zhi/MailPush/releases)下载压缩包，并解压到你电脑的任意目录下
2. 在解压目录中`MailPush/src`文件夹里找到`config.json`文件并编辑
   * 将`user`改为你自己的邮箱。建议为此单独申请一个邮箱，不要混用
   * 将`password`改为你的邮箱密码。因为是明文存储，注意不要泄漏这个文件给他人
   * 将`host`、`port`改为你邮箱服务商的IMAP host和prot。可以参考文末的对照表
   * 其它参数按需修改。`downloaddir`为默认下载路径；`maxage`为下载几天内的邮件；`maxnum`为一次最多下载几封邮件
3. 通过USB把`MailPush`文件夹拷贝到你Kindle设备根目录下的`extensions`目录中
4. 根据你邮箱服务商的要求在邮箱管理页面打开`IMAP`服务的开关。不同邮箱方法不同，如outlook邮箱默认开启IMAP服务，所以不需要此步；而新注册的QQ邮箱需要14天后才能开启IMAP服务
## 使用方法
1. 用其它邮箱向你填在`user`的邮箱发邮件
   * 可以选择添加任何附件
   * 主题部分或正文部分的一行可以是文件下载链接，多个链接用空格或`|`隔开，或者分别用`<`和`>`框住，但不支持逗号或分号分隔
   * 主题部分或正文部分的一行可以以`saveto`关键字开头，用以指定下载到Kindle中的路径或文件名，多个文件名用`|`隔开，或者分别用`<`和`>`框住，不可以用空格分隔。缺省路径通过参数`downloaddir`配置，默认是`/mnt/us/documents/downloads`。格式如：
      > * `saveto abc.pdf` #意为第一个文件保存到 /mnt/us/documents/downloads/abc.pdf
      > * `saveto books/` #意为第一个文件保存到 /mnt/us/documents/downloads/books/ 中，文件名不变
      > * `saveto /mnt/us/123.epub` #意为第一个文件保存到 /mnt/us/123.epub
      > * `saveto abc.pdf | def.pdf` #意为前两个文件分别保存到 /mnt/us/documents/downloads/abc.pdf 和 /mnt/us/documents/downloads/def.pdf
2. 在Kindle打开KUAL，可以在菜单中找到`MailPush`。点击`Fetch unseen mails`系列可以获取未读，或点击`Fetch the latest mails`系列可以获取最新邮件中的文件。运行日志会保存在`extensions/MailPush/`中`log.txt`和`result.txt`以供查看。如果装有插件`Leafpad`，也可以通过菜单按钮打开查看。
3. 点击下载后，如果屏幕上方长时间跳动`Fetching...`或提示了`Time out`，可能是网络不稳定的原因，如果你使用的是国外邮箱服务，可以尝试换用国内的
4. 如果操作成功却没有下载到文件，请先检查`result.txt`中是否有下载文件及路径，如果确实没有下载可以点击`Fetch unseen junk mails`或`Fetch the latest 1 junk mail`尝试在垃圾邮件中寻找
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
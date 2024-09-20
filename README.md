# MailPush
For English users, there is a [fork](https://github.com/Darthagnon/MailPush).  
для русскоязычных пользователей здесь есть [fork](https://github.com/DarkAssassinUA/MailPushRU).

这是个Kindle的`KUAL`插件，实现了邮箱推送功能，类似于亚马逊的`Send-to-Kindle`，但是并不依赖于在亚马逊官方注册的`@kindle.com`邮箱，而可以使用任意支持`IMAP`服务第三方邮箱。在使用本插件前请确保你已经把设备越狱而且安装了[`KUAL`和`Python3`](https://www.mobileread.com/forums/showthread.php?t=225030)。实际上，本插件的主体功能仅使用`Python3`的标准库完成，`src`文件夹里的程序可以运行于任何安装了`Python3`的操作系统或平台。
## 特点
* 支持通过邮件附件推送文件
* 支持通过在邮件里填写文件下载链接推送文件。这有时更方便而且可以突破邮箱的文件大小的限制
* 支持以压缩包的方式推送，插件会自动完成解压，支持zip, tar, gztar, bztar等格式
* 支持在邮件中指定文件要保存的路径或文件名
* 不同于亚马逊官方服务，我们没有“已认可的发件人”或其它白名单的概念，任何邮箱都可以向你推送文件
* 不同于亚马逊官方服务，我们支持推送任意格式的文件到任意目录（不限于图书），插件不会进行检测，除了压缩包解压也不会进行任何格式转换

这里可能会有一些安全隐患（例如可以通过这种方法推送固件升级的文件），所以你最好申请一个名称相对复杂的邮箱并且不要公开。另外，你可以在`config.json`文件中为`root`设置一个更严格的路径，邮件推送的文件将不允许下载到`root`目录及其子目录之外的地方。
## 安装和配置
1. 注册一个邮箱账户并在其设置页面开启`IMAP`服务。请不要和其他重要账户使用同一个密码，因为MailPush采用了不安全的明文存储！不同品牌的邮箱启用IMAP服务的要求和限制不同，需要仔细选择。大部分邮箱（例如Gmail、Yahoo、QQ）都需要你创建专门的应用程序密码（授权码），而不能使用常规登录密码。新注册的QQ邮箱需要14天后才能开启IMAP；163邮箱的授权码只有180天有效期，到期需要重新设置；outlook邮箱则要求特殊的验证方式，本插件暂不支持。欢迎在issue里分享你的邮箱服务商的设置方法。
2. `git clone`本项目或前往[发布页面](https://github.com/guo-yong-zhi/MailPush/releases)下载压缩包并解压到你电脑的任意目录下。最外层的文件夹可以重命名。
3. 在`MailPush/src`文件夹里找到并编辑`config.json`文件：
	* 将`user`改为刚才申请的新邮箱
	* 将`password`改为刚才创建的IMAP授权码（也可能就是常规登录密码）。注意不要泄露`config.json`文件给他人！
	* 将`host`、`port`改为你邮箱服务商的IMAP host和port。可以参考文末的对照表
	* 其它参数按需修改（可选）：
		- `downloaddir`为默认下载路径，`root`为允许写入的目录。`root`默认为Kindle USB磁盘根目录（/mnt/us/），请谨慎修改。
		- `maxage`为下载几天内的邮件，`maxnum`为一次最多下载几封邮件，`mailbox`和`criteria`是邮件类型，这些选项配置了菜单中`Fetch emails via config.json (custom)`的功能
4. 通过USB把`MailPush`文件夹复制到你Kindle设备根目录下的`extensions`目录中。
5. 安全弹出你的设备，现在可以在KUAL菜单里找到`MailPush`。
## 使用方法
1. 用其它邮箱向你填在`config.json`中的邮箱发邮件
	* 可以添加任意附件（如电子书、图片、压缩包等）
	* 主题或正文都可以为空
	* 主题或正文都可以包括多行
	* 主题或正文的一行可以是一个或多个文件下载链接，多个链接可用空格或`|`隔开，或者分别用`<`和`>`框住，注意不可以用逗号或分号分隔。
	* 主题或正文的一行可以以`saveto`关键字开头，用于指定下载到Kindle中的路径或文件名，多个文件名用`|`隔开，或者分别用`<`和`>`框住，注意不可以用空格、逗号或分号分隔。缺省路径通过参数`downloaddir`配置，默认是`/mnt/us/documents/downloads`。格式如：
		> * `saveto abc.pdf`              # 意为第一个文件保存到 /mnt/us/documents/downloads/abc.pdf
		> * `saveto books/`               # 意为第一个文件保存到 /mnt/us/documents/downloads/books/ 中，文件名不变
		> * `saveto /mnt/us/123.epub`     # 意为第一个文件保存到 /mnt/us/123.epub
		> * `saveto abc.pdf | ../def.pdf` # 意为前两个文件分别保存到 /mnt/us/documents/downloads/abc.pdf 和 /mnt/us/documents/def.pdf
	* 主题或正文中的其它内容则会被忽略
2. 在Kindle上打开KUAL，在菜单中找到`MailPush`。点击`Fetch unread emails`可以获取未读邮件中的文件，或点击`Fetch newest emails`可以获取最新邮件中的文件。
## 故障排除
1. 点击KUAL菜单按钮`View log`和`View results`可以查看运行日志和结果。也可以USB连接Kindle到电脑，查看`extensions/MailPush/`目录中的`log.txt`和`result.txt`
2. 如果在屏幕顶端看不到任何提示，或者它们显示的位置不合适，可以在电脑上修改文件`COL.txt`中的数字，例如从10改到20可以让显示更靠右。
3. 如果提示`Operation failed`，请先检查`log.txt`中的内容。检查`Python3`的安装状态及`config.json`中的配置（如`password`、`host`等）。
4. 手动登录你填在`config.json`的邮箱，检查是否收到了邮件，必要时把发送者加入白名单。注意登录查看会使得未读邮件变已读，`Fetch unread emails`会忽略这些邮件，可以点击`Fetch newest emails`来测试。
5. 设备的时钟错误可能会导致连接失败，请在Kindle设置里为其设置正确的时间。
6. 如果屏幕上方长时间跳动`Fetching...`或提示`Time out`，则可能是网络问题。可以点击`Fetch newest emails`重试。
7. 如果提示`Operation success`却找不到文件，请先依`result.txt`中的路径检查文件，如果没有任何下载则可以点击`Fetch junk mails`，尝试在垃圾邮件中寻找。
8. 如果文件已下载但没有出现在你的图书馆中，请确认文件位于`/mnt/us/documents`及其子目录中，确认文件类型（后缀名）是Kindle支持的格式。确认无误后可以尝试重启设备。

## 附：常见邮箱类型和host对照表
|邮箱类型|host|port|
|----|----|----|
|gmail|imap.gmail.com|993|
|yahoo|imap.mail.yahoo.com|993|
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

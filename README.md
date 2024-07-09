## 项目背景
##### 1. 前置项目为一个1688搜图的模块，业务通过图像搜索找到相关性较强的品，然后勾选商品，进行批量首次话术沟通，通过阿里旺旺IM工具；

##### 2. 1688-阿里旺旺群发消息接口，为该项目提供后置服务；

##### 3. Python实现发送/接收消息和添加/更新Cookie的接口；



## 编译/部署
#### 1. 通过下列命令打包镜像；
docker build -f Dockerfile.chat -t 1688-chat-service:1.0 .

#### 2. 通过以下命令启动服务；
docker run -itd -p 10019:10015 1688-chat-service:1.0 /bin/sh

#### 3. 通过以下命令查看服务是否正常；
docker logs -f container_id



## 测试
#### 1. 先增加cookie；
##### 
	METHOD: POST
##### 
	URL:http://ip:10019/aliWangWang/cookie/update/{loginAccount}
##### 
	BODY: cookie string

#### 2. 发送消息；
##### 
	METHOD: POST
##### 
	URL:http://ip:10019/aliWangWang/tx
##### BODY: 
	{
		"offerId": "679618131020",
		"chatList": [
			"你好!",
			"请问商品的价格可以便宜点吗？"
		],
		"userName": "loginAccount"
	}

#### 3. 接收消息；
##### 
	METHOD: POST
##### 
	URL:http://ip:10019/aliWangWang/rx
##### BODY: 
	{
		"offerId": "679618131020",
		"userName": "loginAccount"
	}

#### 4. 获取商品详情；
#####
	METHOD: POST
##### 
	URL:http://ip:10019/aliWangWang/getDetail
##### 
	BODY: 
	{
		"offerId": "679618131020",
		"userName": "loginAccount"
	}

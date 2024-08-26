# 一个AI问答页面项目，基于百度千帆SDK

[Access Key](https://console.bce.baidu.com/iam/#/iam/accesslist)

[SDK文档](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/7lq3ft3pb)


![image](https://github.com/user-attachments/assets/93692d91-b800-4404-ad0b-b702e730ff11)

# 环境要求
|环境|版本|
|-|-|
|python|3.7.4|
|pip|22.0.4|

## 1. 安装

百度千帆AI

<img width="400"  height="400" alt="image" src="https://user-images.githubusercontent.com/19643260/158024815-9871c401-d023-41cf-bc4e-b99445469946.png">
 
 
## 更新pip

```python
pip install --upgrade pip
```

## 创建虚拟目录

```shell
# python -m venv 虚拟环境名称，名称是随意起的
python -m venv tutorial-env
python3 -m venv tutorial-env
```

## 激活虚拟环境

* 当激活虚拟环境时命令行上会有个虚拟环境名前缀

#### Unix或MacOS上激活虚拟环境
```shell
source tutorial-env/bin/activate
```
#### windows上激活虚拟环境
```shell
tutorial-env\Scripts\activate.bat
```

### 项目依赖安装
```shell
python3.7 -m pip install --upgrade pip
pip install -r requirements.txt
```

* 如果引入其他新的依赖，可以执行冻结第三方库，就是将所有第三方库及版本号保存到requirements.txt文本文件中
```shell
pip freeze > requirements.txt
```
* 如果pip不起作用，可以从pypi上下载最新的源码包(https://pypi.python.org/pypi/)进行安装：
```shell
python setup.py install 
```



## 2. 使用


### (1)单元测试

```python
python test.py
```
```bash
    curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"message": "最近厦门天气怎么样"}'
```




### （2）运行 Flask 应用

```python
export FLASK_APP=app.py
flask run
```


# 部署

## 1. 服务器Linux CentOS 7.6

### python3.7

#### (1)安装

```shell
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
sudo tar xzf Python-3.7.9.tgz
cd Python-3.7.9
sudo ./configure --enable-optimizations
sudo make altinstall
```

#### (2)验证安装
```shell
python3.7 --version
```

#### (3)安装pip
```shell
sudo yum install python3-pip
sudo /usr/local/bin/python3.7 -m ensurepip
sudo /usr/local/bin/python3.7 -m pip install --upgrade pip
```

```shell
pip3.7 --version
```


使用 update-alternatives 来设置默认的 Python 版本
```
sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.7 1
```

然后选择默认版本：
```shell
sudo update-alternatives --config python
```


#### (4)安装依赖
```shell
python3.7 -m pip install --upgrade pip
pip install -r requirements.txt
```

#### (5)测试运行
```shell
export FLASK_APP=app.py
flask run
```


###  安装和配置 Gunicorn

Gunicorn 是一个 WSGI HTTP 服务器，可以用来**运行你的 Flask 应用**。

```shell
pip install gunicorn
# gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

创建一个 Gunicorn 服务文件 /etc/systemd/system/your_project.service，内容如下：

```shell
[Unit]
Description=Gunicorn instance to serve your_project
After=network.target

[Service]
User=your_username
Group=nginx
WorkingDirectory=/path/to/your_project
Environment="PATH=/path/to/your_project/venv/bin"
ExecStart=/path/to/your_project/venv/bin/gunicorn --workers 3 --bind unix:your_project.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

#### 启动并启用 Gunicorn 服务
```shell
sudo systemctl start your_project
sudo systemctl enable your_project
sudo systemctl status qianfan
```

### 安装和配置 Nginx

安装 Nginx 并配置它作为反向代理。


#### 源码包安装方式

```shell
wget http://nginx.org/download/nginx-1.20.1.tar.gz
tar zxvf nginx-1.20.1.tar.gz
cd nginx-1.20.1
```

配置Nginx编译选项
```shell
./configure
```

编译并安装Nginx
```shell
make
sudo make install
```

启动Nginx服务
```shell
sudo /usr/local/nginx/sbin/nginx
```

（可选）设置Nginx开机自启动：
```shell
sudo echo "/usr/local/nginx/sbin/nginx" >> /etc/rc.local
chmod +x /etc/rc.local
```


#### yum安装方式

#### 更换镜像源

```shell

# 这个已经访问不了了，我就是吃这个亏（国外的服务器还能用）
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo 
​
# 国内用下面这个
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```


```shell
sudo yum install -y nginx
```

创建一个 Nginx 配置文件 /etc/nginx/conf.d/your_project.conf，内容如下：
```shell
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /path/to/your_project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/your_project/your_project.sock;
    }
}
```

#### 重启 Nginx 服务：
```shell
sudo systemctl restart nginx
```

#### 启动并启用 Nginx
```shell
sudo systemctl start nginx
sudo systemctl enable nginx
```


#### 配置防火墙
确保防火墙允许 HTTP 和 HTTPS 流量。

```shell
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

#### 监控和日志
确保你监控你的应用并查看日志以确保一切正常运行。
```shell
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```



### 2. 部署到docker

* docker build -t baidu-ai .
* docker run -p 5000:5000 baidu-ai

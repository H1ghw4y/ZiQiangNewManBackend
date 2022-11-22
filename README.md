# ZiQiangBackend
珈有好食项目
## 开发要求
在主分支下拉取以各自name拼音缩写的分支
完成任务后merge到主分支

### 目前完成的配置

参考所给的资料：美多商城/C01-Prepare/Config.html中的配置部分

参考：https://www.bilibili.com/video/BV1ya411A7C8?p=10&vd_source=763af5f146c65b47f793e885944c3b1b

11月22日：进行的修改有：

- 将setting.py改成dev(开发使用)和prod(生产使用)两个文件，现在是开发阶段，使用dev作为配置文件

  ![image-20221122164718791](img\image-20221122164718791.png)

- 在dev中配置了mysql数据库，redis数据库

- 我们所写的应用在`NewmanBackend/NewmanBackend/apps`中进行，里面放了一个test_lhw应用：

  ![image-20221122165213905](img\image-20221122165213905.png)

  创建应用后记得在dev.py中INSTALLED_APPS添加:

  ![image-20221122165442050](img\image-20221122165442050.png)

- 日志文件还没有配置好

```shell
.
│  .gitignore
│  README.md
│
├─.idea
│  │  .gitignore
│  │  dataSources.local.xml
│  │  dataSources.xml
│  │  misc.xml
│  │  modules.xml
│  │  vcs.xml
│  │  workspace.xml
│  │  ZiQiangBackend.iml
│  │
│  ├─dataSources
│  │  │  ee7b8b93-cff9-45c7-bfbe-5d3eb137f316.xml
│  │  │
│  │  └─ee7b8b93-cff9-45c7-bfbe-5d3eb137f316
│  │      └─storage_v2
│  │          └─_src_
│  │              └─schema
│  │                      information_schema.FNRwLQ.meta
│  │                      performance_schema.kIw0nw.meta
│  │                      ZqNewmanDb.T0K2qg.meta
│  │
│  └─inspectionProfiles
│          profiles_settings.xml
│
└─NewmanBackend
    │  manage.py
    │
    └─NewmanBackend
        │  asgi.py
        │  db.sqlite3
        │  urls.py
        │  wsgi.py
        │  __init__.py
        │
        ├─apps
        │  │  __init__.py
        │  │
        │  └─test_lhw
        │      │  admin.py
        │      │  apps.py
        │      │  models.py
        │      │  tests.py
        │      │  views.py
        │      │  __init__.py
        │      │
        │      ├─migrations
        │      │  │  __init__.py
        │      │  │
        │      │  └─__pycache__
        │      │          __init__.cpython-38.pyc
        │      │
        │      └─__pycache__
        │              admin.cpython-38.pyc
        │              apps.cpython-38.pyc
        │              models.cpython-38.pyc
        │              __init__.cpython-38.pyc
        │
        ├─logs
        │      .gitkeep
        │      mylog.log
        │
        ├─settings
        │  │  dev.py
        │  │  prod.py
        │  │
        │  └─__pycache__
        │          dev.cpython-38.pyc
        │
        └─__pycache__
                urls.cpython-38.pyc
                wsgi.cpython-38.pyc
                __init__.cpython-38.pyc
```


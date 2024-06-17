# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_mcsm']

package_data = \
{'': ['*'], 'nonebot_plugin_mcsm': ['static/icons/*', 'static/templates/*']}

install_requires = \
['httpx>=0.13.0',
 'jinja2>=3.1.4',
 'nonebot-adapter-onebot>=2.2.3',
 'nonebot-plugin-htmlrender>=0.3.1',
 'nonebot2>=2.2.0']

setup_kwargs = {
    'name': 'nonebot-plugin-mcsm',
    'version': '0.1.5',
    'description': 'MCSM plugin for NoneBot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n\n<h1 align="center">MCSM小助手</h1>\n\n_✨ 对接MCSM的管理插件，可用于查询面板、节点、实例信息以及管理实例✨_\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">\n    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-analysis-bilibili">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-analysis-bilibili.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</p>\n\n\n## 安装\n\n### nb-cli\n\n```shell\nnb plugin install nonebot_plugin_mcsm\n```\n\n### pip\n\n```shell\npip install nonebot_plugin_mcsm\n```\n\n### git\n```shell\ngit clone https://github.com/LiLuo-B/nonebot-plugin-mcsm.git\n```\n\n## 配置\n\n### .env|.env.prod|.env.dev\n\n| 配置项        | 说明                             |\n| ------------- | -------------------------------- |\n| mcsm_api_key  | MCSM API Key                     |\n| mcsm_url      | MCSM面板地址                     |\n| mcsm_img_path | 背景图片地址                     |\n| mcsm_log_size | 日志输出大小（单位KB，默认1024） |\n\n## 使用\n\n| 指令     | 权限 | 相关参数                                              |\n| -------- | ---- | ----------------------------------------------------- |\n| 面板信息 | 超管 | 无                                                    |\n| 节点列表 | 超管 | 无                                                    |\n| 实例列表 | 超管 | 节点序号，可通过“节点列表”查看                        |\n| 实例详情 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |\n| 实例启动 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |\n| 实例关闭 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |\n| 实例重启 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |\n| 实例终止 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |\n| 实例更新 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |\n| 实例日志 | 超管 | 节点序号 实例序号，分别通过“节点列表”、“实例列表”查看 |\n\n## 示例\n\n### 面板信息\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/panel_info.png" width="800"></img>\n\n### 节点列表\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/node_list.png" width="800"></img>\n\n### 实例列表\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/instance_list.png" width="800"></img>\n\n### 实例详情\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/instance_info.png" width="800"></img>\n\n### 实例重启\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-mcsm/blob/main/image/instance_restart.png" width="800"></img>',
    'author': 'LiLuo-B',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LiLuo-B/nonebot-plugin-mcsm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

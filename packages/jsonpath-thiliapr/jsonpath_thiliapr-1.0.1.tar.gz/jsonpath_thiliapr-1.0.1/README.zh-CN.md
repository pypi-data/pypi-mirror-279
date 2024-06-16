![GitHub top language](https://img.shields.io/github/languages/top/thiliapr/tkjsonpath)
![GitHub License](https://img.shields.io/badge/license-GPL--3.0--or--later-blue)
![GitHub repo size](https://img.shields.io/github/repo-size/thiliapr/tkjsonpath)
![GitHub forks](https://img.shields.io/github/forks/thiliapr/tkjsonpath)
![GitHub Repo stars](https://img.shields.io/github/stars/thiliapr/tkjsonpath)

# TkJSONPath
这是一个简单的JSONPath解析器。
- 版本: 1.0.1
- 版权: 根据GPL-3.0或更高版本分发。

## 语言
- [简体中文](README.zh-CN.md)
- [English](README.md)

## 使用
- 以下示例展示了4个基本函数的使用。
  ```python
  from tkjsonpath import jsonpath

  src = {"docs": [{"how": "how?", "id": 1}, {"how": "emm", "id": 2}]}

  path_a = "$.docs"
  path_b = "$[0].how"

  # path_ab -> "$.docs[0].how"
  path_ab = jsonpath.concat_path(path_a, path_b)

  # how_1 -> "how?"
  how_1 = jsonpath.get(src, path_ab)

  # dst -> src
  dst = src.copy()
  # dst["docs"][1]["id"] -> 4
  jsonpath.assign(dst, "$.docs[1].id", 4)
  ```
  1. `src`被赋值为一个字典
  2. 将`path_a`与`path_b`拼合，赋值给`path_ab`。
  3. 获取`src`中路径`path_ab`的值，赋值给`how_1`。
  4. 将`src`复制出一份副本，赋值给`dst`。
  5. 赋值给`dst`中路径`$.docs[1].id`的值，值为`4`。

关于全部函数的使用，请参阅[文档](docs/index.zh-CN.md)。

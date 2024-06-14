<h1 align="center">pyqiniu_util</h1>

- qiniu_util.py

七牛云oss封装，使用示例：

```python
# 上传
qiniu = QiniuFunction()
ret, info = qiniu.upload_file(local_file, remote_file)
```

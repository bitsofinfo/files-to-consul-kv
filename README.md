# files-to-consul-kv


```
 ./fs2consulkv.py \
    --fs-kv-path ./consul-kv/ \
    --consul-url https://[consul-fqdn][:port] \
    --consul-acl-token xxxxxxx \
    --consul-data-center optional-dc \
    --consul-kv-root some/root/path/
 ```



## Usage

 ```
 $ ./fs2consulkv.py  -h

usage: fs2consulkv.py [-h] [-p FS_KV_PATH] [-k CONSUL_KV_ROOT] [-c CONSUL_URL]
                      [-t CONSUL_ACL_TOKEN] [-d CONSUL_DATA_CENTER] [-x] [-n]
                      [-l LOG_LEVEL] [-b LOG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -p FS_KV_PATH, --fs-kv-path FS_KV_PATH
                        Full or relative path to filesystem directory
                        containing the KV structure to send to consul
                        (default: ./)
  -k CONSUL_KV_ROOT, --consul-kv-root CONSUL_KV_ROOT
                        Root path in Consul KV by which all new keys will be
                        set, required. i.e. some/root/path (default: None)
  -c CONSUL_URL, --consul-url CONSUL_URL
                        Consul url, required. i.e. http[s]://[fqdn][:port]
                        (default: None)
  -t CONSUL_ACL_TOKEN, --consul-acl-token CONSUL_ACL_TOKEN
                        Consul acl token, required (default: None)
  -d CONSUL_DATA_CENTER, --consul-data-center CONSUL_DATA_CENTER
                        Consul data-center, optional. (default: None)
  -x, --skip-prompt     Skip confirmation and prompt (default: False)
  -n, --retain-trailing-newlines
                        Retain trailing newline chars (\n) in values files and
                        do not strip them. Default behavior is to strip them
                        (default: False)
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        log level, DEBUG, INFO, etc (default: DEBUG)
  -b LOG_FILE, --log-file LOG_FILE
                        Path to log file; default None = STDOUT (default:
                        None)
```
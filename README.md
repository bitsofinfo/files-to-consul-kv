# files-to-consul-kv

Simple utility for bulk loading sets of [Consul key-value](https://www.consul.io/docs/agent/kv.html) entries via the [transactions API](https://www.consul.io/api/txn.html) where the source of those values exist on disk in a directory structure. 

For example given a simple directory structure like:
```
cd mykvs/

$ find . -print
.
./sub
./sub/key2
./key1

$ cat key1 
val1

$ cat sub/key2 
val2
```

You could use `fs2consulkv.py` to set all these in Consul under some root path:
```
 ./fs2consulkv.py \
    --fs-kv-path ./mykvs \
    --consul-url https://[consul-fqdn][:port] \
    --consul-acl-token xxxxxxx \
    --consul-data-center optional-dc \
    --consul-kv-root some/root/path/
 ```

Would result in your KVs in consul at:
```
https://[consul-fqdn][:port]/ui/mydc/kv/some/root/path/key1 = val1
https://[consul-fqdn][:port]/ui/mydc/kv/some/root/path/sub/key2 = val2
```

## Docker

Run via Docker:
https://hub.docker.com/r/bitsofinfo/files-to-consul-kv

```
docker run -i -v `pwd`/mykvs:/kvsource \
   bitsofinfo/files-to-consul-kv fs2consulkv.py \
   --fs-kv-path /kvsource \
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
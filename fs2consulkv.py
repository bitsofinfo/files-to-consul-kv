#!/usr/bin/env python3

# https://www.consul.io/api/txn.html
# https://github.com/hashicorp/consul/issues/7278

import os
import base64
import requests
import json
import logging
import sys
import time
import argparse


# Yield successive n-sized 
# chunks from l. 
# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(l, n): 
    
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--fs-kv-path', dest='fs_kv_path', default="./", \
        help="Full or relative path to filesystem directory containing the KV structure to send to consul")

    parser.add_argument('-k', '--consul-kv-root', dest='consul_kv_root', default=None, \
        help="Root path in Consul KV by which all new keys will be set, required. i.e. some/root/path")

    parser.add_argument('-c', '--consul-url', dest='consul_url', default=None, \
        help="Consul url, required. i.e. http[s]://[fqdn][:port]")

    parser.add_argument('-t', '--consul-acl-token', dest='consul_acl_token', default=None, \
        help="Consul acl token, required")

    parser.add_argument('-f', '--consul-acl-token-file', dest='consul_acl_token_file', default=None, \
        help="Consul acl token file, path to a file that contains the token value, required")

    parser.add_argument('-d', '--consul-data-center', dest='consul_data_center', default=None, \
        help="Consul data-center, optional.")

    parser.add_argument('-x', '--skip-prompt', action='store_true', default=False, \
        help="Skip confirmation and prompt")

    parser.add_argument('-n', '--retain-trailing-newlines', action='store_true', default=False, \
        help="Retain trailing newline chars (\\n) in values files and do not strip them. Default behavior is to strip them")

    parser.add_argument('-l', '--log-level', dest='log_level', default="DEBUG", \
        help="log level, DEBUG, INFO, etc")
    parser.add_argument('-b', '--log-file', dest='log_file', default=None, \
        help="Path to log file; default None = STDOUT")

    args = parser.parse_args()

    dump_help = False

    if not args.consul_kv_root:
        dump_help = True
   
    if dump_help:
        parser.print_help()
        sys.exit(1)

    logging.basicConfig(level=logging.getLevelName(args.log_level),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename=args.log_file,filemode='w')
    logging.Formatter.converter = time.gmtime

    url = "{}/v1/txn".format(args.consul_url)

    if args.consul_data_center is not None:
        url += "?dc={}".format(args.consul_data_center)

    consul_acl_token = args.consul_acl_token
    if args.consul_acl_token_file:
        with open (args.consul_acl_token_file, "r") as tokenfile:
            value = tokenfile.read()
            if value and value.strip() == '':
                logging.error("--consul-acl-token-file {} contains nothing!".format(args.consul_acl_token_file))
                sys.exit(1)
            else:
                consul_acl_token = value

    if not consul_acl_token or consul_acl_token.strip() == '':
        logging.error("--consul-acl-token-file or --consul-acl-token is required!")

    headers = {
        'Content-Type': "application/json",
        'X-Consul-Token': consul_acl_token,
        'User-Agent': "github.com/bitsofinfo/files-to-consul-kv",
        'Accept': "*/*",
        'Cache-Control': "no-cache"
    }

    try:
        kvs = []

        if args.consul_kv_root.strip().endswith('/'):
            args.consul_kv_root = args.consul_kv_root.strip()[:-1]

        for root, dirs, files in os.walk(args.fs_kv_path):

            for name in files:
                filepath = os.path.join(root, name)
            
                targetkv = filepath.replace(args.fs_kv_path,"")

                with open (filepath, "r") as kvfile:
                    value = kvfile.read()

                if not args.retain_trailing_newlines:
                     if value.endswith('\n'):
                        value = value[:-1]

                if targetkv.startswith('/'):
                    targetkv = targetkv[1:]

                kvs.append({
                    "KV": {
                    "Verb": "set",
                    "Key": "{}/{}".format(args.consul_kv_root,targetkv),
                    "Value": "{}".format(base64.b64encode(value.encode("utf-8")).decode("utf-8"))
                    }
                })

        if not args.skip_prompt:
            print(json.dumps(kvs,indent=2))
            proceed = input("\n\nYou are about to 'set' the above consul KV paths:\n... that were consumed from {}\n... will be PUT against {}\n... and set relative from {}/\n\nAre you sure?: (y|n):".format(args.fs_kv_path,url,args.consul_kv_root)).strip()
            if proceed.lower() != 'y':
                logging.info("Exiting, confirmation prompt input was: " + proceed)
                sys.exit(1)


        # we can only max send 64 per request...
        # https://github.com/hashicorp/consul/issues/7278
        kv_chunks = list(divide_chunks(kvs, 64)) 

        logging.info("Number of kvs totals: {}, this has to be split up " \
            "into {} 64 kv chunks: https://github.com/hashicorp/consul/issues/7278".format(len(kvs),len(kv_chunks)))
        
        for kvchunk in kv_chunks:

            logging.info("PUTing chunk with {} keys @ {}".format(len(kvchunk),url))

            response = requests.request("PUT", url, data=json.dumps(kvchunk), headers=headers)
            
            if response.status_code == 200:
                logging.debug("KVs 'set' OK: {}".format(response.content))
            else:
                print(response.status_code)
                logging.error("KVs 'set' http response code: {} FAILED: {} ".format(response.status_code,json.loads(response.content)))


    except Exception as e:
        logging.exception("error PUTing consul KVs via /txn: POST-DATA={} ERROR={} " \
            .format(kvs,str(sys.exc_info()[:2])))



if __name__ == '__main__':
    main()
#!/bin/bash

set -e

not_in_array() {
    local needle="$1"
    shift 1
    local haystack=("$@")

    local value
    for value in "${haystack[@]}"; do
        [ "$value" = "$needle" ] && return 1
    done
    return 0
}


if [ "$(id -u)" -eq 0 ]; then

if hash apt-get 2>/dev/null; then
  if lsb_release -a | grep Ubuntu; then
      if [ -f "/usr/share/doc/apt/examples/sources.list" ]; then
        mkdir -p /etc/apt
        cp -rf /usr/share/doc/apt/examples/sources.list /etc/apt/sources.list
      fi
      if [ -f "/etc/apt/sources.list" ]; then
        sed -i "s@http://.*archive.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
        sed -i "s@http://.*security.ubuntu.com@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
      fi
  fi
fi

if hash apt-get 2>/dev/null; then
  if lsb_release -a | grep Debian; then
    if [ -f "/etc/apt/sources.list.d/debian.sources" ]; then
      sed -i "s@http://.*deb.debian.org@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list.d/debian.sources
    fi
  fi
fi

if not_in_array docker "$@" ; then
if hash docker 2>/dev/null; then
mkdir -p /etc/docker
cat <<EOF | tee /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://dockerproxy.com",
    "https://docker.nju.edu.cn",
    "https://docker.mirrors.sjtug.sjtu.edu.cn",
    "https:docker.m.daocloud.io",
    "https://registry-1.docker.io"
  ]
}
EOF
systemctl daemon-reload && systemctl restart docker
fi
fi


## https://zhuanlan.zhihu.com/p/655419673
## https://github.com/ciiiii/cloudflare-docker-proxy
if not_in_array containerd "$@" ; then
if hash containerd 2>/dev/null; then
mkdir -p /etc/containerd
cat <<EOF | tee /etc/containerd/config.toml
version = 2

[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
    [plugins."io.containerd.grpc.v1.cri".registry]
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["https://dockerproxy.com","https://docker.nju.edu.cn","https://docker.mirrors.sjtug.sjtu.edu.cn","https://docker.m.daocloud.io","https://registry-1.docker.io"]
EOF
systemctl daemon-reload && systemctl restart containerd
fi
fi

if [ -f "/usr/share/zoneinfo/Asia/Shanghai" ]; then
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
fi

fi



if hash npm 2>/dev/null; then
  npm config set registry http://registry.npmmirror.com
  npm cache clean -f

  npm config set disturl https://repo.huaweicloud.com/nodejs

  npm config set sass_binary_site https://repo.huaweicloud.com/node-sass

  npm config set phantomjs_cdnurl https://repo.huaweicloud.com/phantomjs
  npm config set chromedriver_cdnurl https://repo.huaweicloud.com/chromedriver
  npm config set operadriver_cdnurl https://repo.huaweicloud.com/operadriver

  npm config set electron_mirror https://repo.huaweicloud.com/electron/
  npm config set python_mirror https://repo.huaweicloud.com/python

  npm config set sqlite3_binary_host_mirror https://foxgis.oss-cn-shanghai.aliyuncs.com/
  npm config set profiler_binary_host_mirror https://npm.taobao.org/mirrors/node-inspector/
fi

## https://mirrors.cernet.edu.cn/list/pypi
PYPI_INDEX=https://mirror.nju.edu.cn/pypi/web/simple
PYPI_INDEX_EXTRA_1=https://deksep-pypi.pkg.coding.net/common/pypi/simple
PYPI_INDEX_EXTRA_2=https://mirror.sjtu.edu.cn/pypi/web/simple

if hash pip3 2>/dev/null; then
mkdir -p $HOME/.config/pip
cat <<EOF | tee $HOME/.config/pip/pip.conf
[global]
index-url = $PYPI_INDEX
extra-index-url = $PYPI_INDEX_EXTRA_1
;                 $PYPI_INDEX_EXTRA_2
EOF
fi

if hash pdm 2>/dev/null; then
  pdm config pypi.url $PYPI_INDEX
  pdm config pypi.extra.url $PYPI_INDEX_EXTRA_1
#  pdm config pypi.extra.url $PYPI_INDEX_EXTRA_2
fi

if hash gem 2>/dev/null; then
  gem sources --add https://gems.ruby-china.com/ --remove https://rubygems.org/
fi

# 第一阶段: 构建项目
FROM node:lts-alpine as build

WORKDIR /app

# 拷贝依赖文件
COPY package.json package-lock.json ./

# 安装依赖
RUN npm i

# 拷贝项目文件
COPY . .


# 使用nginx作为web服务器
FROM nginx:1.19.4-alpine

RUN rm -rf /usr/share/nginx/html/*

COPY nginx.conf.template /etc/nginx/conf.d

RUN rm /etc/nginx/nginx.conf
# 删除nginx中之前的配置
RUN rm /etc/nginx/conf.d/default.conf

RUN rm /etc/nginx/conf.d/nginx.conf.template

# 拷贝当前的文件到nginx中
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf.template /etc/nginx/conf.d/default.conf.template

# 拷贝第一阶段构建的项目文件
COPY --from=build /app /usr/share/nginx/html
# COPY ./dist /usr/share/nginx/html

WORKDIR /etc/nginx/conf.d

# 写入环境变量并运行
ENTRYPOINT envsubst '$SERVER_URL $CLIENT_PORT'  < default.conf.template > default.conf && cat default.conf && nginx -g 'daemon off;'

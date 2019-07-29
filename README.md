# AWDFF

AWD-FOR-FUN  
开源AWD平台

# 第一次开始

## 执行


初始化数据库以及静态文件   
生成配置文件
```bash
cd script
bash init.sh
cp config.yml.bak config.yml

```


创建一个管理员账户
```bash
python manage.py createsuperuser --username xxx --email xxxx
```


## 配置文件说明
```yaml
start_time: '2019/7/29 15:00:00'
end_time: '2019/7/29 19:00:00'
check_time_interval: 2
round_time_interval: 10
check_log: '/tmp/check.log'
round_log: '/tmp/round.log'
play_now: True
```

+ start_time 格式为 '%Y/%m/%d %H:%M:%S' 为比赛开始时间,会根据这个时间判定是否能看到题目,
是否能提交FLAG
+ end_time 格式为 '%Y/%m/%d %H:%M:%S' 为比赛结束时间,会根据这个时间判定是否能提交FLAG
+ check_time_interval check脚本每多少分钟执行一次
+ round_time_interval 一轮多长时间
+ check_log check脚本日志文件的位置
+ round_log 更新轮数脚本文件的位置
+ play_now play_now模式是否开启

### PLAY_NOW 模式说明
由于本平台定时任务采用的cron,又由于作者十分菜鸡的缘故,暂时未找到crontab可以在非整点循环的表达式方法,所以切入了一个新的模式
- PLAY_NOW 模式开启
    + 执行`bash start_check.sh`后,定时任务马上执行,开始时间(用于计算距离下轮数时间)从执行`start_check.sh`这一刻开始算起
- PLAY_NOW 模式关闭
    + 执行`bash start_check.sh`后,定时任务等到配置文件中的开始时间开始,结束时间结束,要求开始和结束时间都必须是整点
    





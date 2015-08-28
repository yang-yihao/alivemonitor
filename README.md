# 服务存活监听器 (Services Availability Monitor)

## 软件用途 (Software Purpose)

用于监测指定的http服务是否可用，当服务从可用状态变为不可用，或由不可用状态变成可用时，系统会向指定的用户发送邮件通知.

Monitoring availability of given http services.
Sending email to administrators when status of services become available or unavailable.

## 软件功能 (Functions of this software)

* 可配置要监测的服务；
* 可配置每个服务在状态变动时要通知的用户邮箱列表；
* 可定义http服务不可用的标准（监测次数+时间间隔）；

* Services to monitor is configurable.
* Administrators of notification are configurable per service.
* Customization of what is service unavailable (times of monitoring and monitor interval).

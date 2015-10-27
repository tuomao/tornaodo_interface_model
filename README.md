# tornaodo_interface_model

一个基于tornado框架搭建的，用来写客户端接口的框架，该框架的扩展性和努棒性比较差，但是在写客户端接口的时候，开发十分的高效。

## 框架的逻辑流程

1. 在server启动初始化的时候，初始化全局变量和数据库连接。
2. 在请求到来的时候，handler层负责解析请求，分发请求到processor，最后根据processor层里面传回来得处理结果，构造返回的数据。让processor层专注于业务逻辑的处理，从最后构造返回字符串中解放出来。
3. processor层的processor是基于base_processor构造的。base_processor的主要功能是提取handler里面的参数，保存在processor里面。


## 框架实现的功能

1. 数据库做了读写分离
2. 框架能区分开发环境和部署环境，根据setting里面的HOSTS来进行区分
3. 框架提供了一些数据操作的基本工具类

## 未来的工作

1. 减小各个模块之间的耦合性，增加整个框架的鲁棒性。
2. 完善其中逻辑不完整和合理的地方







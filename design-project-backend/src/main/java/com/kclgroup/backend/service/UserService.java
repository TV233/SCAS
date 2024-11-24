package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.User;
import com.baomidou.mybatisplus.extension.service.IService;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;


/**
* @author 张小明
* @description 针对表【user】的数据库操作Service
* @createDate 2024-06-23 20:02:22
*/
@Resource
public interface UserService extends IService<User> {
    //根据用户名查询用户
    User findByUserName(String username);

    //注册
    void register(String username, String password);


    //更新
    void update(User user);

    //更新头像
//    void updateAvatar(String avatarUrl);

    //更新密码
    void updatePwd(String newPwd);


}

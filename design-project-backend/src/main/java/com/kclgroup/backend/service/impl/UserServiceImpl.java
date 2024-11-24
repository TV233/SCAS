package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.Favor;
import com.kclgroup.backend.pojo.entity.StockInfo;
import com.kclgroup.backend.pojo.entity.User;
import com.kclgroup.backend.service.FavorService;
import com.kclgroup.backend.service.StockInfoService;
import com.kclgroup.backend.service.UserService;
import com.kclgroup.backend.mapper.UserMapper;
import com.kclgroup.backend.util.Md5Util;
import com.kclgroup.backend.util.ThreadLocalUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Map;

/**
* @author 张小明
* @description 针对表【user】的数据库操作Service实现
* @createDate 2024-06-23 20:02:22
*/
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private StockInfoService stockInfoService;
    @Autowired
    private FavorService favorService;
    @Override
    public User findByUserName(String username) {
        User user = userMapper.findByUserName(username);
        return user;
    }

    @Override
    public void register(String username, String password) {
        //加密
        String md5String = Md5Util.getMD5String(password);
        //添加
        userMapper.add(username,md5String);
    }

    @Override
    public void update(User user) {
        user.setUpdateTime(LocalDateTime.now());
        userMapper.update(user);
    }

//    @Override
//    public void updateAvatar(String avatarUrl) {
////        Map<String,Object> map = ThreadLocalUtil.get();
////        Integer id = (Integer) map.get("id");
////        userMapper.updateAvatar(avatarUrl,id);
//    }

    @Override
    public void updatePwd(String newPwd) {
        Map<String,Object> map = ThreadLocalUtil.get();
        Integer id = (Integer) map.get("id");
        userMapper.updatePwd(Md5Util.getMD5String(newPwd),id);
    }





}



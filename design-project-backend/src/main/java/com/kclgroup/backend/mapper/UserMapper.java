package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.User;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

/**
* @author 张小明
* @description 针对表【user】的数据库操作Mapper
* @createDate 2024-06-23 20:02:22
* @Entity com.kclgroup.backend.pojo/entity.User
*/
@Mapper
public interface UserMapper extends BaseMapper<User> {
    //根据用户名查询用户
    @Select("select * from user where username=#{username}")
    User findByUserName(String username);

    //添加
    @Insert("insert into user(username,password,create_time,update_time)" +
            " values(#{username},#{password},now(),now())")
    void add(String username, String password);

    @Update("update user set nickname=#{nickname},email=#{email},update_time=#{updateTime} where id=#{id}")
    void update(User user);

//    @Update("update user set user_pic=#{avatarUrl},update_time=now() where id=#{id}")
//    void updateAvatar(String avatarUrl,Integer id);

    @Update("update user set password=#{md5String},update_time=now() where id=#{id}")
    void updatePwd(String md5String, Integer id);
}





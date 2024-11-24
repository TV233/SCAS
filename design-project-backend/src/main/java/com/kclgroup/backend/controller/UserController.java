package com.kclgroup.backend.controller;

import com.kclgroup.backend.pojo.entity.Favor;
import com.kclgroup.backend.pojo.entity.Result;
import com.kclgroup.backend.pojo.entity.StockInfo;
import com.kclgroup.backend.pojo.entity.User;
import com.kclgroup.backend.service.FavorService;
import com.kclgroup.backend.service.UserService;
import com.kclgroup.backend.util.JwtUtil;
import com.kclgroup.backend.util.Md5Util;
import com.kclgroup.backend.util.ThreadLocalUtil;
import jakarta.validation.constraints.Pattern;
import org.hibernate.validator.constraints.URL;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.util.StringUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.TimeUnit;

@RestController
// @RequestMapping("/user")
@Validated
public class UserController {

  @Autowired private UserService userService;
  @Autowired private StringRedisTemplate stringRedisTemplate;

  @PostMapping("/auth/register")
  public Result register(
      @Pattern(regexp = "^\\S{5,16}$") String username,
      @Pattern(regexp = "^\\S{5,16}$") String password) {

    // 查询用户
    User u = userService.findByUserName(username);
    if (u == null) {
      // 没有占用
      // 注册
      userService.register(username, password);
      return Result.success();
    } else {
      // 占用
      return Result.error("用户名已被占用");
    }
  }

  @PostMapping("/auth/login")
  public Result<String> login(
      @Pattern(regexp = "^\\S{5,16}$") String username,
      @Pattern(regexp = "^\\S{5,16}$") String password) {
    // 根据用户名查询用户
    User loginUser = userService.findByUserName(username);
    // 判断该用户是否存在
    if (loginUser == null) {
      return Result.error("用户名错误");
    }

    // 判断密码是否正确  loginUser对象中的password是密文
    if (Md5Util.getMD5String(password).equals(loginUser.getPassword())) {
      // 登录成功
      Map<String, Object> claims = new HashMap<>();
      claims.put("id", loginUser.getId());
      claims.put("username", loginUser.getUsername());
      String token = JwtUtil.genToken(claims);
      // 把token存储到redis中
      ValueOperations<String, String> operations = stringRedisTemplate.opsForValue();
      operations.set(token, token, 1, TimeUnit.HOURS);
      return Result.success(token);
    }
    return Result.error("密码错误");
  }

  @GetMapping("/user/userInfo")
  public Result<User> userInfo(/*@RequestHeader(name = "Authorization") String token*/ ) {
    // 根据用户名查询用户
    /* Map<String, Object> map = JwtUtil.parseToken(token);
    String username = (String) map.get("username");*/
    Map<String, Object> map = ThreadLocalUtil.get();
    String username = (String) map.get("username");
    User user = userService.findByUserName(username);
    return Result.success(user);
  }

  @PutMapping("/user/update")
  public Result update(@RequestBody @Validated User user) {
    Map<String, Object> map = ThreadLocalUtil.get();
    Integer id = (Integer) map.get("id");
    if (!Objects.equals(user.getId(), id)) return Result.error("要修改的用户id错误");
    userService.update(user);
    return Result.success();
  }

  //    @PatchMapping("updateAvatar")
  //    public Result updateAvatar(@RequestParam @URL String avatarUrl) {
  //        userService.updateAvatar(avatarUrl);
  //        return Result.success();
  //    }

  @PatchMapping("/user/updatePwd")
  public Result updatePwd(
      @RequestBody Map<String, String> params, @RequestHeader("Authorization") String token) {
    // 1.校验参数
    String oldPwd = params.get("old_pwd");
    String newPwd = params.get("new_pwd");
    String rePwd = params.get("re_pwd");

    if (!StringUtils.hasLength(oldPwd)
        || !StringUtils.hasLength(newPwd)
        || !StringUtils.hasLength(rePwd)) {
      return Result.error("缺少必要的参数");
    }

    // 原密码是否正确
    // 调用userService根据用户名拿到原密码,再和old_pwd比对
    Map<String, Object> map = ThreadLocalUtil.get();
    String username = (String) map.get("username");
    User loginUser = userService.findByUserName(username);
    if (!loginUser.getPassword().equals(Md5Util.getMD5String(oldPwd))) {
      return Result.error("原密码填写不正确");
    }

    // newPwd和rePwd是否一样
    if (!rePwd.equals(newPwd)) {
      return Result.error("两次填写的新密码不一样");
    }

    // 2.调用service完成密码更新
    userService.updatePwd(newPwd);
    // 删除redis中对应的token
    ValueOperations<String, String> operations = stringRedisTemplate.opsForValue();
    operations.getOperations().delete(token);
    return Result.success();
  }
}

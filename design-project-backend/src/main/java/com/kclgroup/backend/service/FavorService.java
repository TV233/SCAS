package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.Favor;
import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.vo.FavorVo;

import java.util.List;

/**
* @author 张小明
* @description 针对表【favor】的数据库操作Service
* @createDate 2024-06-25 14:11:43
*/
public interface FavorService extends IService<Favor> {

    Favor getFavor(String username, String stockCode);
    void favor(String username,String stockCode);

    void cancelFavor(String username, String stockCode);

    List<FavorVo> getFavorList(String username);
}

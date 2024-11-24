package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.Favor;
import com.kclgroup.backend.pojo.vo.FavorVo;
import com.kclgroup.backend.service.FavorService;
import com.kclgroup.backend.mapper.FavorMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 张小明
* @description 针对表【favor】的数据库操作Service实现
* @createDate 2024-06-25 14:11:43
*/
@Service
public class FavorServiceImpl extends ServiceImpl<FavorMapper, Favor>
    implements FavorService{
    @Autowired
    FavorMapper favorMapper;
    @Override
    public Favor getFavor(String username, String stockCode) {
        Favor favor = favorMapper.getFavor(username, stockCode);
        return favor;
    }

    @Override
    public void favor(String username, String stockCode) {
        favorMapper.addFavor(username, stockCode);
    }

    @Override
    public void cancelFavor(String username, String stockCode) {
        favorMapper.deleteFavor(username,stockCode);
    }

    @Override
    public List<FavorVo> getFavorList(String username) {
        List<FavorVo> favorList = favorMapper.getFavorList(username);
        return favorList;
    }

}





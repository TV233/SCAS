package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.MarketStyle;
import com.kclgroup.backend.service.MarketStyleService;
import com.kclgroup.backend.mapper.MarketStyleMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 张小明
* @description 针对表【market_style】的数据库操作Service实现
* @createDate 2024-06-24 21:07:10
*/
@Service
public class MarketStyleServiceImpl extends ServiceImpl<MarketStyleMapper, MarketStyle>
    implements MarketStyleService{

    @Autowired
    private MarketStyleMapper marketStyleMapper;
    @Override
    public List<MarketStyle> getMarketStyle() {
        List<MarketStyle> marketStyles = marketStyleMapper.getMarketStyle();
        return marketStyles;
    }
}





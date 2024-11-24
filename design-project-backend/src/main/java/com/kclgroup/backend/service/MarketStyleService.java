package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.MarketStyle;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;

/**
* @author 张小明
* @description 针对表【market_style】的数据库操作Service
* @createDate 2024-06-24 21:07:10
*/
public interface MarketStyleService extends IService<MarketStyle> {

    List<MarketStyle> getMarketStyle();
}

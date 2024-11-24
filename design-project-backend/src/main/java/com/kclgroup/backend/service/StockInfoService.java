package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.StockInfo;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;

/**
* @author 张小明
* @description 针对表【stock_info】的数据库操作Service
* @createDate 2024-06-25 13:58:37
*/

public interface StockInfoService extends IService<StockInfo> {

    StockInfo getByStockCode(String stockCode);

    List<StockInfo> getStockInfoByStockName(String stockName);
}

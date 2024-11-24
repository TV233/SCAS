package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.StockIndices;
import com.kclgroup.backend.pojo.entity.StockPrices;
import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.vo.PriceVo;
import com.kclgroup.backend.pojo.vo.StockPriceVo;

import java.util.List;

/**
* @author 张小明
* @description 针对表【stock_prices】的数据库操作Service
* @createDate 2024-06-25 13:36:30
*/
public interface StockPricesService extends IService<StockPrices> {

    List<StockPriceVo> getStockPrices();

    String getLatestPrice(String stockCode);

    String getPriceChangeRate(String stockCode);

    String getPriceChange(String stockCode);

    String getRiseSpeed(String stockCode);

    PriceVo getUpDown();
}

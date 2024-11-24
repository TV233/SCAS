package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.StockPrices;
import com.kclgroup.backend.pojo.vo.PriceVo;
import com.kclgroup.backend.pojo.vo.StockPriceVo;
import com.kclgroup.backend.service.StockPricesService;
import com.kclgroup.backend.mapper.StockPricesMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.DecimalFormat;
import java.util.List;

/**
* @author 张小明
* @description 针对表【stock_prices】的数据库操作Service实现
* @createDate 2024-06-25 13:36:30
*/
@Service
public class StockPricesServiceImpl extends ServiceImpl<StockPricesMapper, StockPrices>
    implements StockPricesService{
    @Autowired
    private StockPricesMapper stockPricesMapper;
    @Override
    public List<StockPriceVo> getStockPrices() {
        List<StockPriceVo> stockPrices = stockPricesMapper.getStockPrices();
        return stockPrices;
    }

    @Override
    public String getLatestPrice(String stockCode) {
        String latestPrice = stockPricesMapper.getLatestPrice(stockCode);
        return latestPrice;
    }

    @Override
    public String getPriceChangeRate(String stockCode) {
        String priceChangeRate = stockPricesMapper.getPriceChangeRate(stockCode);
        return priceChangeRate;
    }

    @Override
    public String getPriceChange(String stockCode) {
        String priceChange = stockPricesMapper.getPriceChange(stockCode);
        return priceChange;
    }

    @Override
    public String getRiseSpeed(String stockCode) {
        String riseSpeed = stockPricesMapper.getRiseSpeed(stockCode);
        return riseSpeed;
    }

    @Override
    public PriceVo getUpDown() {
        PriceVo priceVo = stockPricesMapper.getUpDown();
        return priceVo;
    }
}





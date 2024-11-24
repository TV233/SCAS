package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.StockInfo;
import com.kclgroup.backend.service.StockInfoService;
import com.kclgroup.backend.mapper.StockInfoMapper;
import org.springframework.stereotype.Service;

import java.util.List;

/**
* @author 张小明
* @description 针对表【stock_info】的数据库操作Service实现
* @createDate 2024-06-25 13:58:37
*/
@Service
public class StockInfoServiceImpl extends ServiceImpl<StockInfoMapper, StockInfo>
    implements StockInfoService{

    @Override
    public StockInfo getByStockCode(String stockCode) {
        StockInfo stockInfo = baseMapper.getByStockCode(stockCode);
        return stockInfo;
    }

    @Override
    public List<StockInfo> getStockInfoByStockName(String stockName) {
        List<StockInfo> stockInfoList = baseMapper.getStockInfoByStockName(stockName);
        return stockInfoList;
    }

}





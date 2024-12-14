package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.pojo.entity.StockKline;
import com.kclgroup.backend.pojo.vo.KlineVo;
import com.kclgroup.backend.service.StockKlineService;
import com.kclgroup.backend.mapper.StockKlineMapper;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StockKlineServiceImpl extends ServiceImpl<StockKlineMapper, StockKline> implements StockKlineService {

    @Autowired
    StockKlineMapper stockKlineMapper;

    @Override
    public List<KlineVo> getStockKline(String stockCode) {
        List<KlineVo> klineVo = stockKlineMapper.getStockKline(stockCode);
        return klineVo;
    }
}

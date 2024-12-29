package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.mapper.SentimentPriceCorrelationMapper;
import com.kclgroup.backend.pojo.entity.SentimentPriceCorrelation;
import com.kclgroup.backend.service.SentimentPriceCorrelationService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SentimentPriceCorrelationServiceImpl extends ServiceImpl<SentimentPriceCorrelationMapper, SentimentPriceCorrelation> implements SentimentPriceCorrelationService {
    
    @Override
    public List<SentimentPriceCorrelation> getByStockCode(String stockCode) {
        QueryWrapper<SentimentPriceCorrelation> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("stock_code", stockCode)
                   .orderBy(true, true, "date");
        return list(queryWrapper);
    }
} 
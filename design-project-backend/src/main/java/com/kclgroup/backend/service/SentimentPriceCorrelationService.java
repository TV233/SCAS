package com.kclgroup.backend.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.entity.SentimentPriceCorrelation;
import java.util.List;

public interface SentimentPriceCorrelationService extends IService<SentimentPriceCorrelation> {
    List<SentimentPriceCorrelation> getByStockCode(String stockCode);
} 
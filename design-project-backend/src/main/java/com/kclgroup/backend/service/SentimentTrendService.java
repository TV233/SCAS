package com.kclgroup.backend.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.entity.SentimentTrend;
import com.kclgroup.backend.pojo.vo.SentimentTrendVo;
import java.util.List;

public interface SentimentTrendService extends IService<SentimentTrend> {
    List<SentimentTrendVo> getSentimentTrend(String stockCode);
} 
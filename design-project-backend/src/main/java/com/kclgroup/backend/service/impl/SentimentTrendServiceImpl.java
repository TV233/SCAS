package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.mapper.SentimentTrendMapper;
import com.kclgroup.backend.pojo.entity.SentimentTrend;
import com.kclgroup.backend.pojo.vo.SentimentTrendVo;
import com.kclgroup.backend.service.SentimentTrendService;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class SentimentTrendServiceImpl extends ServiceImpl<SentimentTrendMapper, SentimentTrend> implements SentimentTrendService {
    
    @Override
    public List<SentimentTrendVo> getSentimentTrend(String stockCode) {
        // 使用LambdaQueryWrapper构建查询条件
        LambdaQueryWrapper<SentimentTrend> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.eq(SentimentTrend::getStockCode, stockCode)
                   .orderByDesc(SentimentTrend::getDate);
        
        List<SentimentTrend> trends = this.list(queryWrapper);
        
        // 转换为VO对象，确保类型匹配
        return trends.stream().map(trend -> {
            SentimentTrendVo vo = new SentimentTrendVo();
            vo.setDate(trend.getDate());
            vo.setSentimentAvg(trend.getSentimentAvg());
            vo.setCommentCount(trend.getCommentCount());
            return vo;
        }).collect(Collectors.toList());
    }
} 
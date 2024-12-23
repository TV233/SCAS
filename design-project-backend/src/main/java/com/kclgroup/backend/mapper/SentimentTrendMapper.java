package com.kclgroup.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.entity.SentimentTrend;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface SentimentTrendMapper extends BaseMapper<SentimentTrend> {
    // 可以添加自定义的查询方法
} 
package com.kclgroup.backend.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.entity.WordFrequency;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface WordFrequencyMapper extends BaseMapper<WordFrequency> {
    // 可以添加自定义的查询方法
} 
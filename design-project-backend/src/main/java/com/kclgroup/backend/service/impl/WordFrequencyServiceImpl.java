package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.mapper.WordFrequencyMapper;
import com.kclgroup.backend.pojo.entity.WordFrequency;
import com.kclgroup.backend.pojo.vo.WordFrequencyVo;
import com.kclgroup.backend.service.WordFrequencyService;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class WordFrequencyServiceImpl extends ServiceImpl<WordFrequencyMapper, WordFrequency> implements WordFrequencyService {

    
    @Override
    public List<WordFrequencyVo> getWordFrequency(String stockCode) {
        // 使用LambdaQueryWrapper构建查询条件
        LambdaQueryWrapper<WordFrequency> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.eq(WordFrequency::getStockCode, stockCode)
                   .orderByDesc(WordFrequency::getFrequency)
                   .last("LIMIT 100"); // 限制返回前100个高频词
        
        List<WordFrequency> frequencies = this.list(queryWrapper);
        
        // 转换为VO对象
        return frequencies.stream().map(freq -> {
            WordFrequencyVo vo = new WordFrequencyVo();
            vo.setWord(freq.getWord());
            vo.setFrequency(freq.getFrequency());
            return vo;
        }).collect(Collectors.toList());
    }
} 
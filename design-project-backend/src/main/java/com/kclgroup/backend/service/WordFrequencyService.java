package com.kclgroup.backend.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.entity.WordFrequency;
import com.kclgroup.backend.pojo.vo.WordFrequencyVo;
import java.util.List;

public interface WordFrequencyService extends IService<WordFrequency> {
    List<WordFrequencyVo> getWordFrequency(String stockCode);
} 
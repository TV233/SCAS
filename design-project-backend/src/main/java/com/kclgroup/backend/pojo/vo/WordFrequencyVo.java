package com.kclgroup.backend.pojo.vo;

import lombok.Data;

@Data
public class WordFrequencyVo {
    private String word;         // 词语
    private Integer frequency;   // 词频
} 
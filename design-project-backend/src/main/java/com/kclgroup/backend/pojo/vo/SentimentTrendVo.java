package com.kclgroup.backend.pojo.vo;

import lombok.Data;
import java.time.LocalDate;

@Data
public class SentimentTrendVo {
    private LocalDate date;          // 日期
    private Float sentimentAvg;      // 修改为Float类型，与实体类保持一致
    private Integer commentCount;     // 评论数量
} 
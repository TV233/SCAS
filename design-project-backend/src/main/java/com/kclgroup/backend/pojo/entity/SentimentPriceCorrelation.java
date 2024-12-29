package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("sentiment_price_correlation")
public class SentimentPriceCorrelation {
    private String stockCode;
    private LocalDate date;
    private Float sentimentAvg;
    private Float priceChange;
    private Float nextDayPriceChange;
    private Float correlation;
    private Integer sentimentCount;
    private Integer isSignificant;
    private LocalDateTime updateTime;
} 
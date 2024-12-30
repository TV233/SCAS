package com.kclgroup.backend.pojo.vo;

import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class SentimentPriceCorrelationVo {
    private String stockCode;
    private LocalDate date;
    private Float sentimentChange;
    private Float priceChange;
    private Float nextDayPriceChange;
    private Float correlation;
    private Integer sentimentCount;
    private Integer isSignificant;
    private LocalDateTime updateTime;
    private String correlationSummary;
} 
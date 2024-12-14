package com.kclgroup.backend.pojo.vo;

import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
public class KlineVo {
    private String stockCode;
    private LocalDate dateTime;
    private BigDecimal openPrice;
    private BigDecimal closePrice;
    private BigDecimal highPrice;
    private BigDecimal lowPrice;
    private Long volume;
    private BigDecimal tradeValue;
    private BigDecimal amplitude;
    private BigDecimal upDownRange;
    private BigDecimal upDownPrice;
    private BigDecimal turnoverRate;
}
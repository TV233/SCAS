package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@TableName(value ="stock_kline")
public class StockKline {
    @TableId
    private Long id;
    
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